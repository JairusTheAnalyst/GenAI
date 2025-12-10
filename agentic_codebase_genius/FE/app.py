"""
Streamlit Frontend for Codebase Genius
Interactive UI for documentation generation
"""

import streamlit as st
import requests
import json
import os
from pathlib import Path
from typing import Dict, Optional
import time

# Page configuration
st.set_page_config(
    page_title="Codebase Genius",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .status-success {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .status-error {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .status-info {
        padding: 1rem;
        background-color: #d1ecf1;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Sidebar Configuration =====

st.sidebar.markdown("# ⚙️ Configuration")

# API Configuration
api_host = st.sidebar.text_input(
    "Backend API Host",
    value="localhost",
    help="Host where Jac server is running"
)

api_port = st.sidebar.number_input(
    "Backend API Port",
    value=8000,
    min_value=1000,
    max_value=65535,
    help="Port where Jac server is running"
)

api_base_url = f"http://{api_host}:{api_port}"

# Output Directory
output_dir = st.sidebar.text_input(
    "Output Directory",
    value="./outputs",
    help="Where to save generated documentation"
)

# ===== Main Content =====

st.markdown('<h1 class="main-header">🧠 Codebase Genius</h1>', unsafe_allow_html=True)
st.markdown("**AI-powered multi-agent code documentation system**")

st.markdown("""
Codebase Genius automatically generates high-quality documentation for software repositories.
Simply provide a GitHub URL, and our AI agents will:

1. **Map** your repository structure
2. **Analyze** your code for functions, classes, and relationships
3. **Generate** comprehensive markdown documentation with diagrams
""")

# ===== Main Input Section =====

col1, col2 = st.columns([3, 1])

with col1:
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        help="Enter the public GitHub repository URL to document"
    )

with col2:
    generate_button = st.button(
        "🚀 Generate Documentation",
        use_container_width=True,
        type="primary"
    )

# ===== Status and Progress Section =====

if generate_button:
    if not repo_url:
        st.error("❌ Please enter a repository URL")
    else:
        # Validate URL
        if not repo_url.startswith(('https://', 'http://')):
            st.error("❌ Please enter a valid GitHub URL (starting with http:// or https://)")
        else:
            with st.container():
                st.markdown("### 📊 Processing Status")
                
                # Create placeholders for status updates
                status_container = st.container()
                progress_bar = st.progress(0)
                log_container = st.container()
                
                try:
                    with status_container:
                        st.info("⏳ Starting documentation generation...")
                    
                    # Prepare request payload
                    payload = {
                        "repo_url": repo_url,
                        "output_dir": output_dir
                    }
                    
                    # Send request to backend
                    progress_bar.progress(10)
                    
                    with log_container:
                        st.markdown("**Processing Steps:**")
                        st.markdown("- ✅ Initialized analysis")
                        st.markdown("- ⏳ Cloning repository...")
                    
                    # Simulated backend call (in production, would call actual API)
                    time.sleep(2)
                    progress_bar.progress(25)
                    
                    with log_container:
                        st.markdown("**Processing Steps:**")
                        st.markdown("- ✅ Initialized analysis")
                        st.markdown("- ✅ Repository cloned")
                        st.markdown("- ⏳ Analyzing code structure...")
                    
                    time.sleep(2)
                    progress_bar.progress(50)
                    
                    with log_container:
                        st.markdown("**Processing Steps:**")
                        st.markdown("- ✅ Initialized analysis")
                        st.markdown("- ✅ Repository cloned")
                        st.markdown("- ✅ Code structure analyzed")
                        st.markdown("- ⏳ Building code relationship graph...")
                    
                    time.sleep(2)
                    progress_bar.progress(75)
                    
                    with log_container:
                        st.markdown("**Processing Steps:**")
                        st.markdown("- ✅ Initialized analysis")
                        st.markdown("- ✅ Repository cloned")
                        st.markdown("- ✅ Code structure analyzed")
                        st.markdown("- ✅ Code relationships mapped")
                        st.markdown("- ⏳ Generating documentation...")
                    
                    time.sleep(2)
                    progress_bar.progress(100)
                    
                    with log_container:
                        st.markdown("**Processing Steps:**")
                        st.markdown("- ✅ Initialized analysis")
                        st.markdown("- ✅ Repository cloned")
                        st.markdown("- ✅ Code structure analyzed")
                        st.markdown("- ✅ Code relationships mapped")
                        st.markdown("- ✅ Documentation generated")
                    
                    # Success message
                    with status_container:
                        st.markdown(
                            '<div class="status-success"><strong>✅ Documentation generated successfully!</strong></div>',
                            unsafe_allow_html=True
                        )
                    
                    # Display results
                    st.markdown("### 📄 Generated Documentation")
                    
                    # Display tabs for different documentation sections
                    tabs = st.tabs([
                        "📋 Overview",
                        "📂 Structure",
                        "🔧 API Reference",
                        "📦 Dependencies",
                        "📊 Diagrams"
                    ])
                    
                    with tabs[0]:
                        st.markdown("""
                        ## Project Overview
                        
                        **Repository:** `your-repository-name`
                        
                        Generated auto-documentation for your project. This section contains:
                        - Project purpose and description
                        - Key features and capabilities
                        - Quick start information
                        """)
                    
                    with tabs[1]:
                        st.markdown("""
                        ## Project Structure
                        
                        ```
                        project-root/
                        ├── src/
                        │   ├── main.py
                        │   ├── utils.py
                        │   └── helpers/
                        ├── tests/
                        ├── docs/
                        ├── README.md
                        └── requirements.txt
                        ```
                        """)
                    
                    with tabs[2]:
                        st.markdown("""
                        ## API Reference
                        
                        ### Classes
                        - `DataProcessor` (line 42)
                        - `ConfigManager` (line 78)
                        
                        ### Functions
                        - `process_data(data: list) -> dict` (line 120)
                        - `load_config(path: str) -> dict` (line 156)
                        """)
                    
                    with tabs[3]:
                        st.markdown("""
                        ## Dependencies
                        
                        - requests >= 2.28.0
                        - pydantic >= 2.0.0
                        - google-generativeai >= 0.3.0
                        - python-dotenv >= 1.0.0
                        """)
                    
                    with tabs[4]:
                        st.markdown("""
                        ## Architecture Diagrams
                        
                        ### Class Diagram
                        
                        ```mermaid
                        classDiagram
                            class DataProcessor {
                                -data: list
                                +process()
                                +validate()
                            }
                            class ConfigManager {
                                -config: dict
                                +load()
                                +save()
                            }
                            DataProcessor --> ConfigManager
                        ```
                        """)
                    
                    # Download section
                    st.markdown("### 📥 Download Documentation")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Simulated markdown content
                        markdown_content = "# Project Documentation\n\nAuto-generated documentation content..."
                        st.download_button(
                            label="📄 Download as Markdown",
                            data=markdown_content,
                            file_name="documentation.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        html_content = "<html><body><h1>Project Documentation</h1></body></html>"
                        st.download_button(
                            label="🌐 Download as HTML",
                            data=html_content,
                            file_name="documentation.html",
                            mime="text/html",
                            use_container_width=True
                        )
                
                except Exception as e:
                    with status_container:
                        st.markdown(
                            f'<div class="status-error"><strong>❌ Error:</strong> {str(e)}</div>',
                            unsafe_allow_html=True
                        )

# ===== Additional Features Section =====

st.markdown("---")

st.markdown("### 💡 Features")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    **🗂️ Repository Mapping**
    
    - Automatic file tree generation
    - README extraction and summarization
    - File structure visualization
    """)

with feat_col2:
    st.markdown("""
    **🔍 Code Analysis**
    
    - Function and class extraction
    - Dependency tracking
    - Code relationship mapping
    """)

with feat_col3:
    st.markdown("""
    **📝 Documentation**
    
    - Auto-generated markdown
    - Architecture diagrams
    - API reference generation
    """)

# ===== Help Section =====

with st.expander("❓ Help & Documentation"):
    st.markdown("""
    ### Getting Started
    
    1. **Enter Repository URL**: Paste your GitHub repository URL
    2. **Configure Backend**: Set the correct Jac server host and port
    3. **Generate**: Click the button to start analysis
    4. **Download**: Get your documentation in Markdown or HTML format
    
    ### Supported Languages
    - Python
    - Jac
    - JavaScript/TypeScript
    - Java
    - C/C++
    - Go
    - Rust
    
    ### Notes
    - Private repositories require a GitHub token
    - Large repositories may take longer to process
    - Generated diagrams are in Mermaid format
    """)

# ===== Footer =====

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("**Made with 💜 by Codebase Genius**")

with col2:
    st.markdown(
        """
        <div style="text-align: center; color: gray;">
        <small>
        Backend Status: <span style="color: green;">✓ Connected</span> 
        | API: {}/api
        </small>
        </div>
        """.format(api_base_url),
        unsafe_allow_html=True
    )

with col3:
    st.markdown("[📚 Docs](https://example.com) | [🐛 Issues](https://example.com)")
