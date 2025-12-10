"""
Code parsing utilities using Tree-sitter.
"""
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    from tree_sitter import Language, Parser
except ImportError:
    logger.warning("tree-sitter not available. Some parsing features will be limited.")
    Language = None
    Parser = None


class CodeParser:
    """Wrapper for Tree-sitter based code parsing."""
    
    def __init__(self):
        self.parsers = {}
        self._initialize_parsers()
    
    def _initialize_parsers(self):
        """Initialize language parsers."""
        if Language is None or Parser is None:
            logger.warning("Tree-sitter not available")
            return
        
        try:
            # Python parser
            python_lang = Language('/usr/lib/tree-sitter/tree-sitter-python.so', 'python')
            python_parser = Parser()
            python_parser.set_language(python_lang)
            self.parsers['python'] = python_parser
        except Exception as e:
            logger.warning(f"Could not initialize Python parser: {e}")
    
    def parse_python_file(self, file_path: str) -> Optional[Dict]:
        """
        Parse a Python file and extract structural information.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary with parsed information
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract basic structure without tree-sitter if not available
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)
            imports = self._extract_imports(content)
            
            return {
                'file': file_path,
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None
    
    @staticmethod
    def _extract_functions(content: str) -> List[Dict]:
        """Extract function definitions from Python code."""
        functions = []
        for i, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line.startswith('def '):
                # Extract function name and parameters
                func_sig = line[4:]  # Remove 'def '
                func_name = func_sig.split('(')[0]
                params = func_sig[func_sig.find('('):func_sig.find(')')+1] if '(' in func_sig else ''
                
                functions.append({
                    'name': func_name,
                    'line': i,
                    'signature': func_sig,
                    'params': params
                })
        return functions
    
    @staticmethod
    def _extract_classes(content: str) -> List[Dict]:
        """Extract class definitions from Python code."""
        classes = []
        for i, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line.startswith('class '):
                # Extract class name and bases
                class_sig = line[6:]  # Remove 'class '
                class_name = class_sig.split('(')[0] if '(' in class_sig else class_sig.split(':')[0]
                
                bases = ''
                if '(' in class_sig:
                    bases = class_sig[class_sig.find('('):class_sig.find(')')+1]
                
                classes.append({
                    'name': class_name,
                    'line': i,
                    'signature': class_sig,
                    'bases': bases
                })
        return classes
    
    @staticmethod
    def _extract_imports(content: str) -> List[Dict]:
        """Extract import statements from Python code."""
        imports = []
        for i, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append({
                    'statement': line,
                    'line': i
                })
        return imports


def extract_functions_and_classes(file_path: str) -> Dict:
    """
    Extract functions and classes from a source file.
    
    Args:
        file_path: Path to source file
        
    Returns:
        Dictionary with extracted information
    """
    parser = CodeParser()
    
    if file_path.endswith('.py'):
        return parser.parse_python_file(file_path)
    else:
        # For other languages, return basic info
        return {
            'file': file_path,
            'error': 'Parser not yet implemented for this language'
        }


def analyze_code_relationships(file_contents: List[Tuple[str, str]]) -> Dict:
    """
    Analyze relationships between files and functions.
    
    Args:
        file_contents: List of (file_path, content) tuples
        
    Returns:
        Dictionary representing code relationships
    """
    relationships = {
        'imports': {},
        'calls': {},
        'definitions': {}
    }
    
    parser = CodeParser()
    
    for file_path, content in file_contents:
        if file_path.endswith('.py'):
            parsed = parser.parse_python_file(file_path)
            if parsed:
                relationships['definitions'][file_path] = {
                    'functions': parsed.get('functions', []),
                    'classes': parsed.get('classes', [])
                }
                relationships['imports'][file_path] = parsed.get('imports', [])
    
    return relationships
