# Codebase Genius - Complete Setup Guide

This guide will walk you through setting up and running the Codebase Genius documentation generation system on your machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Usage Examples](#usage-examples)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Python 3.8 or higher**
  ```bash
  python3 --version  # Should be 3.8+
  ```

- **Git**
  ```bash
  git --version  # Should be 2.0+
  ```

- **Jac Language Runtime**
  - Installation: `pip install jaclang`
  - Verification: `jac --version`

### API Keys

You'll need at least one of the following:

- **Google Gemini API Key** (recommended)
  - Get it from: https://ai.google.dev/
  - Required for code analysis and documentation generation

- **OpenAI API Key** (alternative)
  - Get it from: https://platform.openai.com/api-keys
  - Required if not using Gemini

### Optional

- **GitHub Token** (for analyzing private repositories)
  - Get it from: https://github.com/settings/tokens
  - Scopes: `repo`, `read:user`

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic_codebase_genius.git
cd agentic_codebase_genius

# OR if using the workspace structure
cd /path/to/myproject/agentic_codebase_genius
```

### Step 2: Create Virtual Environments

#### Main Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Backend Virtual Environment (Jac Server)

```bash
cd BE

# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
cd ..
```

#### Frontend Virtual Environment (Streamlit)

```bash
cd FE

# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install frontend dependencies
pip install -r requirements.txt
cd ..
```

### Step 3: Install Main Dependencies

```bash
# Make sure main venv is activated
source venv/bin/activate

# Install all requirements
pip install -r requirements.txt
```

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env

# OR on Windows:
copy .env.example .env
```

### Step 2: Edit .env File

Open `.env` in your text editor and add your API keys:

```dotenv
# Required: Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: GitHub Token for private repos
GITHUB_TOKEN=your_github_token_here

# System settings
TEMP_REPO_DIR=./temp_repos
OUTPUT_DIR=./outputs
MAX_FILE_SIZE=100000
MAX_REPO_SIZE=500000000

# Model Configuration
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Step 3: Verify Configuration

```bash
# Test that the environment file is loaded correctly
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

## Running the System

### Option 1: Backend Only (Jac Server)

This runs the backend API server without the UI:

```bash
cd BE

# Activate the backend virtual environment
source venv/bin/activate

# Start the Jac server
jac serve main.jac --port 8000

# You should see output like:
# > Server starting at http://localhost:8000
```

### Option 2: Full System (Backend + Frontend)

Run in separate terminal windows:

#### Terminal 1: Start Backend

```bash
cd BE
source venv/bin/activate
jac serve main.jac --port 8000
```

#### Terminal 2: Start Frontend

```bash
cd FE
source venv/bin/activate
streamlit run app.py --server.port=8501

# Frontend will open at http://localhost:8501
```

### Option 3: Using Docker

If you prefer containerized deployment:

```bash
# Build Docker image
docker build -t codebase-genius .

# Run backend container
docker run -p 8000:8000 --env-file .env codebase-genius

# Run frontend container (in another terminal)
docker run -p 8501:8501 --env-file .env codebase-genius streamlit run FE/app.py
```

See [DOCKER.md](./DOCKER.md) for detailed Docker instructions.

## Usage Examples

### Example 1: Generate Documentation via Web UI

1. Start both backend and frontend (see "Running the System")
2. Open http://localhost:8501 in your browser
3. Enter a GitHub repository URL:
   ```
   https://github.com/pallets/flask
   ```
4. Click "Generate Documentation"
5. Wait for analysis to complete
6. Download the generated markdown file

### Example 2: Generate Documentation via API

```bash
# Using curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/pallets/flask"}'

# Using Python
import requests

response = requests.post(
    'http://localhost:8000/analyze',
    json={'repo_url': 'https://github.com/pallets/flask'}
)

documentation = response.json()
print(documentation)
```

### Example 3: Using Python Directly

```python
from helpers.git_utils import clone_repository, validate_github_url
from helpers.file_utils import traverse_directory

# Validate URL
repo_url = "https://github.com/pallets/flask"
if validate_github_url(repo_url):
    # Clone repository
    result = clone_repository(repo_url)
    
    if result['success']:
        repo_path = result['path']
        
        # Analyze repository
        file_tree = traverse_directory(repo_path)
        print(f"Found {len(file_tree['files'])} files")
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'jaclang'"

**Solution:**
```bash
# Make sure you're in the correct virtual environment
which python  # Should show path inside venv

# Reinstall Jac
pip install --upgrade jaclang
```

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in the project root
2. Check that `GEMINI_API_KEY` is set in the `.env` file
3. Make sure you're running from the project root directory

```bash
# Verify environment variable
cat .env | grep GEMINI_API_KEY
```

### Issue: "Failed to clone repository"

**Possible causes and solutions:**

1. **Network issue:**
   ```bash
   ping github.com  # Check internet connection
   ```

2. **Private repository without authentication:**
   ```bash
   # Add GitHub token to .env
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
   ```

3. **Repository doesn't exist:**
   ```bash
   # Verify URL format
   # Should be: https://github.com/owner/repo
   ```

### Issue: "Port already in use"

**Solution:**
```bash
# Use a different port
jac serve main.jac --port 8001

# Or kill the process using the port
# On Linux/macOS:
lsof -i :8000
kill -9 <PID>

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Streamlit connection refused

**Solution:**
1. Verify backend is running: http://localhost:8000
2. Check firewall settings
3. Verify API URL in Streamlit sidebar matches backend address

```bash
# Backend should be running
curl http://localhost:8000/health
```

### Issue: Out of Memory

**Solution:**
```bash
# Reduce max file size in .env
MAX_FILE_SIZE=50000

# Or analyze smaller repositories first to test
```

### Issue: "Rate limit exceeded" from Gemini API

**Solution:**
1. Wait before making another request
2. Check your API quota at https://ai.google.dev/
3. Consider upgrading your API plan

## Getting Help

- Check [README.md](./README.md) for overview and features
- See [API.md](./API.md) for API documentation
- Review [INSTALLATION.md](./INSTALLATION.md) for advanced setup options
- Check backend [README.md](./BE/README.md) for Jac-specific details
- Check frontend [README.md](./FE/README.md) for UI details

## Next Steps

After successful setup:

1. ✅ Run the system on a small test repository
2. ✅ Generate your first documentation
3. ✅ Customize the output format if needed
4. ✅ Integrate with your development workflow

Happy documenting! 🧠📚
