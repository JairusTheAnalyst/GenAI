# API Documentation

Complete API reference for Codebase Genius backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required. For production deployment, implement API key validation.

## Endpoints

### 1. Generate Documentation

**Endpoint:** `POST /api/generate`

Generate documentation for a GitHub repository.

#### Request

```json
{
  "repo_url": "https://github.com/username/repository",
  "output_dir": "./outputs"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repo_url` | string | Yes | GitHub repository URL (must be public) |
| `output_dir` | string | No | Directory to save output (default: `./outputs`) |

#### Response

**Success (200):**
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
    },
    {
      "timestamp": "2024-01-01T00:00:05Z",
      "message": "Repository cloned successfully"
    }
  ]
}
```

**Error (400):**
```json
{
  "status": "error",
  "error": "Invalid repository URL",
  "details": "URL must start with https://github.com"
}
```

**Error (404):**
```json
{
  "status": "error",
  "error": "Repository not found",
  "details": "Could not clone repository. Verify URL is correct and public."
}
```

#### Examples

**cURL:**
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/example/python-project",
    "output_dir": "./outputs"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/generate',
    json={
        'repo_url': 'https://github.com/example/python-project',
        'output_dir': './outputs'
    }
)

print(response.json())
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    repo_url: 'https://github.com/example/python-project',
    output_dir: './outputs'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Python Requests:**
```python
import requests

url = "http://localhost:8000/api/generate"
payload = {
    "repo_url": "https://github.com/jaseci-labs/Agentic-AI",
    "output_dir": "./outputs"
}

response = requests.post(url, json=payload)
result = response.json()

if result['status'] == 'success':
    print(f"Documentation saved to: {result['output_path']}")
else:
    print(f"Error: {result['error']}")
```

### 2. Get Status

**Endpoint:** `GET /api/status`

Get current system status and health.

#### Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 3600,
  "active_tasks": 0,
  "total_repos_analyzed": 5
}
```

### 3. List Generated Docs

**Endpoint:** `GET /api/docs`

List all generated documentation.

#### Response

```json
{
  "status": "success",
  "docs": [
    {
      "repo_name": "python-project",
      "output_path": "./outputs/python-project/documentation.md",
      "generated_at": "2024-01-01T12:30:00Z",
      "status": "completed"
    },
    {
      "repo_name": "jac-project",
      "output_path": "./outputs/jac-project/documentation.md",
      "generated_at": "2024-01-01T11:15:00Z",
      "status": "completed"
    }
  ]
}
```

### 4. Get Document Content

**Endpoint:** `GET /api/docs/:repo_name`

Retrieve generated documentation content.

#### Parameters

| Parameter | Type | Location | Description |
|-----------|------|----------|-------------|
| `repo_name` | string | URL | Repository name |
| `format` | string | Query | Output format (`markdown`, `html`) |

#### Examples

```bash
# Get as markdown
curl http://localhost:8000/api/docs/python-project?format=markdown

# Get as HTML
curl http://localhost:8000/api/docs/python-project?format=html
```

#### Response

**Markdown (200):**
```markdown
# python-project

## Overview
...
```

### 5. Download Document

**Endpoint:** `GET /api/docs/:repo_name/download`

Download documentation as file.

#### Parameters

| Parameter | Type | Query | Description |
|-----------|------|-------|-------------|
| `format` | string | Yes | `md` for Markdown, `html` for HTML |

#### Examples

```bash
# Download markdown
curl -O http://localhost:8000/api/docs/python-project/download?format=md

# Download HTML
curl -O http://localhost:8000/api/docs/python-project/download?format=html
```

## Data Models

### WorkflowLog

```json
{
  "timestamp": "2024-01-01T12:30:00Z",
  "message": "Repository cloned successfully",
  "level": "info"
}
```

### GenerationResponse

```json
{
  "status": "success|error|processing",
  "repo_name": "string",
  "output_path": "string",
  "progress": 0-100,
  "workflow_log": [
    {
      "timestamp": "string",
      "message": "string"
    }
  ],
  "error": "string (if error)"
}
```

### DocumentMetadata

```json
{
  "repo_name": "string",
  "repo_url": "string",
  "output_path": "string",
  "generated_at": "2024-01-01T12:30:00Z",
  "status": "completed|failed|processing",
  "file_count": 42,
  "function_count": 128,
  "class_count": 15,
  "line_count": 5432
}
```

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Repository or resource not found |
| 500 | Internal Error | Server error during processing |
| 503 | Service Unavailable | Backend service not available |

### Error Response Format

```json
{
  "status": "error",
  "error": "Error title",
  "details": "Detailed error message",
  "code": "ERROR_CODE"
}
```

## Rate Limiting

Currently no rate limiting. For production, implement:

```python
# Pseudo-code
RATE_LIMITS = {
    "api_generate": {
        "calls": 5,
        "period": 3600  # per hour
    }
}
```

## Webhooks

Future feature for async notifications:

```json
{
  "event": "generation_complete",
  "repo_name": "python-project",
  "status": "success",
  "timestamp": "2024-01-01T12:30:00Z"
}
```

## CORS

Currently allows all origins. For production:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8501",
    "https://yourdomain.com"
]
```

## Performance Considerations

### Typical Response Times

| Scenario | Time |
|----------|------|
| Small repo (10 files) | 10-15s |
| Medium repo (50 files) | 30-45s |
| Large repo (100+ files) | 60-120s |

### Optimization

- Response times can be improved by:
  - Increasing `MAX_TOKENS`
  - Using faster model (`gemini-1.5-flash`)
  - Limiting file analysis scope

## Versioning

Current API version: **v1**

Future versions will maintain backward compatibility.

## Testing API

### Using Postman

1. Import: `POST` method
2. URL: `http://localhost:8000/api/generate`
3. Headers: `Content-Type: application/json`
4. Body:
```json
{
  "repo_url": "https://github.com/example/repo"
}
```
5. Send and check response

### Using Python

```python
import requests

def test_api():
    response = requests.post(
        'http://localhost:8000/api/generate',
        json={'repo_url': 'https://github.com/example/repo'}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    
    print("API test passed!")

if __name__ == '__main__':
    test_api()
```

## Troubleshooting API

### "Connection Refused"
- Verify backend is running: `jac serve main.jac`
- Check port 8000 is accessible
- Try: `curl http://localhost:8000/api/status`

### "Timeout"
- Increase request timeout
- Check backend logs for processing delays
- Consider smaller repositories for testing

### "Invalid JSON"
- Verify request body is valid JSON
- Use proper Content-Type header
- Check for special characters in repo URL

## Security Recommendations

For production deployment:

1. **Add Authentication:**
   ```python
   @app.post("/api/generate")
   def generate(request: GenerateRequest, auth: AuthToken = Depends(verify_token)):
       # Implementation
   ```

2. **Validate Input:**
   ```python
   def validate_repo_url(url: str) -> bool:
       return url.startswith('https://github.com/')
   ```

3. **Rate Limit:**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

4. **HTTPS Only:**
   - Use HTTPS in production
   - Set secure cookies
   - Implement CORS properly

## Support

- Check [README.md](../README.md) for general help
- Review [Backend Guide](../BE/README.md) for implementation details
- Open GitHub issues for bugs or feature requests

---

**API Documentation v1.0**
