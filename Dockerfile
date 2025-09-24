FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y git python3 python3-pip python3-venv ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

COPY . /workspace
ENV PYTHONPATH=/workspace

CMD ["/bin/bash"]