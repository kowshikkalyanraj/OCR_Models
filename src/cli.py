# src/cli.py
import sys
import os
import json
from pathlib import Path
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.groq_extractor import extract_fields_from_ocr

def process_file(input_path, output_path):
    """Process raw OCR text file and extract structured data."""
    
    print(f"📂 Input file: {input_path}")
    print(f"📊 Output file: {output_path}")
    print("-" * 80)
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = [line.strip() for line in infile if line.strip()]
    
    print(f"Found {len(lines)} records to process...")
    print("-" * 80)
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for idx, raw_text in enumerate(tqdm(lines, desc="Processing"), 1):
            result = extract_fields_from_ocr(raw_text)
            
            # Combine input and output
            output_record = {
                "record_id": idx,
                "input": raw_text,
                **result
            }
            
            # Write as JSONL
            outfile.write(json.dumps(output_record) + '\n')
            
            # Print to console
            print(f"\n✅ Record {idx}:")
            print(f"   Name: {result.get('name')}")
            print(f"   Address: {result.get('address')}")
            print(f"   Tracking: {result.get('tracking_number')}")
    
    print("\n" + "=" * 80)
    print(f"✓ Extraction complete! Results saved to: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 src/cli.py <input_txt> <output_jsonl>")
        print("\nExample:")
        print("  python3 src/cli.py examples/sample_raw_texts.txt output/results.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    process_file(input_file, output_file)
