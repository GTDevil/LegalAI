FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        python3-tk \
        python3-dev \
        git \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash ubuntu || true

USER ubuntu
WORKDIR /home/ubuntu
