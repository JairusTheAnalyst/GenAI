# Codebase Genius - Backend (Jac)

The backend is built with **Jac** (JacLang) and implements the core multi-agent system for analyzing repositories and generating documentation.

## Architecture

The backend consists of four main agents:

### 1. **Code Genius (Supervisor)** - `main.jac`
- Orchestrates the entire workflow
- Manages communication between agents
- Handles error recovery and logging
- Implements high-level decision making

### 2. **Repo Mapper** - `repo_mapper.jac`
- Clones GitHub repositories
- Builds file tree representations
- Extracts and summarizes README files
- Identifies key entry points and configuration files

### 3. **Code Analyzer** - `code_analyzer.jac`
- Parses source code (Python, Jac, etc.)
- Builds Code Context Graph (CCG) showing relationships
- Extracts functions, classes, and their dependencies
- Analyzes code complexity and structure

### 4. **DocGenie** - `doc_genie.jac`
- Synthesizes analysis results into markdown
- Generates architecture diagrams (Mermaid format)
- Creates API reference sections
- Produces human-readable documentation

## File Structure

```
BE/
├── main.jac              # Supervisor agent (entry point)
├── repo_mapper.jac       # Repository analysis
├── code_analyzer.jac     # Code parsing and CCG
└── doc_genie.jac         # Documentation generation
```

## Prerequisites

- Python 3.8+
- Jac runtime (JacLang)
- Git (for cloning repositories)

## Setup

### 1. Create Virtual Environment

```bash
cd BE
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GITHUB_TOKEN`: (Optional) For private repositories

### 4. Install Jac

```bash
pip install jaclang
```

## Running the Backend

### Start Jac Server

```bash
jac serve main.jac
```

The server will start on `localhost:8000` by default.

### API Endpoint

Send a POST request to generate documentation:

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/username/repository",
    "output_dir": "./outputs"
  }'
```

### Expected Response

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

## Agent Workflow

```
┌─────────────────────┐
│  Code Genius (Sup)  │
│   (Orchestrates)    │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
    ▼             ▼          ▼          ▼
┌────────┐  ┌──────────┐ ┌────────┐ ┌──────────┐
│ Clone  │  │Repo Map  │ │Analyze │ │Generate  │
│ Repo   │  │ Structure│ │ Code   │ │ Doc      │
└────────┘  └──────────┘ └────────┘ └──────────┘
    │             │          │          │
    └─────────────┴──────────┴──────────┘
                  │
            ▼─────────────▼
        Markdown + Diagrams
```

## Extending the System

### Add Support for New Languages

1. Extend `code_analyzer.jac`:
   ```jac
   walker language_analyzer {
       can analyze_java_file, analyze_go_file;
   }
   ```

2. Add parser in `helpers/parser_utils.py`:
   ```python
   def parse_java_file(file_path: str) -> Dict:
       # Implementation
   ```

### Add Custom Analysis

Create a new walker in a dedicated `.jac` file:

```jac
walker custom_analyzer {
    can analyze_metrics;
    
    init() {
        analyze_metrics();
    }
    
    analyze_metrics() {
        # Your analysis logic
    }
}
```

## Configuration Options

In `.env`:

```env
# Model Configuration
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=2000

# System Configuration
TEMP_REPO_DIR=./temp_repos
OUTPUT_DIR=./outputs
MAX_FILE_SIZE=100000
MAX_REPO_SIZE=500000000
```

## Troubleshooting

### "Failed to clone repository"
- Verify the GitHub URL is correct and public
- Check your internet connection
- For private repos, ensure `GITHUB_TOKEN` is set

### "Tree-sitter parser not found"
- Install tree-sitter: `pip install tree-sitter`
- The system falls back to basic parsing if unavailable

### Jac Server Won't Start
- Ensure Jac is properly installed: `jac --version`
- Check port 8000 is not in use
- Run with verbose logging: `jac serve main.jac -v`

## Performance Tips

- **Limit file analysis**: Currently analyzes first 30 files to prevent timeout
- **Use caching**: Generated file trees are cached where possible
- **Cleanup temp repos**: Temporary clones are automatically deleted

## API Reference

### Walkers

#### `code_genius`
Main orchestrator walker

**Parameters:**
- `repo_url` (str): GitHub repository URL
- `output_dir` (str): Output directory path

**Outputs:**
- Complete markdown documentation
- Workflow logs
- Status updates

#### `clone_repo`
Clones a repository

**Parameters:**
- `repo_url` (str): Repository URL

#### `map_repository`
Builds file tree and extracts README

**Parameters:**
- `repo_path` (str): Path to cloned repo

#### `analyze_code`
Analyzes source files

**Parameters:**
- `repo_path` (str): Path to cloned repo

#### `generate_documentation`
Generates markdown documentation

**Parameters:**
- `repo_name` (str): Repository name
- `analysis` (dict): Analysis results
- `output_dir` (str): Output directory

## Limitations & Future Work

### Current Limitations
- Python/Jac analysis most complete
- Limited to 30 files per repo (to prevent timeouts)
- No support for private repositories yet
- Cyclomatic complexity analysis is simplified

### Future Enhancements
- [ ] Full AST-based analysis for Java, Go, Rust
- [ ] Incremental analysis for large repos
- [ ] Test coverage metrics
- [ ] Performance profiling
- [ ] Type annotation extraction
- [ ] Docstring AI enhancement
- [ ] Interactive graph visualization
- [ ] Integration with code review tools

## Contributing

1. Test your changes locally: `jac serve main.jac`
2. Ensure all walkers are documented with docstrings
3. Follow Jac language conventions
4. Add test cases for new functionality

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a detailed bug report
3. Include relevant `.jac` files and error logs

---

**Happy documenting! 🎉**
