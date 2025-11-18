# Model Persistence and Performance Optimization Guide

## ✅ Model Persistence (Already Works!)

**Good News**: Ollama automatically saves models locally after downloading. You **don't need to pull the model every time**.

### How Model Persistence Works

1. **First Time**: Run `ollama pull llama3.2:1b`
   - Model is downloaded from Ollama servers
   - Saved to local storage: `~/.ollama/models/` (or similar)
   - **Model stays saved permanently**

2. **Subsequent Uses**: Just use the model name in your code
   - Ollama automatically loads from local storage
   - No need to download again
   - Works offline (once downloaded)

### Verify Model is Saved

```bash
# Check installed models
ollama list

# You should see your model:
# llama3.2:1b    baf6a787fdff    1.3 GB    [recent date]
```

**✅ Your model is already saved!** (You can see it in `ollama list` output)

## 🚀 Optimizing for <2 Second Performance

The model is **pre-trained** and doesn't need training. Instead, we optimize the **inference process** for speed.

### Why Performance Varies

1. **Cold Start**: First call takes 3-5 seconds (model loading)
2. **Warm Model**: Subsequent calls are faster (<2 seconds)
3. **Model Size**: Smaller models (1b) are faster than larger ones (3.2b)
4. **GPU**: GPU acceleration makes it 3-5x faster
5. **Memory**: Keep model in memory for instant access

### Solution: Model Pre-warming

Pre-warming loads the model into memory **before** processing your data, ensuring consistent <2s performance.

## 📋 Setup Instructions

### Step 1: One-Time Model Setup

```bash
# Run the setup script (only needed once)
python setup_model.py
```

This script:
- ✅ Checks if model is downloaded (it is!)
- ✅ Pre-warms the model (loads into memory)
- ✅ Provides optimization instructions

### Step 2: Set Keep-Alive (Recommended)

Keep the model in memory for faster subsequent calls:

```bash
# Temporary (for current session)
export OLLAMA_KEEP_ALIVE=5m

# Permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export OLLAMA_KEEP_ALIVE=5m' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Use Optimized Startup

**Option A: Use startup script (Easiest)**
```bash
./start.sh
```
This automatically sets keep-alive and runs your script.

**Option B: Pre-warm before processing**
```bash
# Pre-warm the model
python optimize_for_speed.py

# Then run your pipeline
python main.py
```

**Option C: Manual setup**
```bash
# Set keep-alive
export OLLAMA_KEEP_ALIVE=5m

# Run your script
python main.py
```

## 🎯 Performance Optimization Strategies

### 1. Model Pre-warming (Best for Consistency)

Run before processing new data:
```bash
python optimize_for_speed.py
```

**What it does**:
- Makes test calls to load model into memory
- Warms up the inference pipeline
- Tests performance to ensure <2s target

**When to use**:
- Before processing large batches
- When starting a new session
- To ensure consistent performance

### 2. Keep-Alive (Best for Repeated Use)

Set environment variable:
```bash
export OLLAMA_KEEP_ALIVE=5m
```

**What it does**:
- Keeps model loaded in memory for 5 minutes
- Eliminates cold start delays
- Ensures fast subsequent calls

**When to use**:
- Processing multiple files
- Interactive use
- Batch processing

### 3. Startup Script (Best for Convenience)

Use the provided startup script:
```bash
./start.sh
```

**What it does**:
- Automatically sets keep-alive
- Checks if Ollama is running
- Starts Ollama if needed
- Runs your script with optimal settings

## 📊 Expected Performance

### Without Optimization
- **First call**: 3-5 seconds (cold start)
- **Subsequent calls**: 1.5-3 seconds
- **New session**: 3-5 seconds again (model unloaded)

### With Optimization (Keep-Alive + Pre-warming)
- **First call**: 2-3 seconds (pre-warming)
- **Subsequent calls**: 0.5-1.5 seconds ✅
- **New session**: <2 seconds (model stays in memory) ✅

### With Database Lookup
- **Database hits**: <10ms (instant) ✅
- **AI extraction**: <2 seconds (with optimization) ✅

## 🔄 Workflow for New OCR Data

### Recommended Workflow

1. **Startup** (once per session):
   ```bash
   # Option A: Use startup script
   ./start.sh
   
   # Option B: Manual setup
   export OLLAMA_KEEP_ALIVE=5m
   python optimize_for_speed.py
   ```

2. **Process Data**:
   ```bash
   python main.py
   ```
   - Database lookups: Instant (<10ms)
   - New extractions: <2 seconds (model in memory)
   - Results saved to database for future instant lookups

3. **Subsequent Runs**:
   - Same data: Instant (from database)
   - New data: <2 seconds (model still in memory)

## 🎓 Understanding Model "Training" vs Optimization

### ❌ Model Training (Not Needed)
- Models are **pre-trained** by Meta (Llama creators)
- Training requires large datasets and GPUs
- Training takes hours/days
- **We don't train the model**

### ✅ Inference Optimization (What We Do)
- Optimize **how we use** the pre-trained model
- Pre-warm model into memory
- Use keep-alive to prevent unloading
- Limit output tokens for faster generation
- Optimize sampling parameters

## 📝 Summary

1. **Model Persistence**: ✅ Models are saved locally (no re-download needed)
2. **Performance**: ✅ Optimize inference, not training
3. **Setup**: ✅ Run `setup_model.py` once
4. **Usage**: ✅ Use `start.sh` or set `OLLAMA_KEEP_ALIVE=5m`
5. **Result**: ✅ Consistent <2 second performance

## 🚀 Quick Start

```bash
# 1. One-time setup (if not done already)
python setup_model.py

# 2. Set keep-alive (recommended)
export OLLAMA_KEEP_ALIVE=5m

# 3. Run your pipeline
./start.sh
# OR
python main.py
```

That's it! Your model is saved, optimized, and ready for fast inference.

