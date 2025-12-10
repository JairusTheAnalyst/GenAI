"""
Doc Genie Agent - Synthesizes documentation from analyzed code
Converts structured data into well-organized markdown documents
"""

import:py from helpers.doc_utils:generate_full_documentation, save_documentation;
import:py from helpers.doc_utils:MarkdownGenerator, generate_project_overview, generate_file_structure;
import:py from helpers.doc_utils:generate_api_reference, generate_dependencies;
import json;

# ===== Node Definitions =====

node documentation {
    has repo_name: str;
    has output_path: str;
    has content: str;
    has status: str = "pending";
    has sections: list;
    has generation_time: float;
    has error: str = null;
}

node doc_section {
    has title: str;
    has section_type: str;  # 'overview', 'structure', 'api', 'examples', etc.
    has content: str;
    has order: int;
}

node diagram {
    has diagram_type: str;  # 'class', 'sequence', 'dependency'
    has description: str;
    has mermaid_code: str;
    has title: str;
}

# ===== Edge Definitions =====

edge section_of;
edge includes_diagram;

# ===== Walker: Documentation Generator =====

walker doc_generator {
    can generate_overview, generate_structure, generate_api_ref;
    can generate_dependencies_sec, generate_examples;
    
    init(repo_name: str, repo_info: dict, file_tree: dict, code_analysis: dict) {
        generate_overview(repo_name, repo_info);
        generate_structure(file_tree);
        generate_api_ref(code_analysis);
        generate_dependencies_sec(code_analysis);
    }
    
    generate_overview(repo_name: str, repo_info: dict) {
        readme_summary = repo_info.get('readme_summary', 'No readme found');
        
        section = doc_section(
            title='Project Overview',
            section_type='overview',
            content=generate_project_overview(repo_name, repo_info, readme_summary),
            order=1
        );
        
        here -->section_of--> section;
    }
    
    generate_structure(file_tree: dict) {
        section = doc_section(
            title='Project Structure',
            section_type='structure',
            content=generate_file_structure(file_tree),
            order=2
        );
        
        here -->section_of--> section;
    }
    
    generate_api_ref(code_analysis: dict) {
        section = doc_section(
            title='API Reference',
            section_type='api',
            content=generate_api_reference(code_analysis),
            order=3
        );
        
        here -->section_of--> section;
    }
    
    generate_dependencies_sec(code_analysis: dict) {
        section = doc_section(
            title='Dependencies',
            section_type='dependencies',
            content=generate_dependencies(code_analysis.get('imports', {})),
            order=4
        );
        
        here -->section_of--> section;
    }
    
    generate_examples() {
        # Generate examples section if applicable
        section = doc_section(
            title='Examples',
            section_type='examples',
            content='# Examples\n\nAdd example usage here.',
            order=5
        );
        
        here -->section_of--> section;
    }
}

# ===== Walker: Diagram Generator =====

walker diagram_generator {
    can generate_class_diagram, generate_dependency_diagram;
    
    init(code_analysis: dict) {
        generate_class_diagram(code_analysis);
        generate_dependency_diagram(code_analysis);
    }
    
    generate_class_diagram(code_analysis: dict) {
        # Generate Mermaid class diagram from code analysis
        mermaid_code = build_class_diagram_mermaid(code_analysis);
        
        if mermaid_code != null {
            diagram = diagram(
                diagram_type='class',
                title='Class Diagram',
                description='Relationships between classes in the codebase',
                mermaid_code=mermaid_code
            );
            
            here -->includes_diagram--> diagram;
        }
    }
    
    generate_dependency_diagram(code_analysis: dict) {
        # Generate dependency graph
        mermaid_code = build_dependency_diagram_mermaid(code_analysis);
        
        if mermaid_code != null {
            diagram = diagram(
                diagram_type='dependency',
                title='Module Dependency Graph',
                description='Dependencies between modules',
                mermaid_code=mermaid_code
            );
            
            here -->includes_diagram--> diagram;
        }
    }
}

# ===== Walker: Final Assembler =====

walker doc_assembler {
    can assemble_documentation, save_to_file;
    
    init(repo_name: str, output_dir: str) {
        assemble_documentation(repo_name);
        save_to_file(repo_name, output_dir);
    }
    
    assemble_documentation(repo_name: str) {
        # Collect all sections
        sections = [];
        
        visitor(root=root) {
            if "doc_section" in type(here) {
                sections.append({
                    'title': here.title,
                    'content': here.content,
                    'order': here.order,
                    'type': here.section_type
                });
            }
        }
        
        # Sort sections by order
        sections.sort(key=lambda x: x['order']);
        
        # Assemble final content
        content = '';
        for section in sections {
            content += section['content'] + '\n';
        }
        
        # Add diagrams if any
        visitor(root=root) {
            if "diagram" in type(here) {
                content += f"\n## {here.title}\n\n";
                content += f"{here.description}\n\n";
                content += "```mermaid\n" + here.mermaid_code + "\n```\n\n";
            }
        }
        
        here.content = content;
        here.sections = sections;
        here.status = "generated";
    }
    
    save_to_file(repo_name: str, output_dir: str) {
        output_path = output_dir + '/' + repo_name + '/documentation.md';
        success = save_documentation(here.content, output_path);
        
        if success {
            here.output_path = output_path;
            here.status = "saved";
        } else {
            here.error = "Failed to save documentation";
            here.status = "failed";
        }
    }
}

# ===== Helper Functions =====

ability build_class_diagram_mermaid(code_analysis: dict) -> str {
    """Generate Mermaid class diagram from code analysis."""
    
    definitions = code_analysis.get('definitions', {});
    
    if len(definitions) == 0 {
        return null;
    }
    
    mermaid = "classDiagram\n";
    
    for file_path, defs in definitions.items() {
        for cls in defs.get('classes', []) {
            class_name = cls['name'];
            mermaid += f"    class {class_name} {{\n";
            mermaid += f"        string name\n";
            mermaid += f"    }}\n";
        }
    }
    
    return mermaid;
}

ability build_dependency_diagram_mermaid(code_analysis: dict) -> str {
    """Generate Mermaid dependency diagram."""
    
    imports = code_analysis.get('imports', {});
    
    if len(imports) == 0 {
        return null;
    }
    
    mermaid = "graph TD\n";
    
    for file_path, file_imports in imports.items() {
        file_name = file_path.split('/')[-1];
        for imp in file_imports {
            mermaid += f"    {file_name} --> {imp['statement']}\n";
        }
    }
    
    return mermaid;
}

ability format_markdown_section(title: str, content: str) -> str {
    """Format a markdown section."""
    return f"# {title}\n\n{content}\n\n";
}

# ===== Main Documentation Builder =====

walker doc_genie {
    can build_documentation;
    
    init(repo_name: str, repo_info: dict, file_tree: dict, 
         code_analysis: dict, output_dir: str) {
        build_documentation(repo_name, repo_info, file_tree, code_analysis, output_dir);
    }
    
    build_documentation(repo_name: str, repo_info: dict, file_tree: dict, 
                       code_analysis: dict, output_dir: str) {
        # Create documentation node
        doc = documentation(
            repo_name=repo_name,
            status="generating"
        );
        
        # Generate documentation sections
        generator = doc_generator(
            repo_name=repo_name,
            repo_info=repo_info,
            file_tree=file_tree,
            code_analysis=code_analysis
        );
        
        # Generate diagrams
        diagram_gen = diagram_generator(code_analysis=code_analysis);
        
        # Assemble final documentation
        assembler = doc_assembler(
            repo_name=repo_name,
            output_dir=output_dir
        );
    }
}
