"""
Repo Mapper Agent - Handles repository analysis and initial exploration
Clones repository and builds high-level understanding of codebase structure
"""

import:py from helpers.file_utils:build_file_tree, get_file_list, read_file_safe;
import:py from helpers.git_utils:clone_repository, get_repo_info, cleanup_repo;
import:py from helpers.parser_utils:CodeParser;
import json;

# ===== Node Definitions =====

node repo_map_node {
    has repo_url: str;
    has repo_path: str;
    has repo_name: str;
    has file_tree: dict;
    has readme_content: str;
    has readme_summary: str;
    has source_files: list;
    has status: str = "pending";
    has error: str = null;
    has metadata: dict;
}

node file_info {
    has path: str;
    has name: str;
    has extension: str;
    has size: int;
    has content_preview: str;
}

node code_entity {
    has name: str;
    has type: str;  # 'function', 'class', 'module'
    has file_path: str;
    has line_number: int;
    has description: str;
}

# ===== Edge Definitions =====

edge contains_file;
edge contains_entity;
edge imports_from;

# ===== Walker: Repository Cloner =====

walker repo_cloner {
    can clone_and_analyze;
    
    init(repo_url: str) {
        clone_and_analyze(repo_url);
    }
    
    clone_and_analyze(repo_url: str) {
        (path, success) = clone_repository(repo_url);
        
        if success {
            repo_info = get_repo_info(path);
            repo_name = repo_info.get('remote_url', repo_url).split('/')[-1].replace('.git', '');
            
            visit_node = repo_map_node(
                repo_url=repo_url,
                repo_path=path,
                repo_name=repo_name,
                status="cloned",
                metadata=repo_info
            );
        } else {
            visit_node = repo_map_node(
                repo_url=repo_url,
                status="failed",
                error="Failed to clone repository"
            );
        }
    }
}

# ===== Walker: File Tree Builder =====

walker file_tree_builder {
    can build_tree, extract_readme;
    
    init(node_id: str) {
        build_tree(node_id);
        extract_readme(node_id);
    }
    
    build_tree(node_id: str) {
        # Build comprehensive file tree
        repo_path = here.repo_path;
        tree = build_file_tree(repo_path);
        here.file_tree = tree;
        
        # Get all source files
        source_files = get_file_list(repo_path, extensions=['.py', '.jac', '.js', '.ts']);
        here.source_files = source_files;
    }
    
    extract_readme(node_id: str) {
        repo_path = here.repo_path;
        
        # Look for README files
        readme_files = ['.md', '.rst', '.txt'];
        readme_content = null;
        
        for readme_name in ['README.md', 'readme.md', 'README.rst', 'README.txt'] {
            readme_path = repo_path + '/' + readme_name;
            content = read_file_safe(readme_path, max_size=10000);
            if content != null {
                readme_content = content;
                break;
            }
        }
        
        here.readme_content = readme_content;
        
        # Summarize README
        if readme_content != null {
            here.readme_summary = summarize_readme(readme_content);
        }
    }
}

# ===== Walker: Source File Analyzer =====

walker source_analyzer {
    can analyze_sources;
    
    init(node_id: str) {
        analyze_sources(node_id);
    }
    
    analyze_sources(node_id: str) {
        source_files = here.source_files;
        parser = CodeParser();
        
        for file_path in source_files[0:20] {  # Analyze first 20 files
            if file_path.endswith('.py') {
                result = parser.parse_python_file(file_path);
                
                if result != null {
                    # Create file info node
                    file_node = file_info(
                        path=file_path,
                        name=file_path.split('/')[-1],
                        extension='.py'
                    );
                    
                    # Create entities
                    for func in result.get('functions', []) {
                        entity = code_entity(
                            name=func['name'],
                            type='function',
                            file_path=file_path,
                            line_number=func['line']
                        );
                        file_node -->contains_entity--> entity;
                    }
                    
                    for cls in result.get('classes', []) {
                        entity = code_entity(
                            name=cls['name'],
                            type='class',
                            file_path=file_path,
                            line_number=cls['line']
                        );
                        file_node -->contains_entity--> entity;
                    }
                    
                    here -->contains_file--> file_node;
                }
            }
        }
        
        here.status = "analyzed";
    }
}

# ===== Helper Functions =====

ability summarize_readme(content: str) -> str {
    # Simple summarization - extract first few paragraphs
    paragraphs = content.split('\n\n');
    summary = paragraphs[0] if len(paragraphs) > 0 else content[:500];
    return summary[:500];  # Limit to 500 chars
}

# ===== Main Graph Builder =====

walker main {
    can create_repo_analysis;
    
    init(repo_url: str) {
        create_repo_analysis(repo_url);
    }
    
    create_repo_analysis(repo_url: str) {
        # Create root node
        root = repo_map_node(
            repo_url=repo_url,
            status="initializing"
        );
        
        # Clone repository
        cloner = repo_cloner(repo_url=repo_url);
        
        # Build file tree
        builder = file_tree_builder();
        
        # Analyze sources
        analyzer = source_analyzer();
    }
}
