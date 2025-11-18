# OCR Label Extractor with AI

An offline OCR label extraction system that uses Llama 3 (via Ollama) to extract recipient names and addresses from raw OCR text. The system first checks a local SQLite database for existing records, and if not found, uses AI to extract the information and saves it to the database for future lookups.

## Features

- ✅ Database-first lookup for fast retrieval
- ✅ AI-powered extraction using Llama 3 when database lookup fails
- ✅ Automatic saving of AI-extracted results to database
- ✅ Fully offline operation (once Ollama is set up)
- ✅ Interactive manual query mode
- ✅ CSV batch processing support

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running
   - Download from: https://ollama.ai
   - Install Ollama on your system
   - Start Ollama service: `ollama serve`
3. **Llama 3 model** pulled in Ollama
   - Run: `ollama pull llama3.2` (or `ollama pull llama3`)

## Installation

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Setup the model (one-time setup):
```bash
# This will download the model if needed and pre-warm it
python setup_model.py
```
**Note**: Models are saved locally after downloading. You only need to download once!

5. Ensure Ollama is running:
```bash
ollama serve
# Or if using Homebrew:
brew services start ollama
```

6. Verify the model is available:
```bash
ollama list
```

## Project Structure

```
ocr_label_llama3/
├── db_manager.py              # Database operations (init, get, save)
├── ai_extractor.py            # AI extraction logic using Ollama
├── data_pipeline.py           # Pipeline with database lookup + AI extraction
├── main.py                    # Entry point with interactive mode
├── requirements.txt           # Python dependencies
├── ocr_raw_labels.csv         # Input CSV file (create this)
├── ocr_structured_output.csv  # Output CSV file (generated)
├── ocr_labels.db              # SQLite database (created automatically)
└── venv/                      # Virtual environment (created during setup)
```

## Usage

### 1. Activate Virtual Environment

Before running the script, make sure to activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Prepare Input CSV File

Create a file named `ocr_raw_labels.csv` with the following format:

```csv
raw_text
"lex2 2.8 lbs, 2821 carradale dr, 95661-4047 roseville, ca, fat1, united states, zoey dong, dsm1, 0503 dsm1, tba132376390000, cycle 1, a sm1"
"batavia stkllt, special instructiu, metr 4684 3913 8542, g, ca 8206s, 95661, o, 230, 2, paper, fedex, mps 46843913 8553, frun, 2164 n, 9622 00 19 0 000 000 0000 0 00 4684 3913 8553, 8150 sierra college blvd ste, syta saephan, notifil, roseville ca 95661, ground, of 2, 214 787-430o, us, bill sender"
```

### 3. Run the Pipeline

**Option A: Using the optimized startup script (Recommended)**
```bash
./start.sh
```
This script automatically sets `OLLAMA_KEEP_ALIVE=5m` for optimal performance.

**Option B: Manual run**
```bash
# Set keep-alive for faster performance
export OLLAMA_KEEP_ALIVE=5m
python main.py
```

**Option C: Pre-warm model for consistent <2s performance**
```bash
# Run optimization script first (pre-warms the model)
python optimize_for_speed.py

# Then run your pipeline
python main.py
```

The system will:
1. Process all labels from `ocr_raw_labels.csv`
2. Check the database for each label
3. If not found, use AI to extract recipient name and address
4. Save AI-extracted results to the database
5. Generate `ocr_structured_output.csv` with results
6. Enter interactive mode for manual queries

### 4. Interactive Manual Query

After processing the CSV file, you can manually enter raw OCR text to test extraction:

```
Would you like to enter a raw text manually? (y/n): y
Enter raw text: [paste your OCR text here]
```

## Database Schema

The SQLite database (`ocr_labels.db`) uses the following schema:

```sql
CREATE TABLE labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_text TEXT UNIQUE,
    recipient_name TEXT,
    address TEXT
);
```

## Configuration

You can modify the AI model and settings in `ai_extractor.py`:

```python
OLLAMA_MODEL = 'llama3.2'  # Change to 'llama3' or other models
OLLAMA_ENDPOINT = 'http://localhost:11434'  # Default Ollama endpoint
```

## Output Format

The output CSV file (`ocr_structured_output.csv`) contains:

```csv
recipient_name,address
"Zoey Dong","2821 Carradale Dr, Roseville, CA 95661"
"Syta Saephan","8150 Sierra College Blvd Ste, Roseville, CA 95661"
```

## How It Works

1. **Database Lookup**: First, the system checks if the raw text exists in the database
2. **AI Extraction**: If not found, the system uses Llama 3 via Ollama to extract recipient name and address
3. **Database Storage**: AI-extracted results are automatically saved to the database
4. **Future Lookups**: Subsequent queries for the same text will be retrieved from the database (faster and no AI cost)

## Performance Optimization

The system is optimized for **sub-2-second response times**. Here are ways to achieve faster inference:

### 1. Use a Smaller Model (Recommended for Speed)

For faster inference, use a smaller model:

```bash
# Pull a smaller, faster model (1B parameters)
ollama pull llama3.2:1b

# Update ai_extractor.py to use it:
# OLLAMA_MODEL = 'llama3.2:1b'
```

### 2. Keep Model in Memory

Set the `OLLAMA_KEEP_ALIVE` environment variable to keep the model loaded in memory:

```bash
# macOS/Linux
export OLLAMA_KEEP_ALIVE=5m

# Windows
set OLLAMA_KEEP_ALIVE=5m

# Or add to your shell profile (.bashrc, .zshrc, etc.)
echo 'export OLLAMA_KEEP_ALIVE=5m' >> ~/.zshrc
```

### 3. Enable GPU Acceleration

Ensure Ollama is using your GPU (if available):

```bash
# Check if GPU is being used
ollama ps

# GPU acceleration is automatic if available
```

### 4. Test Performance

Run the performance test script:

```bash
python test_performance.py
```

This will test extraction speed and provide recommendations.

### 5. Current Optimizations

The code already includes:
- ✅ Shortened prompts for faster processing
- ✅ Limited output tokens (150 tokens max)
- ✅ Lower temperature (0.1) for deterministic, faster responses
- ✅ Optimized sampling parameters

### Performance Tips

- **First extraction**: May take longer as model loads (3-5 seconds)
- **Subsequent extractions**: Should be under 2 seconds if model stays in memory
- **Database lookup**: Always fast (<10ms) - use database-first approach
- **Batch processing**: Results are cached in database for instant future lookups

## Troubleshooting

### ModuleNotFoundError: No module named 'ollama'

**Solution**: 
- Make sure you've activated the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### Ollama Connection Error

If you see:
```
❌ Error connecting to Ollama: ...
```

**Solution**: 
- Make sure Ollama is installed and running: `ollama serve`
- Verify Ollama is accessible: `curl http://localhost:11434/api/tags`

### Model Not Found

If you see:
```
⚠️ Warning: Model 'llama3.2' not found
```

**Solution**:
- Pull the model: `ollama pull llama3.2`
- Or change the model name in `ai_extractor.py` to a model you have installed

### Empty AI Response

If AI extraction returns no results:
- The OCR text might be too noisy or incomplete
- Try using a different model (e.g., `llama3` instead of `llama3.2`)
- Check the OCR text quality

## Example Output

```
🚀 Running OCR + Database Lookup + AI Extraction System...

🔍 Testing Ollama connection...

📊 Processing labels from ocr_raw_labels.csv...

-------------------------------------------
🧾 Label #1
✅ Found in database
👤 Recipient Name: Zoey Dong
🏠 Address: 2821 Carradale Dr, Roseville, CA 95661
📍 Source: Database
-------------------------------------------
🧾 Label #2
🔍 Not found in database. Using AI extraction...
✅ Extracted with AI
👤 Recipient Name: Syta Saephan
🏠 Address: 8150 Sierra College Blvd Ste, Roseville, CA 95661
💾 Saved to database
📍 Source: AI
-------------------------------------------

✅ Pipeline complete! Results saved to: ocr_structured_output.csv
```

## License

This project is prepared by Palagiri Kowshikkalyanraj.

## Notes

- The system works completely offline once Ollama is set up
- First-time extraction for new texts will use AI (slower)
- Subsequent lookups for the same text will use the database (faster)
- The database grows over time as more texts are processed
- Always activate the virtual environment before running the script

