"""
Code Analyzer Agent - Performs deeper code analysis and builds Code Context Graph
Constructs relationships between functions, classes, and modules
"""

import:py from helpers.parser_utils:CodeParser, analyze_code_relationships;
import:py from helpers.file_utils:read_file_safe, get_file_list;
import json;

# ===== Node Definitions =====

node code_context_graph {
    has repo_path: str;
    has analysis_status: str = "pending";
    has total_entities: int = 0;
    has relationships: dict;
    has module_graph: dict;
    has error: str = null;
}

node module {
    has path: str;
    has name: str;
    has file_type: str;
    has entity_count: int = 0;
    has dependency_count: int = 0;
    has imports: list;
    has exports: list;
}

node function_def {
    has name: str;
    has module: str;
    has line_number: int;
    has parameters: list;
    has return_type: str;
    has docstring: str;
    has complexity: int = 1;
}

node class_def {
    has name: str;
    has module: str;
    has line_number: int;
    has base_classes: list;
    has methods: list;
    has docstring: str;
}

# ===== Edge Definitions =====

edge calls;
edge inherits_from;
edge imports;
edge defines;
edge contains;

# ===== Walker: Module Analyzer =====

walker module_analyzer {
    can analyze_module;
    
    init(repo_path: str) {
        analyze_module(repo_path);
    }
    
    analyze_module(repo_path: str) {
        parser = CodeParser();
        python_files = get_file_list(repo_path, extensions=['.py']);
        
        for file_path in python_files {
            result = parser.parse_python_file(file_path);
            
            if result != null {
                mod = module(
                    path=file_path,
                    name=extract_module_name(file_path),
                    file_type='python'
                );
                
                # Register imports
                imports = result.get('imports', []);
                mod.imports = [imp['statement'] for imp in imports];
                mod.dependency_count = len(imports);
                
                # Create function definitions
                for func in result.get('functions', []) {
                    func_def = function_def(
                        name=func['name'],
                        module=file_path,
                        line_number=func['line'],
                        parameters=func.get('params', [])
                    );
                    mod -->defines--> func_def;
                }
                
                # Create class definitions
                for cls in result.get('classes', []) {
                    class_def = class_def(
                        name=cls['name'],
                        module=file_path,
                        line_number=cls['line'],
                        base_classes=cls.get('bases', [])
                    );
                    mod -->defines--> class_def;
                }
                
                mod.entity_count = len(result.get('functions', [])) + len(result.get('classes', []));
                here -->contains--> mod;
            }
        }
    }
}

# ===== Walker: Relationship Builder =====

walker relationship_builder {
    can build_relationships;
    
    init() {
        build_relationships();
    }
    
    build_relationships() {
        # Traverse all modules and identify relationships
        # This is a simplified version - in production would use AST analysis
        
        traverse_root = visitor(root=root) {
            if "module" in type(here) {
                # Build import relationships
                for import_stmt in here.imports {
                    # Parse import and create relationship
                }
                
                # Analyze calls between functions
                # This would require more sophisticated parsing
            }
        }
    }
}

# ===== Walker: Complexity Analyzer =====

walker complexity_analyzer {
    can analyze_complexity;
    
    init() {
        analyze_complexity();
    }
    
    analyze_complexity() {
        # Calculate cyclomatic complexity for functions
        # Traverse all function definitions
        
        visitor(root=root) {
            if "function_def" in type(here) {
                # Simplified complexity calculation
                # In production, would analyze control flow
                here.complexity = estimate_complexity(here);
            }
        }
    }
}

# ===== Helper Functions =====

ability extract_module_name(file_path: str) -> str {
    parts = file_path.split('/');
    return parts[-1].replace('.py', '').replace('.jac', '');
}

ability estimate_complexity(func: object) -> int {
    # Simplified cyclomatic complexity estimation
    # Would be more sophisticated with actual AST analysis
    return 1;
}

ability build_context_relationships(modules: list) -> dict {
    relationships = {
        'imports': {},
        'calls': {},
        'inheritance': {},
        'dependencies': {}
    };
    
    for module in modules {
        relationships['imports'][module.name] = module.imports;
        relationships['dependencies'][module.name] = module.dependency_count;
    }
    
    return relationships;
}

# ===== Main Graph Builder =====

walker ccg_builder {
    can build_code_context_graph;
    
    init(repo_path: str) {
        build_code_context_graph(repo_path);
    }
    
    build_code_context_graph(repo_path: str) {
        # Create CCG root node
        ccg = code_context_graph(
            repo_path=repo_path,
            analysis_status="analyzing"
        );
        
        # Analyze modules
        analyzer = module_analyzer(repo_path=repo_path);
        
        # Build relationships
        rel_builder = relationship_builder();
        
        # Analyze complexity
        complexity_analyzer();
        
        ccg.analysis_status = "completed";
    }
}
