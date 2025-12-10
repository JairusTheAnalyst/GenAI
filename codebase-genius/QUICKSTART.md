# Quick Start Guide - 5 Minutes to Documentation

Get Codebase Genius running in 5 minutes with this quick setup guide.

## TL;DR

```bash
# 1. Clone and setup
git clone <repo> && cd agentic_codebase_genius
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Run backend (Terminal 1)
cd BE && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
jac serve main.jac --port 8000

# 4. Run frontend (Terminal 2)
cd FE && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
streamlit run app.py --server.port=8501

# 5. Open browser
# Visit http://localhost:8501 and enter a repo URL!
```

## Detailed Quick Start

### 1️⃣ Initial Setup (2 minutes)

```bash
# Navigate to project directory
cd agentic_codebase_genius

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure API Keys (1 minute)

```bash
# Create environment file
cp .env.example .env

# Edit .env with your editor and add:
# GEMINI_API_KEY=your_key_here
nano .env  # Or use your favorite editor
```

Get your Gemini API key from: https://ai.google.dev/

### 3️⃣ Start Backend (1 minute)

Open **Terminal 1:**

```bash
cd BE
source venv/bin/activate
jac serve main.jac --port 8000
```

You should see: `Server running at http://localhost:8000`

### 4️⃣ Start Frontend (1 minute)

Open **Terminal 2:**

```bash
cd FE
source venv/bin/activate
streamlit run app.py --server.port=8501
```

Browser should open automatically to `http://localhost:8501`

### 5️⃣ Generate Documentation!

In the Streamlit web interface:

1. Enter a GitHub repository URL:
   - Try: `https://github.com/pallets/flask`
   - Or: `https://github.com/psf/requests`

2. Click **"Generate Documentation"**

3. Wait for analysis to complete (usually 30-60 seconds)

4. Download the markdown file

5. View generated documentation with diagrams!

## What Next?

- ✅ Generated your first docs? Awesome! 🎉
- 📖 Read the full [SETUP_GUIDE.md](./SETUP_GUIDE.md) for advanced options
- 🐳 Check [DOCKER.md](./DOCKER.md) for containerized deployment
- 🔧 See [API.md](./API.md) for API endpoint documentation
- 💡 Review backend [README.md](./BE/README.md) for architecture details

## Common Issues

### "GEMINI_API_KEY not set"
Make sure `.env` exists and has your key:
```bash
cat .env | grep GEMINI_API_KEY
```

### "Port 8000 already in use"
Change the port:
```bash
jac serve main.jac --port 8001
```

### "ModuleNotFoundError"
Ensure virtual environment is activated:
```bash
which python  # Should show path with 'venv'
```

## Need Help?

- Full setup guide: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- API documentation: [API.md](./API.md)
- Docker deployment: [DOCKER.md](./DOCKER.md)
- Installation details: [INSTALLATION.md](./INSTALLATION.md)

---

**That's it!** You now have Codebase Genius running. 🚀
