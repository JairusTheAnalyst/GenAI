# Codebase Genius - Frontend (Streamlit)

Interactive web interface for generating code documentation using Codebase Genius.

## Features

- **User-friendly Interface**: Clean, intuitive design for repository analysis
- **Real-time Progress**: Live status updates during documentation generation
- **Multiple Export Formats**: Download as Markdown or HTML
- **Preview Sections**: View different sections of generated documentation
- **Architecture Diagrams**: Mermaid diagrams for code relationships
- **Responsive Design**: Works on desktop, tablet, and mobile

## Setup

### 1. Navigate to Frontend Directory

```bash
cd FE
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Ensure Backend is Running

Make sure the Jac backend is running on your configured host and port:

```bash
# In another terminal
cd ../BE
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jac serve main.jac
```

## Running the Frontend

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Enter Repository URL**: Paste a GitHub repository URL (must be public)
2. **Configure Backend**: (Optional) Adjust the API host and port if not using defaults
3. **Set Output Directory**: Choose where documentation should be saved
4. **Click Generate**: Start the analysis
5. **View Results**: Browse the generated documentation in tabs
6. **Download**: Export as Markdown or HTML

## Configuration

### Backend Settings (Sidebar)

- **API Host**: Where your Jac server is running (default: `localhost`)
- **API Port**: Port number (default: `8000`)
- **Output Directory**: Where generated docs are saved (default: `./outputs`)

### Environment Variables

Create a `.env` file for sensitive configuration:

```env
JAC_API_HOST=localhost
JAC_API_PORT=8000
OUTPUT_DIR=./outputs
```

Load in app:
```python
from dotenv import load_dotenv
load_dotenv()
```

## File Structure

```
FE/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Interface Sections

### 🔧 Configuration (Sidebar)
- Backend API settings
- Output directory
- API connection status

### 📝 Main Input
- GitHub repository URL input
- Generate button
- Status indicators

### 📊 Processing Status
- Progress bar
- Processing steps with status
- Real-time logs

### 📄 Generated Documentation
Tabbed interface showing:
- **Overview**: Project description and metadata
- **Structure**: File tree visualization
- **API Reference**: Functions and classes
- **Dependencies**: External packages
- **Diagrams**: Architecture and relationship diagrams

### 📥 Download Options
- Markdown format
- HTML format

## Customization

### Change Color Scheme

Edit the custom CSS in `app.py`:

```python
st.markdown("""
    <style>
    .main-header {
        color: #your-color-here;
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Sections

Add a new tab to the documentation viewer:

```python
with tabs[n]:
    st.markdown("## New Section")
    st.write(content)
```

### Customize Status Messages

Modify the log messages in the generation section:

```python
with log_container:
    st.markdown("- ✅ Your custom message")
```

## Deployment

### Local Network

```bash
streamlit run app.py --server.address=0.0.0.0
```

Access from other machines at `http://your-ip:8501`

### Cloud Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from GitHub repository
4. Configure secrets in Streamlit dashboard

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t codebase-genius-fe .
docker run -p 8501:8501 codebase-genius-fe
```

## Performance Tips

- Keep the backend running for faster generation
- Clear browser cache if UI doesn't update
- For large repositories, increase timeouts in the backend

## Troubleshooting

### "Connection refused" Error
- Verify backend is running: `jac serve main.jac`
- Check host and port settings match
- Ensure firewall allows the port

### Slow Performance
- Check backend logs for processing delays
- Limit file analysis in backend for large repos
- Use a faster network connection

### UI Not Updating
- Refresh the browser
- Clear Streamlit cache: `streamlit cache clear`
- Restart the application

### Repository Not Found
- Verify URL is correct
- Ensure repository is public
- Try a different public repository to test

## Available Components

### Status Messages
```python
st.info("ℹ️ Information message")
st.success("✅ Success message")
st.warning("⚠️ Warning message")
st.error("❌ Error message")
```

### Custom HTML
```python
st.markdown('<div class="status-success">Content</div>', unsafe_allow_html=True)
```

### Progress Tracking
```python
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
```

## Styling Classes

Available CSS classes for custom styling:

- `.main-header`: Main title styling
- `.status-success`: Success message styling
- `.status-error`: Error message styling
- `.status-info`: Info message styling

## Integration with Backend

The frontend communicates with the Jac backend via HTTP API:

```python
payload = {
    "repo_url": repo_url,
    "output_dir": output_dir
}

response = requests.post(
    f"{api_base_url}/api/generate",
    json=payload
)
```

Response format:
```json
{
  "status": "success|error",
  "repo_name": "repository_name",
  "output_path": "/path/to/documentation.md",
  "progress": 100,
  "workflow_log": []
}
```

## Advanced Features

### Custom Themes

```python
st.set_page_config(
    theme="light",  # or "dark"
)
```

### Session State

```python
if 'repo_url' not in st.session_state:
    st.session_state.repo_url = ''
```

### Caching Results

```python
@st.cache_data
def load_documentation(repo_name):
    return read_doc_file(repo_name)
```

## Future Enhancements

- [ ] Batch processing multiple repositories
- [ ] Scheduled documentation updates
- [ ] Repository comparison
- [ ] Custom template support
- [ ] Syntax highlighting improvements
- [ ] Dark mode toggle
- [ ] Documentation versioning
- [ ] Team collaboration features

## Support

For issues with the frontend:
1. Check backend is running
2. Verify network connectivity
3. Review Streamlit logs
4. Check browser console for errors

## License

MIT License - See LICENSE file

---

**Built with Streamlit 🎈**
