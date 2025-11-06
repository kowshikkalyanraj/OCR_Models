# src/groq_extractor.py

import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/settings.env'))

# Initialize Groq client
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in config/settings.env")

client = Groq(api_key=api_key)

# Current available models (November 2025)
# Primary: llama-3.3-70b-versatile (recommended replacement)
# Fallback: mixtral-8x7b-32768 (older but still available)
MODEL = "llama-3.3-70b-versatile"  # LATEST - Production ready
FALLBACK_MODEL = "mixtral-8x7b-32768"  # Alternative if primary fails

def extract_fields_from_ocr(raw_text: str) -> dict:
    """
    Sends raw OCR text to Groq to extract name, address, tracking number.
    Uses llama-3.3-70b-versatile model.
    """
    
    instruction = """You are an OCR data extraction expert. Read the following raw OCR text and extract ONLY:

1. Recipient Name - full name of recipient/addressee (ignore titles like "Ship To", "Bill")
2. Full Address - complete mailing address (street, city, state, zip, country if present)
3. Tracking Number - package tracking/reference number (usually alphanumeric, 8-30 characters)

Rules:
- Extract ONLY the actual names/addresses/numbers, no labels or descriptors
- Ignore weights, product codes, cycle numbers, reference codes that are not tracking numbers
- Tracking numbers often appear after "tracking:", "TRK", "tracking number", etc
- Look for patterns like: 1Z followed by alphanumerics (UPS), FDEG-type codes (FedEx)
- For address, combine street, city, state, zip into one line separated by commas
- Return null for any field not clearly present or identifiable
- Names should be person names only (2+ words typically)

Respond ONLY as valid JSON with NO additional text or explanation:
{
    "name": "extracted recipient name or null",
    "address": "street, city state zip or null",
    "tracking_number": "tracking number or null"
}"""

    raw_prompt = f"{instruction}\n\nRaw OCR Text to parse:\n{raw_text}"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": raw_prompt}],
            max_tokens=256,
            temperature=0.2  # Low temperature for consistent extraction
        )
        
        response_text = response.choices[0].message.content.strip()
        
        try:
            result = json.loads(response_text)
            
            # Clean up the result - ensure null fields are actually None
            result['name'] = result.get('name') or None
            result['address'] = result.get('address') or None
            result['tracking_number'] = result.get('tracking_number') or None
            
            return result
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON response: {response_text[:80]}")
            return {
                "name": None,
                "address": None,
                "tracking_number": None,
                "error": "Failed to parse JSON from model response"
            }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Groq API Error: {error_msg[:100]}")
        return {
            "name": None,
            "address": None,
            "tracking_number": None,
            "error": error_msg
        }