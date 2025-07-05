FROM node:18-slim

RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip git
    
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
