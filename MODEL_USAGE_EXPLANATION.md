# How Model Download and Usage Works

## 🔄 The Complete Flow

### Step 1: Download Model (Terminal Command - Manual)
```bash
ollama pull llama3.2:1b
```
**Where**: Run this in your terminal (NOT in Python code)
**Purpose**: Downloads the model to your local Ollama installation
**Location**: Stored in Ollama's model directory

### Step 2: Configure Model Name (Python Code)
```python
# In ai_extractor.py line 8
OLLAMA_MODEL = 'llama3.2:1b'
```
**Where**: `ai_extractor.py` line 8
**Purpose**: Tells the code which model to use
**Usage**: This string is passed to Ollama API

### Step 3: Use Model (Python Code)
```python
# In ai_extractor.py line 56-57
response = ollama.chat(
    model=model,  # This is 'llama3.2:1b'
    messages=[...]
)
```
**Where**: `ai_extractor.py` line 56
**Purpose**: Calls Ollama API with the model name
**What happens**: Ollama looks for the model locally (downloaded in Step 1)

## 📍 Where `ollama pull` is Mentioned

### 1. **Error Messages** (When model not found)
```python
# ai_extractor.py line 241
print(f"⚠️ Attempting to use '{model}' anyway. If it fails, please pull the model: ollama pull {model}")
```
**When shown**: If the model is not installed
**Purpose**: Tells user how to fix the problem

### 2. **Documentation** (README.md)
```markdown
# README.md line 155
ollama pull llama3.2:1b
```
**Purpose**: Instructions for users to download the model

### 3. **Performance Guide** (PERFORMANCE_GUIDE.md)
```markdown
# PERFORMANCE_GUIDE.md line 39
ollama pull llama3.2:1b
```
**Purpose**: Optimization instructions

### 4. **Test Scripts** (test_performance.py, check_setup.py)
```python
# test_performance.py line 54
print("  1. Use a smaller model: ollama pull llama3.2:1b")

# check_setup.py line 64
print(f"   Install it with: ollama pull {model}")
```
**Purpose**: Recommendations when performance is slow or model is missing

## 🎯 Summary

| Component | Location | Type | Purpose |
|-----------|----------|------|---------|
| `ollama pull llama3.2:1b` | Terminal | Command | Download model |
| `OLLAMA_MODEL = 'llama3.2:1b'` | ai_extractor.py:8 | Variable | Model name |
| `model=model` | ai_extractor.py:57 | Parameter | Pass to Ollama API |
| Error messages | ai_extractor.py:241 | String | Help user fix issues |
| Documentation | README.md, PERFORMANCE_GUIDE.md | Instructions | Guide users |

## ✅ Current Status

You've already:
1. ✅ Changed `OLLAMA_MODEL = 'llama3.2:1b'` in ai_extractor.py
2. ✅ The code will use this model name

**Next step**: Run the terminal command to download the model:
```bash
ollama pull llama3.2:1b
```

After downloading, the Python code will automatically use it!

## 🔍 How to Verify

1. **Check if model is downloaded**:
   ```bash
   ollama list
   ```
   Should show `llama3.2:1b` in the list

2. **Run the code**:
   ```bash
   python main.py
   ```
   The code will use `llama3.2:1b` automatically

3. **If model not found**:
   - Error message will tell you to run `ollama pull llama3.2:1b`
   - Run that command in terminal
   - Try again

