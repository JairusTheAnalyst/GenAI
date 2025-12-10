# Deployment & Launch Checklist

Use this checklist to ensure everything is properly set up before launching Codebase Genius.

## ✅ Pre-Deployment Checklist

### Environment Setup

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Git installed: `git --version`
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Main dependencies installed: `pip install -r requirements.txt`

### Backend Setup

- [ ] Navigated to BE directory: `cd BE`
- [ ] Backend venv created: `python3 -m venv venv`
- [ ] Backend venv activated: `source venv/bin/activate`
- [ ] Backend dependencies installed: `pip install -r requirements.txt`
- [ ] .env file created in project root: `cp ../.env.example ../.env`
- [ ] GEMINI_API_KEY added to .env
- [ ] (Optional) GITHUB_TOKEN added to .env for private repos

### Frontend Setup

- [ ] Navigated to FE directory: `cd FE`
- [ ] Frontend venv created: `python3 -m venv venv`
- [ ] Frontend venv activated: `source venv/bin/activate`
- [ ] Frontend dependencies installed: `pip install -r requirements.txt`

### Configuration Verification

- [ ] .env file exists: `ls -la ../.env`
- [ ] GEMINI_API_KEY is set: `cat ../.env | grep GEMINI`
- [ ] API key format correct: Should start with `AIzaSy...`
- [ ] API key is valid (test with Python):
  ```bash
  python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('VALID' if os.getenv('GEMINI_API_KEY') else 'INVALID')"
  ```

### Port Availability

- [ ] Port 8000 is available (backend):
  ```bash
  lsof -i :8000  # Should show nothing
  ```
- [ ] Port 8501 is available (frontend):
  ```bash
  lsof -i :8501  # Should show nothing
  ```

## 🚀 Launch Checklist

### Terminal 1: Start Backend

- [ ] Navigate to BE: `cd BE`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Verify you're in backend venv: `which python` (should show venv path)
- [ ] Start Jac server: `jac serve main.jac --port 8000`
- [ ] See startup message: "Server running at http://localhost:8000"
- [ ] Keep terminal open

### Terminal 2: Start Frontend

- [ ] Navigate to FE: `cd FE`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Verify you're in frontend venv: `which python` (should show venv path)
- [ ] Start Streamlit: `streamlit run app.py --server.port=8501`
- [ ] Browser opens automatically to http://localhost:8501
- [ ] Keep terminal open

### System Health Checks

In a third terminal:

```bash
# Check backend is running
curl http://localhost:8000/health
# Should return: {"status": "ok"}

# Check frontend is accessible
curl http://localhost:8501
# Should return HTML content
```

- [ ] Backend responds: `curl http://localhost:8000/health`
- [ ] Frontend responds: `curl http://localhost:8501`
- [ ] Both services running without errors

## 🧪 First Run Test

### Via Web UI

1. [ ] Open browser to http://localhost:8501
2. [ ] See Codebase Genius interface
3. [ ] Enter test repo: `https://github.com/octocat/Hello-World`
4. [ ] Click "Generate Documentation"
5. [ ] Wait for processing (should complete in 30-60 seconds)
6. [ ] See generated documentation output
7. [ ] Download or view the markdown file
8. [ ] Verify content looks reasonable

### Via API (curl)

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/octocat/Hello-World"}'
```

- [ ] API endpoint responds
- [ ] Returns valid JSON
- [ ] No authentication errors
- [ ] Processing starts successfully

### Via Python

```python
from helpers.git_utils import validate_github_url
url = "https://github.com/octocat/Hello-World"
assert validate_github_url(url)
print("✓ Python API works")
```

- [ ] Python imports work
- [ ] Helper functions callable
- [ ] No module errors

## 📊 Verification Results

### System Status

- [ ] Backend running: ✓
- [ ] Frontend running: ✓
- [ ] API responding: ✓
- [ ] Web UI accessible: ✓
- [ ] First documentation generated: ✓

### Performance Check

- [ ] Generation completed in <2 minutes
- [ ] No memory warnings
- [ ] No timeout errors
- [ ] Output is readable markdown

## 🐛 Troubleshooting During Launch

### If Backend Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Try different port
jac serve main.jac --port 8001

# Check logs for errors
jac serve main.jac 2>&1 | tee backend.log
```

- [ ] Checked port 8000
- [ ] Verified Jac installation
- [ ] Checked for syntax errors in .jac files
- [ ] Reviewed error messages

### If Frontend Won't Start

```bash
# Check if port is in use
lsof -i :8501

# Kill existing process
kill -9 <PID>

# Check Streamlit installation
pip install --upgrade streamlit

# Try different port
streamlit run app.py --server.port=8502

# Check logs
streamlit run app.py --logger.level=debug
```

- [ ] Checked port 8501
- [ ] Verified Streamlit installation
- [ ] Checked for Python syntax errors
- [ ] Reviewed error messages

### If API Key Invalid

```bash
# Verify .env file location
pwd
ls .env

# Check key is set
cat .env | grep GEMINI_API_KEY

# Get new key from https://ai.google.dev/

# Test key
python3 << 'EOF'
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
print("Key is valid!")
EOF
```

- [ ] Found .env file
- [ ] Verified key is set
- [ ] Obtained new key if needed
- [ ] Key format is correct (no quotes)

## 📚 Documentation Review

Before launch, review:

- [ ] [QUICKSTART.md](./QUICKSTART.md) - Quick reference
- [ ] [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Detailed setup
- [ ] [CONFIG.md](./CONFIG.md) - Configuration options
- [ ] [API.md](./API.md) - API documentation
- [ ] [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues

## 🎯 Post-Launch Steps

After successful launch:

### Configuration Optimization

- [ ] Set appropriate TEMPERATURE (0.5-0.8)
- [ ] Configure MAX_TOKENS based on needs
- [ ] Set parallel workers based on CPU: `PARALLEL_WORKERS=4`
- [ ] Enable caching: `CACHE_ENABLED=true`
- [ ] Set timeout appropriate for your repos

### Integration

- [ ] Test with your own repository
- [ ] Verify output quality
- [ ] Customize output format if needed
- [ ] Set up auto-documentation workflow
- [ ] Integrate with your CI/CD pipeline

### Monitoring

- [ ] Monitor memory usage during analysis
- [ ] Check disk space in outputs directory
- [ ] Review generated documentation quality
- [ ] Track API usage and costs
- [ ] Keep logs for debugging

## 📋 Production Deployment Checklist

If deploying to production:

### Docker Setup

- [ ] Docker installed: `docker --version`
- [ ] Dockerfile created
- [ ] .env file prepared with production keys
- [ ] Docker image built: `docker build -t codebase-genius .`
- [ ] Container runs successfully: `docker run -p 8000:8000 ...`

### Server Configuration

- [ ] Server has 2+ GB RAM
- [ ] Server has stable internet connection
- [ ] Firewall allows ports 8000, 8501
- [ ] SSL/HTTPS configured (if needed)
- [ ] Reverse proxy configured (nginx, etc.)

### Security

- [ ] API keys stored securely (not in repo)
- [ ] .env file not committed to git
- [ ] .gitignore includes .env
- [ ] Authentication/authorization implemented
- [ ] Input validation active
- [ ] Rate limiting configured
- [ ] Error messages don't expose sensitive info

### Monitoring & Backup

- [ ] Logging configured
- [ ] Error notifications set up
- [ ] Output directory has backups
- [ ] Database backups scheduled (if using)
- [ ] Uptime monitoring enabled
- [ ] Performance metrics tracked

### Documentation

- [ ] Production deployment guide created
- [ ] API endpoints documented
- [ ] Configuration parameters documented
- [ ] Troubleshooting guide for production
- [ ] Runbook for common operations

## ✨ Final Verification

Run this final test:

```bash
#!/bin/bash

echo "=== Codebase Genius Deployment Check ==="
echo

echo "✓ Checking Python..."
python3 --version

echo "✓ Checking Git..."
git --version

echo "✓ Checking Backend..."
curl -s http://localhost:8000/health || echo "Backend not running"

echo "✓ Checking Frontend..."
curl -s http://localhost:8501 > /dev/null && echo "Frontend OK" || echo "Frontend not accessible"

echo
echo "=== All Systems Ready ==="
```

- [ ] All checks pass
- [ ] Both services running
- [ ] API responding
- [ ] Ready for production

## 🎉 Launch Complete!

Once all checks pass:

1. ✅ System is deployed and running
2. ✅ Documentation can be generated
3. ✅ API is accessible
4. ✅ Web UI is functional
5. ✅ Ready for end users

### Next Steps

- Announce to team
- Share system URL
- Provide API documentation
- Monitor initial usage
- Gather feedback
- Plan improvements

---

**Deployment Date:** _________________

**Deployed By:** _____________________

**Notes:** _____________________________

_______________________________________________

---

For support, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) or contact the project maintainer.

Good luck! 🚀
