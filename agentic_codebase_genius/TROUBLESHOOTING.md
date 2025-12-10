# Troubleshooting Guide

This guide helps you resolve common issues when using Codebase Genius.

## Quick Diagnosis

Start here to identify your issue:

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check virtual environment is activated
which python  # Should show path with 'venv'

# Check Git is installed
git --version

# Check API key is set
cat .env | grep GEMINI_API_KEY

# Check backend is running
curl http://localhost:8000/health

# Check frontend can access backend
curl http://localhost:8000/health
```

## Common Issues & Solutions

### Installation Issues

#### ❌ "ModuleNotFoundError: No module named 'jaclang'"

**Cause:** Jac is not installed or virtual environment isn't activated

**Solutions:**

```bash
# Solution 1: Activate virtual environment
source venv/bin/activate

# Check which Python is being used
which python

# Solution 2: Install Jac explicitly
pip install jaclang

# Solution 3: Upgrade pip first
pip install --upgrade pip
pip install jaclang

# Solution 4: Check installation
python -c "import jaclang; print(jaclang.__version__)"
```

#### ❌ "pip: command not found"

**Cause:** Python is not in PATH or pip is not installed

**Solutions:**

```bash
# Solution 1: Use python3 -m pip
python3 -m pip install -r requirements.txt

# Solution 2: Check Python installation
python3 --version

# Solution 3: Reinstall Python and pip
# See your OS-specific installation guide
```

#### ❌ "Permission denied" when creating venv

**Cause:** Insufficient permissions in directory

**Solutions:**

```bash
# Solution 1: Use different directory
mkdir ~/.virtualenvs
python3 -m venv ~/.virtualenvs/codebase_genius
source ~/.virtualenvs/codebase_genius/bin/activate

# Solution 2: Fix permissions
chmod 755 /path/to/directory
python3 -m venv venv

# Solution 3: Use sudo (not recommended)
sudo python3 -m venv venv
```

---

### Configuration Issues

#### ❌ "GEMINI_API_KEY not found" or "API key is invalid"

**Cause:** Missing or incorrect API key configuration

**Solutions:**

```bash
# Solution 1: Verify .env file exists
ls -la .env

# Solution 2: Check key is set
cat .env | grep GEMINI

# Solution 3: Verify key format
# Key should start with: AIzaSy...
# Not wrapped in quotes

# Solution 4: Get new key
# Visit: https://ai.google.dev/
# Copy key to .env without quotes:
# GEMINI_API_KEY=AIzaSyDxxx...

# Solution 5: Test loading
python3 << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GEMINI_API_KEY')
print(f"Key loaded: {key is not None}")
print(f"Key starts with: {key[:10] if key else 'NOT SET'}...")
EOF
```

#### ❌ ".env file not found"

**Cause:** .env was deleted or in wrong location

**Solutions:**

```bash
# Solution 1: Create from example
cp .env.example .env

# Solution 2: Manually create
cat > .env << 'EOF'
GEMINI_API_KEY=your_key_here
EOF

# Solution 3: Check location
pwd  # Should output project root
ls .env  # Should list .env file
```

#### ❌ "Invalid characters in configuration"

**Cause:** Special characters or incorrect format in .env

**Solutions:**

```bash
# Correct format (no quotes needed):
GEMINI_API_KEY=AIzaSyDxxx...
MODEL_NAME=gemini-1.5-pro

# Incorrect (will cause issues):
GEMINI_API_KEY="AIzaSyDxxx..."  # Don't quote
MODEL_NAME='gemini-1.5-pro'      # Don't quote

# If values have spaces, quote them:
OUTPUT_DIR="/path/with spaces"
```

---

### Backend Issues

#### ❌ "Port 8000 already in use"

**Cause:** Another process is using port 8000

**Solutions:**

```bash
# Solution 1: Use different port
jac serve main.jac --port 8001

# Solution 2: Kill existing process
# On Linux/macOS:
lsof -i :8000
kill -9 <PID>

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Solution 3: Find what's using the port
# Linux:
sudo netstat -tulpn | grep 8000

# macOS:
lsof -n -i :8000
```

#### ❌ "Jac server won't start"

**Cause:** Syntax error in .jac file or missing dependencies

**Solutions:**

```bash
# Solution 1: Check for syntax errors
cd BE
jac validate main.jac

# Solution 2: Reinstall dependencies
pip install --upgrade jaclang
pip install -r requirements.txt

# Solution 3: Check file exists
ls -la main.jac

# Solution 4: Try simple test
echo 'walker test { }' > test.jac
jac serve test.jac --port 8001

# Solution 5: Check error messages carefully
jac serve main.jac 2>&1 | tee error.log
```

#### ❌ "ImportError: No module named 'helpers'"

**Cause:** Python path not configured correctly

**Solutions:**

```bash
# Solution 1: Check directory structure
cd BE
ls -la ../helpers/

# Solution 2: Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Solution 3: Install as package
cd ..
pip install -e .

# Solution 4: Verify imports
python3 -c "from helpers.git_utils import clone_repository; print('OK')"
```

---

### Frontend Issues

#### ❌ "streamlit: command not found"

**Cause:** Streamlit not installed or wrong venv

**Solutions:**

```bash
# Solution 1: Activate correct venv
cd FE
source venv/bin/activate

# Solution 2: Install Streamlit
pip install streamlit

# Solution 3: Use python -m
python -m streamlit run app.py
```

#### ❌ "Connection refused" from Streamlit

**Cause:** Backend server not running

**Solutions:**

```bash
# Solution 1: Start backend first
cd BE
source venv/bin/activate
jac serve main.jac --port 8000

# Solution 2: Check backend is running
curl http://localhost:8000

# Solution 3: Update API URL in Streamlit
# In sidebar: Change backend host to correct IP/hostname
```

#### ❌ "Address already in use" for Streamlit

**Cause:** Port 8501 is in use

**Solutions:**

```bash
# Solution 1: Use different port
streamlit run app.py --server.port=8502

# Solution 2: Kill existing process
lsof -i :8501
kill -9 <PID>

# Solution 3: Check environment
echo $PORT
netstat -ano | findstr :8501
```

---

### Repository Analysis Issues

#### ❌ "Failed to clone repository"

**Cause:** Network issue, invalid URL, or private repo

**Solutions:**

```bash
# Solution 1: Test URL format
# Should be: https://github.com/owner/repo
# Not: git@github.com:owner/repo

# Solution 2: Test network
ping github.com

# Solution 3: Check URL is reachable
curl https://github.com/pallets/flask

# Solution 4: For private repos, add token
GITHUB_TOKEN=ghp_xxxxx

# Solution 5: Manual test clone
git clone https://github.com/owner/repo /tmp/test
```

#### ❌ "File too large" or "Timeout"

**Cause:** Repository too large or network slow

**Solutions:**

```bash
# Solution 1: Increase timeout
TIMEOUT_SECONDS=600

# Solution 2: Reduce file size limit
MAX_FILE_SIZE=50000

# Solution 3: Use shallow clone
# (Already done by default)

# Solution 4: Try smaller repository first
# Good test repos:
# https://github.com/octocat/Hello-World
# https://github.com/pallets/click

# Solution 5: Check disk space
df -h
```

#### ❌ "Permission denied" on repository files

**Cause:** Read permissions issue

**Solutions:**

```bash
# Solution 1: Check permissions
ls -la /path/to/repo
chmod -R 755 /path/to/repo

# Solution 2: Use different temp directory
TEMP_REPO_DIR=/tmp/codebase_genius

# Solution 3: Run with appropriate user
# Ensure user has read access to temp dir
```

---

### API Issues

#### ❌ "400 Bad Request"

**Cause:** Invalid request format or missing parameters

**Solutions:**

```bash
# Correct request format:
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/owner/repo"}'

# Check JSON is valid:
python3 -m json.tool <<< '{"repo_url": "..."}'
```

#### ❌ "401 Unauthorized"

**Cause:** Missing or invalid API key

**Solutions:**

```bash
# Solution 1: Verify key is set
echo $GEMINI_API_KEY

# Solution 2: Test API key directly
python3 << 'EOF'
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
print("API key is valid")
EOF

# Solution 3: Get new key from https://ai.google.dev/
```

#### ❌ "429 Rate limit exceeded"

**Cause:** Too many API calls in short time

**Solutions:**

```bash
# Solution 1: Wait before retrying
# Rate limit: depends on your API plan

# Solution 2: Reduce PARALLEL_WORKERS
PARALLEL_WORKERS=1

# Solution 3: Upgrade API plan
# Visit: https://ai.google.dev/

# Solution 4: Add retry logic
# (Should be handled by system)
```

---

### Performance Issues

#### ❌ "Out of memory" error

**Cause:** Analyzing too many files or large files

**Solutions:**

```bash
# Solution 1: Reduce parallel workers
PARALLEL_WORKERS=2

# Solution 2: Reduce max file size
MAX_FILE_SIZE=50000

# Solution 3: Increase system memory
# Or analyze smaller repositories

# Solution 4: Monitor memory usage
# Linux:
watch free -h

# macOS:
vm_stat
```

#### ❌ "Slow analysis"

**Cause:** Network latency or slow API

**Solutions:**

```bash
# Solution 1: Check network
ping 8.8.8.8

# Solution 2: Monitor API response time
# Look at backend logs for timing

# Solution 3: Use faster model
MODEL_NAME=gemini-1.5-flash
# Instead of:
MODEL_NAME=gemini-1.5-pro

# Solution 4: Enable caching
CACHE_ENABLED=true
```

---

## Getting More Help

### Collecting Debug Information

When reporting issues, provide:

```bash
# System information
python3 --version
pip --version
git --version
jac --version

# Environment
echo $VIRTUAL_ENV
env | grep GEMINI

# Error logs
jac serve main.jac 2>&1 | tee debug.log

# Backend logs
curl -v http://localhost:8000/health

# Streamlit logs
streamlit run app.py --logger.level=debug
```

### Useful Commands

```bash
# Test Python environment
python3 -c "import sys; print(sys.executable)"

# Test imports
python3 -c "from helpers.git_utils import *; print('OK')"

# Test API connection
curl -X GET http://localhost:8000/health

# Monitor processes
# Linux/macOS:
ps aux | grep -E 'jac|streamlit|python'

# Kill all Python processes (careful!)
pkill -f python
```

### Resources

- **Jac Documentation:** https://docs.jac.ai/
- **Gemini API Docs:** https://ai.google.dev/docs
- **Flask Docs:** https://flask.palletsprojects.com/
- **Streamlit Docs:** https://docs.streamlit.io/

### Contact & Support

- **GitHub Issues:** Report bugs and feature requests
- **Discussions:** Ask questions in GitHub Discussions
- **Email:** See repository for contact info

---

## Issue Not Listed?

1. Check the [README.md](./README.md)
2. Review [SETUP_GUIDE.md](./SETUP_GUIDE.md)
3. Check backend [BE/README.md](./BE/README.md)
4. Check frontend [FE/README.md](./FE/README.md)
5. Search existing GitHub issues
6. Collect debug info and create new issue

Remember: Clear error messages and reproduction steps help us help you faster! 🚀
