FROM python:3.11-slim

WORKDIR /workspace

# pip で必要なツールをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 必要なら補足的なツールも
RUN apt-get update && apt-get install -y curl \
    git
