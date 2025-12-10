# Docker Deployment Guide

Run Codebase Genius using Docker containers.

## Prerequisites

- Docker installed and running
- Docker Compose (optional, for multi-container setup)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: codebase-genius-backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - OUTPUT_DIR=/app/outputs
      - TEMP_REPO_DIR=/app/temp_repos
    volumes:
      - ./outputs:/app/outputs
      - ./temp_repos:/app/temp_repos
    restart: unless-stopped
    networks:
      - codebase-genius

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: codebase-genius-frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - JAC_API_HOST=backend
      - JAC_API_PORT=8000
    restart: unless-stopped
    networks:
      - codebase-genius

networks:
  codebase-genius:
    driver: bridge

volumes:
  outputs:
  temp_repos:
```

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GITHUB_TOKEN=your_token_here
```

Run:

```bash
docker-compose up
```

Access:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000

### Option 2: Individual Containers

#### Backend

Create `Dockerfile.backend`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt BE/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r BE/requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment
ENV PYTHONUNBUFFERED=1

# Start Jac server
CMD ["jac", "serve", "BE/main.jac", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -f Dockerfile.backend -t codebase-genius-backend .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/outputs:/app/outputs \
  codebase-genius-backend
```

#### Frontend

Create `Dockerfile.frontend`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY FE/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY FE ./

# Expose port
EXPOSE 8501

# Set environment
ENV PYTHONUNBUFFERED=1

# Streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[server]\nheadless = true\nenableXsrfProtection = false\n" > ~/.streamlit/config.toml

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

Build and run:

```bash
docker build -f Dockerfile.frontend -t codebase-genius-frontend .
docker run -p 8501:8501 \
  -e JAC_API_HOST=backend_ip \
  -e JAC_API_PORT=8000 \
  codebase-genius-frontend
```

## Multi-Container Network

Run both containers on same network:

```bash
# Create network
docker network create codebase-genius-net

# Run backend
docker run --network codebase-genius-net \
  --name backend \
  -p 8000:8000 \
  codebase-genius-backend

# Run frontend (in new terminal)
docker run --network codebase-genius-net \
  --name frontend \
  -p 8501:8501 \
  -e JAC_API_HOST=backend \
  codebase-genius-frontend
```

## Environment Variables

Pass via `-e` flag or env file:

```bash
docker run -e GEMINI_API_KEY=key -e OUTPUT_DIR=/app/outputs container_name
```

## Volume Mounts

Persist generated documentation:

```bash
docker run -v /host/path:/app/outputs image_name
```

## Networking

### Exposing Ports

```bash
# Map ports
docker run -p 8000:8000 -p 8501:8501 container_name

# Expose range
docker run -p 8000-9000:8000-9000 container_name
```

### Container Communication

```bash
# Link containers (deprecated, use networks)
docker run --link backend:backend container_name

# Modern: use networks
docker network create app-net
docker run --network app-net container_name
```

## Health Checks

Add to docker-compose.yml:

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Logging

### View logs:

```bash
docker logs container_name

# Follow logs
docker logs -f container_name

# View docker-compose logs
docker-compose logs -f
```

### Configure logging:

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Troubleshooting Docker

### Container won't start

```bash
# Check logs
docker logs container_name

# Inspect container
docker inspect container_name

# Run with debug
docker run -it image_name /bin/bash
```

### Port already in use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 process_id

# Or use different port
docker run -p 8001:8000 image_name
```

### Network issues

```bash
# Check network
docker network inspect network_name

# Test connectivity between containers
docker exec container_name ping other_container_name
```

### Slow performance

```bash
# Check resource usage
docker stats

# Increase allocated resources
docker run --memory 4g --cpus 2 image_name
```

## Production Deployment

### Use Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml codebase-genius
```

### Use Kubernetes

```bash
# Create deployment
kubectl apply -f kubernetes/deployment.yaml

# Scale replicas
kubectl scale deployment backend-app --replicas=3
```

Create `kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codebase-genius-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codebase-genius-backend
  template:
    metadata:
      labels:
        app: codebase-genius-backend
    spec:
      containers:
      - name: backend
        image: codebase-genius-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: gemini
```

## Security Best Practices

### Don't use root user

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Use specific versions

```dockerfile
FROM python:3.10-slim
RUN pip install jaclang==0.6.0
```

### Scan for vulnerabilities

```bash
docker scan image_name

# Or use Trivy
trivy image image_name
```

### Private registry

```bash
# Login
docker login registry.example.com

# Tag image
docker tag image_name registry.example.com/image_name:version

# Push
docker push registry.example.com/image_name:version
```

## Cleanup

```bash
# Remove container
docker rm container_name

# Remove image
docker rmi image_name

# Remove unused resources
docker system prune

# Remove all stopped containers
docker container prune
```

## Advanced Docker Compose

### Multiple environments

Create `docker-compose.dev.yml`:

```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    volumes:
      - ./BE:/app/BE  # Mount for development
    environment:
      - DEBUG=true
```

Run specific compose file:

```bash
docker-compose -f docker-compose.dev.yml up
```

## Performance Tips

- Use `.dockerignore` to exclude large files
- Layer dependencies separately for better caching
- Use lightweight base images
- Minimize number of layers
- Use multi-stage builds

Example multi-stage:

```dockerfile
# Build stage
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["python", "app.py"]
```

---

**Docker documentation v1.0**
