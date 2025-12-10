"""
Git utilities for cloning and managing repositories.
"""
import os
import shutil
import tempfile
import subprocess
from typing import Dict, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def clone_repository(repo_url: str, target_dir: str = None) -> Tuple[str, bool]:
    """
    Clone a GitHub repository to a temporary or specified directory.
    
    Args:
        repo_url: GitHub repository URL
        target_dir: Optional target directory. If None, uses temp directory.
        
    Returns:
        Tuple of (directory_path, success_flag)
    """
    try:
        # Validate URL format
        if not isinstance(repo_url, str) or not repo_url.startswith(('http://', 'https://')):
            return None, False
        
        if target_dir is None:
            target_dir = tempfile.mkdtemp(prefix='repo_')
        else:
            os.makedirs(target_dir, exist_ok=True)
        
        logger.info(f"Cloning repository from {repo_url}")
        result = subprocess.run(
            ['git', 'clone', repo_url, target_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            logger.info(f"Successfully cloned to {target_dir}")
            return target_dir, True
        else:
            logger.error(f"Clone failed: {result.stderr}")
            return None, False
            
    except Exception as e:
        logger.error(f"Error cloning repository: {str(e)}")
        return None, False


def get_repo_info(repo_path: str) -> Dict:
    """
    Extract repository metadata.
    
    Args:
        repo_path: Path to the cloned repository
        
    Returns:
        Dictionary with repo metadata
    """
    try:
        result = subprocess.run(
            ['git', 'remote', '-v'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        remote_url = None
        if result.stdout:
            remote_url = result.stdout.split('\n')[0].split('\t')[1].split(' ')[0]
        
        # Get latest commit info
        commit_result = subprocess.run(
            ['git', 'log', '-1', '--format=%H|%an|%ae|%ai|%s'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        commit_info = {}
        if commit_result.stdout:
            parts = commit_result.stdout.strip().split('|')
            commit_info = {
                'hash': parts[0] if len(parts) > 0 else None,
                'author': parts[1] if len(parts) > 1 else None,
                'email': parts[2] if len(parts) > 2 else None,
                'date': parts[3] if len(parts) > 3 else None,
                'message': parts[4] if len(parts) > 4 else None,
            }
        
        return {
            'remote_url': remote_url,
            'latest_commit': commit_info,
            'path': repo_path
        }
    except Exception as e:
        logger.error(f"Error getting repo info: {str(e)}")
        return {'error': str(e)}


def cleanup_repo(repo_path: str) -> bool:
    """
    Clean up a cloned repository.
    
    Args:
        repo_path: Path to the repository to delete
        
    Returns:
        Success flag
    """
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            logger.info(f"Cleaned up {repo_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error cleaning up repo: {str(e)}")
        return False
