FROM python:3.11-bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y git python3 python3-pip python3-venv ffmpeg curl && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt ./

# Install Python dependencies
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

# Install additional dependencies for API server
RUN pip install fastapi uvicorn[standard] python-multipart

COPY . /workspace
ENV PYTHONPATH=/workspace

# Create necessary directories
RUN mkdir -p /workspace/src/models/.cache /workspace/src/checkpoints

# Health check for Render
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command for API server
CMD ["python", "-m", "src.api.server"]