# Installation & Setup Guide

Complete step-by-step guide to install and run Codebase Genius.

## System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for dependencies and temp files
- **Internet**: Required for cloning GitHub repositories

## Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/agentic_codebase_genius.git
cd agentic_codebase_genius
```

## Step 2: Create Root Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

## Step 3: Install Root Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Setup Backend

### 4.1 Navigate to Backend

```bash
cd BE
```

### 4.2 Create Backend Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 4.3 Install Backend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.4 Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Required: Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Optional: GitHub token for private repos
GITHUB_TOKEN=your_token_here

# System configuration
TEMP_REPO_DIR=./temp_repos
OUTPUT_DIR=./outputs
```

### 4.5 Start Backend Server

```bash
jac serve main.jac
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!**

## Step 5: Setup Frontend

### 5.1 Open New Terminal

Leave backend running and open a new terminal window.

### 5.2 Navigate to Frontend

```bash
cd FE
```

### 5.3 Create Frontend Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 5.4 Install Frontend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.5 Start Frontend

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

If not, visit it manually.

## Step 6: Test the System

1. **In Streamlit UI**:
   - Enter a GitHub URL: `https://github.com/JairusTheAnalyst/Guess_Game1`
   - Click "Generate Documentation"
   - Wait for processing to complete

2. **Expected Output**:
   - Progress bar reaching 100%
   - Documentation tabs with content
   - Download buttons for Markdown/HTML

## Troubleshooting Installation

### Python Version Issues

```bash
# Check your Python version
python3 --version  # Should be 3.8+

# If you have multiple Python versions
python3.10 -m venv venv
```

### Virtual Environment Issues

**On macOS/Linux:**
```bash
# If activation fails
source venv/bin/activate

# If still fails, try
. venv/bin/activate
```

**On Windows:**
```bash
# Use proper path
venv\Scripts\activate.bat
# or
venv\Scripts\Activate.ps1
```

### Dependency Installation Issues

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails
pip install package_name --no-cache-dir
```

### Jac Installation

```bash
# Install Jac explicitly
pip install jaclang

# Verify installation
jac --version
```

### Port Already in Use

```bash
# Backend on custom port
jac serve main.jac --port 8001

# Frontend on custom port
streamlit run app.py --server.port 8502
```

### Backend Won't Start

```bash
# Check if port is available
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Try with verbose output
jac serve main.jac -v

# Check dependencies
pip list | grep jaclang
```

### Frontend Won't Start

```bash
# Verify Streamlit installation
streamlit --version

# Clear cache
streamlit cache clear

# Run with verbose
streamlit run app.py --logger.level=debug
```

## Post-Installation Verification

### 1. Check Backend Health

```bash
# In new terminal
curl http://localhost:8000/docs
```

Should return API documentation.

### 2. Check Frontend Access

Visit `http://localhost:8501` in your browser.

### 3. Test Full Workflow

1. Open Streamlit UI
2. Enter test repository: `https://github.com/jaseci-labs/Agentic-AI`
3. Click Generate
4. Verify output is generated

## Configuration After Installation

### Enable Optional Features

**GitHub Token (for private repos)**:
```bash
# Edit BE/.env
GITHUB_TOKEN=ghp_your_token_here
```

**Custom Gemini Model**:
```bash
# Edit BE/.env
MODEL_NAME=gemini-1.5-flash  # Faster but less accurate
```

**Change Listening Port**:
```bash
# Backend
jac serve main.jac --port 9000

# Frontend - in app.py or via args
streamlit run app.py --server.port 9001
```

### Adjust Resource Limits

In `BE/.env`:
```env
# Analyze more files (careful with large repos)
MAX_FILE_SIZE=500000
MAX_REPO_SIZE=1000000000
```

## Directory Structure After Installation

```
agentic_codebase_genius/
├── venv/                       # Root virtual environment
├── BE/
│   ├── venv/                  # Backend virtual environment
│   ├── main.jac
│   ├── repo_mapper.jac
│   ├── code_analyzer.jac
│   ├── doc_genie.jac
│   ├── .env                   # Your configuration (created)
│   └── requirements.txt
├── FE/
│   ├── venv/                  # Frontend virtual environment
│   ├── app.py
│   └── requirements.txt
├── helpers/
│   ├── __init__.py
│   ├── git_utils.py
│   ├── file_utils.py
│   ├── parser_utils.py
│   └── doc_utils.py
├── outputs/                   # Generated docs (created on first run)
├── temp_repos/                # Cloned repos (created, auto-cleanup)
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

## Uninstallation

To completely remove Codebase Genius:

```bash
# Remove virtual environments
rm -rf venv BE/venv FE/venv

# Remove generated files
rm -rf outputs temp_repos

# Remove project directory
cd ..
rm -rf agentic_codebase_genius
```

## Next Steps

1. **Read Documentation**:
   - [Main README](README.md)
   - [Backend Guide](BE/README.md)
   - [Frontend Guide](FE/README.md)

2. **Try Examples**:
   - Analyze: `https://github.com/python/cpython`
   - Analyze: `https://github.com/google/golang-samples`

3. **Customize**:
   - Modify Jac agents in `BE/`
   - Extend parsers in `helpers/`
   - Customize UI in `FE/app.py`

4. **Deploy**:
   - Docker deployment
   - Cloud platform (Streamlit Cloud, Heroku, etc.)
   - Local network access

## Getting Help

- Check [README.md](README.md) for general info
- Review [BE/README.md](BE/README.md) for backend issues
- Check [FE/README.md](FE/README.md) for frontend issues
- Open an issue on GitHub with error details

## Performance Tuning

### For Slow Systems

In `BE/.env`:
```env
MODEL_NAME=gemini-1.5-flash
MAX_FILE_SIZE=50000
TEMPERATURE=0.5
```

### For Better Quality

In `BE/.env`:
```env
MODEL_NAME=gemini-1.5-pro
MAX_TOKENS=2000
TEMPERATURE=0.7
```

---

**Installation complete! Happy documenting! 🎉**
