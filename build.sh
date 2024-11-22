#!/usr/bin/env bash
# Build script for Render deployment
apt-get update && apt-get install -y portaudio19-dev
# Install dependencies
pip install -r requirements.txt

