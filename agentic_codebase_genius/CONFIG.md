# Configuration Guide for Codebase Genius

This guide explains all configuration options available for Codebase Genius.

## Environment Variables (.env file)

### API Configuration

#### GEMINI_API_KEY (Required)
- **Type:** String
- **Description:** Your Google Gemini API key for code analysis
- **Example:** `GEMINI_API_KEY=AIzaSyDxxx...`
- **Get Key:** https://ai.google.dev/

#### OPENAI_API_KEY (Optional)
- **Type:** String  
- **Description:** Alternative to Gemini for code analysis
- **Example:** `OPENAI_API_KEY=sk-xxx...`
- **Get Key:** https://platform.openai.com/api-keys

#### GITHUB_TOKEN (Optional)
- **Type:** String
- **Description:** GitHub token for accessing private repositories
- **Example:** `GITHUB_TOKEN=ghp_xxxxx...`
- **Get Token:** https://github.com/settings/tokens
- **Scopes:** `repo`, `read:user`

### System Configuration

#### TEMP_REPO_DIR
- **Type:** String (Path)
- **Default:** `./temp_repos`
- **Description:** Directory to clone repositories for analysis
- **Example:** `/tmp/codebase_genius_repos`

#### OUTPUT_DIR
- **Type:** String (Path)
- **Default:** `./outputs`
- **Description:** Directory to save generated documentation
- **Example:** `/home/user/docs`

#### MAX_FILE_SIZE
- **Type:** Integer (bytes)
- **Default:** `100000` (100 KB)
- **Description:** Maximum file size to analyze
- **Range:** 1000 - 10000000
- **Example:** `MAX_FILE_SIZE=50000`

#### MAX_REPO_SIZE
- **Type:** Integer (bytes)
- **Default:** `500000000` (500 MB)
- **Description:** Maximum total repository size
- **Range:** 1000000 - 5000000000
- **Example:** `MAX_REPO_SIZE=1000000000`

### Model Configuration

#### MODEL_NAME
- **Type:** String
- **Default:** `gemini-1.5-pro`
- **Description:** LLM model to use for analysis
- **Options:**
  - `gemini-1.5-pro` - High quality, faster
  - `gemini-1.5-flash` - Balanced performance
  - `gpt-4` - Using OpenAI
  - `gpt-3.5-turbo` - Faster, less detailed

#### TEMPERATURE
- **Type:** Float
- **Default:** `0.7`
- **Range:** 0.0 - 2.0
- **Description:** Controls randomness in output
  - Lower (0.0-0.3): More deterministic
  - Medium (0.5-0.8): Balanced
  - Higher (1.0-2.0): More creative

#### MAX_TOKENS
- **Type:** Integer
- **Default:** `2000`
- **Range:** 100 - 4000
- **Description:** Maximum response length per analysis

### Analysis Configuration

#### SUPPORTED_LANGUAGES
- **Type:** Comma-separated string
- **Default:** `python,jac,javascript,typescript,java,cpp,c,go,rust`
- **Description:** Languages to analyze
- **Example:** `SUPPORTED_LANGUAGES=python,jac,javascript`

#### IGNORE_PATTERNS
- **Type:** Comma-separated string
- **Default:** `.git,.pytest_cache,__pycache__,node_modules,.venv,venv`
- **Description:** Patterns to ignore during analysis
- **Example:** `IGNORE_PATTERNS=.git,node_modules,dist,build`

#### INCLUDE_PATTERNS
- **Type:** Comma-separated string
- **Default:** `*.py,*.jac,*.js,*.ts,*.md,*.txt`
- **Description:** File patterns to include
- **Example:** `INCLUDE_PATTERNS=*.py,*.jac`

### Performance Configuration

#### PARALLEL_WORKERS
- **Type:** Integer
- **Default:** `4`
- **Range:** 1 - 16
- **Description:** Number of parallel analysis workers
- **Higher = Faster but uses more memory**

#### TIMEOUT_SECONDS
- **Type:** Integer
- **Default:** `300` (5 minutes)
- **Range:** 10 - 3600
- **Description:** Timeout for repository operations

#### CACHE_ENABLED
- **Type:** Boolean
- **Default:** `true`
- **Description:** Enable caching of analysis results
- **Options:** `true`, `false`

### Output Configuration

#### OUTPUT_FORMAT
- **Type:** String
- **Default:** `markdown`
- **Description:** Output documentation format
- **Options:** `markdown`, `html`, `pdf`

#### INCLUDE_DIAGRAMS
- **Type:** Boolean
- **Default:** `true`
- **Description:** Include Mermaid diagrams in output

#### INCLUDE_CODE_SNIPPETS
- **Type:** Boolean
- **Default:** `true`
- **Description:** Include code examples in documentation

#### DIAGRAM_FORMAT
- **Type:** String
- **Default:** `mermaid`
- **Description:** Diagram rendering format
- **Options:** `mermaid`, `plantuml`, `graphviz`

### Server Configuration

#### JAC_SERVER_HOST
- **Type:** String
- **Default:** `localhost`
- **Description:** Jac server host address
- **Example:** `0.0.0.0` (to accept external connections)

#### JAC_SERVER_PORT
- **Type:** Integer
- **Default:** `8000`
- **Range:** 1000 - 65535
- **Description:** Jac server port

#### STREAMLIT_SERVER_PORT
- **Type:** Integer
- **Default:** `8501`
- **Range:** 1000 - 65535
- **Description:** Streamlit frontend port

## Configuration Examples

### Minimal Setup

```dotenv
# Minimal configuration (just API key)
GEMINI_API_KEY=your_key_here
```

### Production Setup

```dotenv
# Complete production configuration
GEMINI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here

# System paths
TEMP_REPO_DIR=/var/tmp/codebase_genius
OUTPUT_DIR=/var/www/docs

# Performance
PARALLEL_WORKERS=8
TIMEOUT_SECONDS=600
CACHE_ENABLED=true

# Analysis
MAX_FILE_SIZE=500000
MAX_REPO_SIZE=1000000000
SUPPORTED_LANGUAGES=python,jac,javascript

# Output
OUTPUT_FORMAT=markdown
INCLUDE_DIAGRAMS=true
INCLUDE_CODE_SNIPPETS=true
DIAGRAM_FORMAT=mermaid

# Server
JAC_SERVER_HOST=0.0.0.0
JAC_SERVER_PORT=8000
```

### Development Setup

```dotenv
# Development configuration
GEMINI_API_KEY=your_key_here

# Use local temp directory
TEMP_REPO_DIR=./temp_repos
OUTPUT_DIR=./outputs

# Faster, less detailed analysis
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.5
MAX_TOKENS=1000

# Performance
PARALLEL_WORKERS=2
CACHE_ENABLED=true

# Output
INCLUDE_DIAGRAMS=true
DIAGRAM_FORMAT=mermaid
```

### High-Performance Setup

```dotenv
# For analyzing large repositories
GEMINI_API_KEY=your_key_here

# External storage
TEMP_REPO_DIR=/fast_storage/repos
OUTPUT_DIR=/fast_storage/docs

# More workers
PARALLEL_WORKERS=16
TIMEOUT_SECONDS=1800

# Higher limits
MAX_FILE_SIZE=1000000
MAX_REPO_SIZE=2000000000

# Detailed analysis
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=4000

# Cache enabled
CACHE_ENABLED=true
```

## Configuration Validation

Check your configuration is valid:

```bash
# Test configuration loading
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Config valid:', os.getenv('GEMINI_API_KEY') is not None)"

# List all environment variables
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); [print(f'{k}={v}') for k,v in os.environ.items() if 'GEMINI' in k or 'OUTPUT' in k]"
```

## Environment Variable Precedence

Variables are loaded in this order (later overrides earlier):
1. Default values in code
2. `.env.example` file
3. `.env` file
4. System environment variables
5. Command-line arguments

## Tips & Best Practices

1. **Never commit .env** - Add to .gitignore
2. **Use .env.example** - Share template, not secrets
3. **Test after changes** - Verify with configuration validation
4. **Use appropriate limits** - Match your system resources
5. **Enable caching** - For repeated analyses
6. **Monitor parallelism** - More workers = more memory usage
7. **Set reasonable timeouts** - Prevent hanging processes

---

For more help, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)
