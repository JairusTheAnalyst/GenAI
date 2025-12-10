"""
File utilities for traversing repositories and reading files.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Common directories to ignore
IGNORE_DIRS = {
    '.git', '.github', '.gitlab', '__pycache__', '.pytest_cache',
    'node_modules', '.venv', 'venv', 'env', '.env', 'dist', 'build',
    '.egg-info', '.tox', '.idea', '.vscode', '.DS_Store', 'vendor',
    '.next', 'out', '.nuxt', 'coverage', '.nyc_output'
}

# Common files to ignore
IGNORE_FILES = {
    '.DS_Store', 'thumbs.db', '*.pyc', '*.pyo', '*.pyd',
    '.env', '.env.local', '.gitignore', '.gitattributes'
}


def should_ignore(path: str, is_dir: bool) -> bool:
    """Check if a path should be ignored during traversal."""
    name = os.path.basename(path)
    if is_dir:
        return name.startswith('.') or name in IGNORE_DIRS
    return name.startswith('.') or name in IGNORE_FILES


def build_file_tree(root_path: str, max_depth: int = 10) -> Dict:
    """
    Build a tree structure of files and directories.
    
    Args:
        root_path: Root directory to start traversal
        max_depth: Maximum depth to traverse
        
    Returns:
        Dictionary representing the file tree
    """
    def traverse(path: str, depth: int = 0) -> Dict:
        if depth > max_depth:
            return {'name': os.path.basename(path), 'type': 'dir', 'children': []}
        
        result = {
            'name': os.path.basename(path) or path,
            'type': 'dir' if os.path.isdir(path) else 'file',
            'path': path
        }
        
        if os.path.isdir(path):
            children = []
            try:
                for item in sorted(os.listdir(path)):
                    item_path = os.path.join(path, item)
                    is_dir = os.path.isdir(item_path)
                    
                    if should_ignore(item_path, is_dir):
                        continue
                    
                    child = traverse(item_path, depth + 1)
                    children.append(child)
            except PermissionError:
                logger.warning(f"Permission denied accessing {path}")
            
            result['children'] = children
        
        return result
    
    try:
        return traverse(root_path)
    except Exception as e:
        logger.error(f"Error building file tree: {str(e)}")
        return {'error': str(e)}


def get_file_list(root_path: str, extensions: Optional[List[str]] = None) -> List[str]:
    """
    Get a flat list of files matching extensions.
    
    Args:
        root_path: Root directory to search
        extensions: List of file extensions to include (e.g., ['.py', '.jac'])
        
    Returns:
        List of file paths
    """
    files = []
    
    try:
        for root, dirs, filenames in os.walk(root_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), True)]
            
            for filename in filenames:
                if should_ignore(os.path.join(root, filename), False):
                    continue
                
                if extensions is None or any(filename.endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
    except Exception as e:
        logger.error(f"Error getting file list: {str(e)}")
    
    return files


def read_file_safe(file_path: str, max_size: int = 1000000) -> Optional[str]:
    """
    Read file contents safely with size limit.
    
    Args:
        file_path: Path to file
        max_size: Maximum file size to read (default 1MB)
        
    Returns:
        File contents or None if error/too large
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return None
        
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            logger.warning(f"File too large: {file_path} ({file_size} bytes)")
            return None
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return None


def get_file_extension(file_path: str) -> str:
    """Get the file extension."""
    return os.path.splitext(file_path)[1]


def is_source_file(file_path: str) -> bool:
    """Check if file is a source code file."""
    source_extensions = {'.py', '.jac', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs'}
    return get_file_extension(file_path) in source_extensions
