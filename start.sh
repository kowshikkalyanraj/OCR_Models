#!/bin/bash
# Optimized startup script for sub-2s OCR Label Extractor

# Keep model in memory for 5 minutes
export OLLAMA_KEEP_ALIVE=5m

# Ensure Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    brew services start ollama 2>/dev/null || ollama serve &
    sleep 3
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# ✅ Pre-warm the model before running main.py
echo "🔥 Pre-warming model for faster inference..."
python optimize_for_speed.py

# 🚀 Run main pipeline
echo "🚀 Starting OCR Label Extractor with optimal settings..."
python main.py
