"""
Documentation generation utilities.
"""
import os
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Generate markdown documentation from parsed code information."""
    
    def __init__(self):
        self.content = []
    
    def add_heading(self, text: str, level: int = 1):
        """Add a heading."""
        self.content.append('#' * level + ' ' + text + '\n')
    
    def add_paragraph(self, text: str):
        """Add a paragraph."""
        self.content.append(text + '\n\n')
    
    def add_code_block(self, code: str, language: str = 'python'):
        """Add a code block."""
        self.content.append(f'```{language}\n{code}\n```\n\n')
    
    def add_list(self, items: List[str], ordered: bool = False):
        """Add a list."""
        for i, item in enumerate(items, 1):
            prefix = f'{i}.' if ordered else '-'
            self.content.append(f'{prefix} {item}\n')
        self.content.append('\n')
    
    def add_table(self, headers: List[str], rows: List[List[str]]):
        """Add a markdown table."""
        # Header row
        self.content.append('| ' + ' | '.join(headers) + ' |\n')
        # Separator row
        self.content.append('|' + '|'.join([' --- ' for _ in headers]) + '|\n')
        # Data rows
        for row in rows:
            self.content.append('| ' + ' | '.join(row) + ' |\n')
        self.content.append('\n')
    
    def add_horizontal_rule(self):
        """Add a horizontal rule."""
        self.content.append('---\n\n')
    
    def get_content(self) -> str:
        """Get the generated markdown content."""
        return ''.join(self.content)


def generate_project_overview(repo_name: str, repo_info: Dict, readme_summary: str) -> str:
    """
    Generate project overview section.
    
    Args:
        repo_name: Repository name
        repo_info: Repository metadata
        readme_summary: Summary of README
        
    Returns:
        Markdown content
    """
    gen = MarkdownGenerator()
    
    gen.add_heading(repo_name, 1)
    gen.add_paragraph('**Generated on:** ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    if readme_summary:
        gen.add_heading('Overview', 2)
        gen.add_paragraph(readme_summary)
    
    return gen.get_content()


def generate_file_structure(tree: Dict) -> str:
    """
    Generate file structure section.
    
    Args:
        tree: File tree dictionary
        
    Returns:
        Markdown content
    """
    gen = MarkdownGenerator()
    gen.add_heading('Project Structure', 2)
    
    def render_tree(node: Dict, prefix: str = '') -> List[str]:
        lines = []
        if node.get('type') == 'file':
            lines.append(f"{prefix}📄 `{node['name']}`")
        else:
            lines.append(f"{prefix}📁 {node['name']}/")
            children = node.get('children', [])
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                next_prefix = prefix + ('    ' if is_last else '│   ')
                lines.extend(render_tree(child, next_prefix))
        return lines
    
    lines = render_tree(tree)
    for line in lines[:50]:  # Limit output
        gen.content.append(line + '\n')
    
    if len(lines) > 50:
        gen.content.append(f'\n... and {len(lines) - 50} more items\n\n')
    else:
        gen.content.append('\n')
    
    return gen.get_content()


def generate_api_reference(code_analysis: Dict) -> str:
    """
    Generate API reference section.
    
    Args:
        code_analysis: Analyzed code structure
        
    Returns:
        Markdown content
    """
    gen = MarkdownGenerator()
    gen.add_heading('API Reference', 2)
    
    # Group by file
    for file_path, definitions in code_analysis.get('definitions', {}).items():
        gen.add_heading(os.path.basename(file_path), 3)
        
        # Classes
        classes = definitions.get('classes', [])
        if classes:
            gen.add_heading('Classes', 4)
            for cls in classes:
                gen.add_paragraph(f"**`{cls['name']}`** (Line {cls['line']})")
                if cls.get('bases'):
                    gen.add_paragraph(f"*Bases:* {cls['bases']}")
        
        # Functions
        functions = definitions.get('functions', [])
        if functions:
            gen.add_heading('Functions', 4)
            for func in functions:
                gen.add_paragraph(f"**`{func['name']}{func['params']}`** (Line {func['line']})")
    
    return gen.get_content()


def generate_dependencies(imports: Dict) -> str:
    """
    Generate dependencies section.
    
    Args:
        imports: Import information
        
    Returns:
        Markdown content
    """
    gen = MarkdownGenerator()
    gen.add_heading('Dependencies', 2)
    
    all_imports = set()
    for file_path, file_imports in imports.items():
        for imp in file_imports:
            statement = imp.get('statement', '')
            # Extract module name
            if statement.startswith('from '):
                module = statement.split(' import ')[0].replace('from ', '')
            else:
                module = statement.replace('import ', '').split(' as ')[0].split(',')[0]
            
            module = module.strip()
            if module and not module.startswith('.'):
                all_imports.add(module)
    
    if all_imports:
        gen.add_list(sorted(all_imports))
    else:
        gen.add_paragraph('*No external dependencies detected*')
    
    return gen.get_content()


def generate_full_documentation(repo_name: str, repo_info: Dict, readme_summary: str,
                               file_tree: Dict, code_analysis: Dict, imports: Dict) -> str:
    """
    Generate complete documentation.
    
    Args:
        repo_name: Repository name
        repo_info: Repository metadata
        readme_summary: README summary
        file_tree: File tree structure
        code_analysis: Code analysis results
        imports: Import information
        
    Returns:
        Complete markdown documentation
    """
    doc = ''
    
    doc += generate_project_overview(repo_name, repo_info, readme_summary)
    doc += '\n'
    doc += generate_file_structure(file_tree)
    doc += '\n'
    doc += generate_dependencies(imports)
    doc += '\n'
    doc += generate_api_reference(code_analysis)
    
    # Footer
    doc += '\n---\n'
    doc += f'*Documentation generated automatically by Codebase Genius*\n'
    
    return doc


def save_documentation(content: str, output_path: str) -> bool:
    """
    Save documentation to file.
    
    Args:
        content: Markdown content
        output_path: Output file path
        
    Returns:
        Success flag
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Documentation saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving documentation: {e}")
        return False
