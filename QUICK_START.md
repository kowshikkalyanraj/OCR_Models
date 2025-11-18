# Quick Start Guide - Model Persistence & <2s Performance

## ✅ Model Persistence (Already Working!)

**Your model is already saved!** Ollama automatically saves models locally after downloading.

### Verify Your Model is Saved

```bash
ollama list
```

You should see:
```
llama3.2:1b    baf6a787fdff    1.3 GB    [recent date]
```

**✅ No need to download again!** The model stays saved permanently.

## 🚀 Achieving <2 Second Performance

### Method 1: Use Startup Script (Easiest - Recommended)

```bash
./start.sh
```

This automatically:
- ✅ Sets `OLLAMA_KEEP_ALIVE=5m` (keeps model in memory)
- ✅ Checks if Ollama is running
- ✅ Starts Ollama if needed
- ✅ Runs your pipeline with optimal settings

### Method 2: Set Keep-Alive Manually

```bash
# Set keep-alive (keeps model in memory for 5 minutes)
export OLLAMA_KEEP_ALIVE=5m

# Run your script
python main.py
```

**To make it permanent:**
```bash
# Add to your shell profile
echo 'export OLLAMA_KEEP_ALIVE=5m' >> ~/.zshrc
source ~/.zshrc
```

### Method 3: Pre-warm Before Processing

```bash
# Pre-warm the model (loads into memory)
python optimize_for_speed.py

# Then run your pipeline
python main.py
```

## 📊 Performance Expectations

### Without Optimization
- First call: 3-5 seconds (cold start)
- Subsequent calls: 1.5-3 seconds

### With Optimization (Keep-Alive + Pre-warming)
- First call: 2-3 seconds (pre-warming)
- Subsequent calls: **0.5-1.5 seconds** ✅
- New OCR data: **<2 seconds** ✅

### Database Lookup
- Always: **<10ms** (instant) ✅

## 🎯 Workflow for New OCR Data

### Recommended Workflow

1. **Startup** (once per session):
   ```bash
   ./start.sh
   ```
   OR
   ```bash
   export OLLAMA_KEEP_ALIVE=5m
   python main.py
   ```

2. **Process Your Data**:
   - Database lookups: Instant (<10ms)
   - New extractions: <2 seconds (model in memory)
   - Results saved to database for future instant lookups

3. **Subsequent Runs**:
   - Same data: Instant (from database)
   - New data: <2 seconds (model still in memory)

## 🔧 One-Time Setup

Run this once to verify everything is set up:

```bash
python setup_model.py
```

This will:
- ✅ Check if model is downloaded (it is!)
- ✅ Pre-warm the model
- ✅ Provide optimization instructions

## 📝 Key Points

1. **Model Persistence**: ✅ Models are saved locally (no re-download needed)
2. **Performance**: ✅ Use keep-alive or pre-warming for <2s performance
3. **New Data**: ✅ Works with any new OCR data (not just training data)
4. **Database**: ✅ Results are cached for instant future lookups

## 🎓 Understanding "Training" vs Optimization

### ❌ Model Training (Not What We Do)
- Models are **pre-trained** by Meta
- Training requires large datasets and GPUs
- Training takes hours/days
- **We don't train the model**

### ✅ Inference Optimization (What We Do)
- Optimize **how we use** the pre-trained model
- Pre-warm model into memory
- Use keep-alive to prevent unloading
- Limit output tokens for faster generation
- Optimize sampling parameters

**Result**: Consistent <2 second performance with any new OCR data!

## 🚀 Quick Commands

```bash
# Check if model is saved
ollama list

# Setup (one-time)
python setup_model.py

# Run with optimal performance
./start.sh

# OR manually
export OLLAMA_KEEP_ALIVE=5m
python main.py

# Test performance
python test_performance.py

# Optimize for speed
python optimize_for_speed.py
```

## ✅ Summary

1. ✅ **Model is saved** - No need to download again
2. ✅ **Use `./start.sh`** - Easiest way to get <2s performance
3. ✅ **Set keep-alive** - Keeps model in memory for fast inference
4. ✅ **Works with new data** - Not limited to training data
5. ✅ **Database caching** - Instant lookups for repeated data

Your system is ready for fast, consistent performance! 🎉

