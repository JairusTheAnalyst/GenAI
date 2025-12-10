# Codebase Genius 🧠

An AI-powered, multi-agent system that automatically generates high-quality documentation for any software repository.

## Overview

Codebase Genius uses a team of specialized AI agents to analyze your codebase and produce comprehensive, well-organized documentation with:

- 📋 **Automatic README summarization**
- 🗂️ **Project structure mapping**
- 🔍 **Code analysis and relationship detection**
- 📊 **Architecture diagrams (Mermaid format)**
- 🔧 **API reference generation**
- 📦 **Dependency tracking**
- 💾 **Multiple export formats (Markdown, HTML)**

## Quick Start

### Prerequisites

- Python 3.8+
- Git
- Jac runtime
- (Optional) API keys for Gemini (for enhanced analysis)

### Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/agentic_codebase_genius.git
cd agentic_codebase_genius

# Create main virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the System

#### Backend (Jac Server)

```bash
cd BE
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Start the Jac server
jac serve main.jac
```

The backend will be available at `http://localhost:8000`

#### Frontend (Streamlit UI)

In a new terminal:

```bash
cd FE
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the Streamlit app
streamlit run app.py
```

The frontend will open in your browser at `http://localhost:8501`

### Generate Documentation

1. Go to the Streamlit interface
2. Enter a GitHub repository URL (must be public)
3. Click "Generate Documentation"
4. Wait for analysis to complete
5. Download the generated markdown or HTML

## System Architecture

### Multi-Agent Pipeline

```
                    ┌─────────────────────────┐
                    │  Code Genius (Supervisor) │
                    │   Orchestrates Workflow   │
                    └────────┬──────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌──────────┐        ┌──────────┐      ┌──────────┐
    │   Repo   │        │   Code   │      │   Doc    │
    │  Mapper  │        │ Analyzer │      │  Genie   │
    └──────────┘        └──────────┘      └──────────┘
         │                   │                   │
    • Clone repo         • Parse code        • Generate MD
    • File tree          • Extract functions • Create diagrams
    • README summary     • Build CCG         • Format output
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ▼─────────────────▼
                   Markdown Documentation
                   + Mermaid Diagrams
```

### Component Details

#### 1. Code Genius Supervisor (`BE/main.jac`)
- Orchestrates the entire workflow
- Manages agent communication
- Handles error recovery
- Produces execution logs

#### 2. Repo Mapper (`BE/repo_mapper.jac`)
- Clones repositories from GitHub
- Builds file tree representations
- Extracts and summarizes README files
- Identifies project metadata

#### 3. Code Analyzer (`BE/code_analyzer.jac`)
- Parses source files (Python, Jac, JS, etc.)
- Builds Code Context Graph (CCG)
- Extracts functions, classes, dependencies
- Analyzes code complexity

#### 4. DocGenie (`BE/doc_genie.jac`)
- Synthesizes analysis into markdown
- Generates architecture diagrams
- Creates API reference sections
- Produces human-readable documentation

### Supporting Python Modules (`helpers/`)

- **`git_utils.py`**: Repository cloning and management
- **`file_utils.py`**: File tree traversal and reading
- **`parser_utils.py`**: Code parsing with Tree-sitter
- **`doc_utils.py`**: Markdown generation and formatting

## Project Structure

```
agentic_codebase_genius/
├── BE/                          # Backend (Jac agents)
│   ├── main.jac                # Supervisor agent
│   ├── repo_mapper.jac         # Repository mapping
│   ├── code_analyzer.jac       # Code analysis
│   ├── doc_genie.jac           # Documentation generation
│   ├── README.md               # Backend documentation
│   └── requirements.txt
│
├── FE/                          # Frontend (Streamlit)
│   ├── app.py                  # Streamlit interface
│   ├── README.md               # Frontend documentation
│   └── requirements.txt
│
├── helpers/                     # Python utilities
│   ├── __init__.py
│   ├── git_utils.py           # Git operations
│   ├── file_utils.py          # File utilities
│   ├── parser_utils.py        # Code parsing
│   └── doc_utils.py           # Documentation generation
│
├── outputs/                     # Generated documentation
│   └── {repo-name}/
│       └── documentation.md
│
├── requirements.txt             # Root dependencies
├── .env.example                # Environment template
├── README.md                   # This file
└── LICENSE
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Gemini API (for enhanced analysis)
GEMINI_API_KEY=your_api_key_here

# GitHub (optional, for private repos)
GITHUB_TOKEN=your_token_here

# System paths
TEMP_REPO_DIR=./temp_repos
OUTPUT_DIR=./outputs

# Model settings
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=2000

# Limits
MAX_FILE_SIZE=100000
MAX_REPO_SIZE=500000000
```

## Usage Examples

### Example 1: Analyze a Python Project

```bash
# Backend already running...

# Via Streamlit UI:
# 1. Enter: https://github.com/example/python-project
# 2. Click "Generate Documentation"
# 3. Download the markdown

# Result: ./outputs/python-project/documentation.md
```

### Example 2: Analyze a Jac Project

```bash
# Same process, works with any public GitHub repo
# Supports: Python, Jac, JavaScript, TypeScript, Java, C++, Go, Rust
```

### Example 3: Using the API Directly

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/example/repo",
    "output_dir": "./outputs"
  }'
```

## Supported Languages

- ✅ **Python** - Full support (functions, classes, imports)
- ✅ **Jac** - Full support (primary language)
- ⚠️ **JavaScript/TypeScript** - Basic parsing
- ⚠️ **Java** - Basic parsing
- ⚠️ **C/C++** - Basic parsing
- ⚠️ **Go** - Basic parsing
- ⚠️ **Rust** - Basic parsing

## Features

### Repository Analysis

- [x] Clone public repositories
- [x] Ignore standard directories (.git, node_modules, etc.)
- [x] Extract project metadata
- [x] Summarize README files
- [x] Detect entry points (main.py, app.py, etc.)

### Code Analysis

- [x] Parse source files
- [x] Extract function definitions
- [x] Extract class definitions
- [x] Track imports and dependencies
- [x] Build code relationship graphs
- [x] Calculate basic complexity metrics

### Documentation Generation

- [x] Auto-formatted markdown
- [x] Project overview section
- [x] File structure visualization
- [x] API reference section
- [x] Dependency list
- [x] Mermaid architecture diagrams
- [x] Multiple export formats

### User Interface

- [x] Web-based Streamlit interface
- [x] Real-time progress updates
- [x] Tab-based documentation preview
- [x] Download buttons for exports
- [x] Configuration panel
- [x] Error handling and messages

## API Reference

### POST /api/generate

Generates documentation for a repository.

**Request:**
```json
{
  "repo_url": "https://github.com/username/repository",
  "output_dir": "./outputs"
}
```

**Response:**
```json
{
  "status": "success",
  "repo_name": "repository",
  "output_path": "./outputs/repository/documentation.md",
  "progress": 100,
  "workflow_log": [
    {
      "timestamp": "2024-01-01T00:00:00Z",
      "message": "Workflow starting"
    }
  ]
}
```

## Performance

### Benchmarks

- Typical Python project (50 files): ~30-45 seconds
- Small Jac project (20 files): ~15-20 seconds
- Large repository (100+ files): ~60-120 seconds

### Optimization Tips

- Configure `MAX_FILE_SIZE` for large projects
- Increase `MAX_TOKENS` for more detailed analysis
- Adjust `TEMPERATURE` for consistency vs creativity

## Troubleshooting

### Backend Issues

**Error: "Failed to clone repository"**
- Verify GitHub URL is correct and public
- Check internet connectivity
- For private repos, set `GITHUB_TOKEN`

**Error: "Tree-sitter parser not found"**
- Install: `pip install tree-sitter tree-sitter-python`
- System falls back to basic parsing if unavailable

**Error: "Jac server won't start"**
- Verify Jac installation: `jac --version`
- Check port 8000 is available
- Run with verbose logging: `jac serve main.jac -v`

### Frontend Issues

**Error: "Connection refused"**
- Verify backend is running
- Check host and port settings
- Verify firewall allows the port

**Error: "Module not found"**
- Activate virtual environment
- Run: `pip install -r requirements.txt`
- Restart Streamlit

**Slow performance**
- Check backend processing in logs
- Verify internet connectivity
- Consider reducing file analysis scope

## Extending the System

### Add Support for New Language

1. Extend `helpers/parser_utils.py`:
```python
def parse_rust_file(file_path: str) -> Dict:
    # Implementation
    pass
```

2. Update `code_analyzer.jac`:
```jac
walker rust_analyzer {
    can analyze_rust;
}
```

### Add Custom Analysis

Create new walker in `BE/custom_analyzer.jac`:
```jac
walker security_analyzer {
    can check_vulnerabilities;
}
```

### Customize Documentation Template

Edit section generation in `doc_genie.jac`:
```jac
ability custom_template() -> str {
    // Your markdown template
}
```

## Known Limitations

- Limited to 30 files per analysis (prevents timeout)
- Simplified cyclomatic complexity calculation
- No private repository support yet
- Basic type annotation extraction
- Limited to publicly accessible repositories

## Future Roadmap

- [ ] Full AST-based analysis for more languages
- [ ] Incremental analysis for large repos
- [ ] Test coverage metrics
- [ ] Performance profiling integration
- [ ] Type annotation extraction
- [ ] Docstring AI enhancement
- [ ] Interactive graph visualization
- [ ] IDE plugin integration
- [ ] CI/CD pipeline integration
- [ ] Private repository support

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/agentic_codebase_genius.git
cd agentic_codebase_genius

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -r requirements.txt
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Citation

If you use Codebase Genius in your research or projects:

```bibtex
@software{codebase_genius_2024,
  title={Codebase Genius: AI-Powered Code Documentation System},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/agentic_codebase_genius}
}
```

## Support

- 📚 [Backend Documentation](BE/README.md)
- 🎨 [Frontend Documentation](FE/README.md)
- 🐛 [Report Issues](https://github.com/yourusername/agentic_codebase_genius/issues)
- 💬 [Discussions](https://github.com/yourusername/agentic_codebase_genius/discussions)

## Acknowledgments

- Built with [Jac/JacLang](https://jaseci.org/)
- Uses [Streamlit](https://streamlit.io/) for frontend
- Code parsing with [Tree-sitter](https://tree-sitter.github.io/tree-sitter/)
- LLM integration with [Google Gemini](https://ai.google.dev/)

## Contact

For questions or feedback:
- Open an issue on GitHub
- Start a discussion
- Email: your-email@example.com

---

<div align="center">

**⭐ Star us on GitHub if you find this helpful!**

Made with 💜 by the Codebase Genius team

</div>
