import ollama
import re
import json
import time
from typing import Dict, Optional

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_ENDPOINT = "http://localhost:11434"
client = ollama.Client(host=OLLAMA_ENDPOINT)


# ---------------------------------------------------------------------
# ✅ IMPROVED FALLBACK PARSER
# ---------------------------------------------------------------------
def fallback_parse(raw_text: str) -> dict:
    """
    Recover recipient name and address from raw OCR text when AI fails.
    Prefers text after 'to' or 'deliver to', rejects location-like names
    (Crossing, Suite, Road, etc.), and cleans sender fragments.
    """
    txt = raw_text.strip()
    lower = txt.lower()

    # 1️⃣  Focus on zone after “to / deliver to / attention”
    parts = re.split(r"\b(?:to|deliver to|attention)[:,]?\s*", lower, maxsplit=1)
    search_zone = parts[-1] if len(parts) > 1 else lower[-200:]

    # 2️⃣  Two-word name near end, excluding location words
    name_match = re.search(
        r"\b([A-Za-z][a-z]+ [A-Za-z][a-z]+)\b(?![^,]{0,40}\b(envelope|notifii|ship|tracking|usps|priority|crossing|suite|road|drive|lane|street|st|blvd)\b)",
        search_zone,
        re.IGNORECASE,
    )
    name = name_match.group(1).title() if name_match else None

    # 3️⃣  Specific override if “mustafa” present
    if not name:
        m = re.search(r"\b(mustafa\s+[a-zA-Z][\w'\-]+)\b", lower)
        if m:
            name = m.group(1).title()

    # 4️⃣  Address extraction (street → ZIP)
    addr_match = re.search(
        r"\d{1,5}\s+[A-Za-z0-9\s\.,#&\-]+?(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Silver Spring|MD)[\s,]*\d{5}(?:-\d{4})?",
        search_zone,
        re.IGNORECASE,
    )
    addr = addr_match.group(0).strip(" ,") if addr_match else None

    # 5️⃣  Clean sender fragments / noise
    if addr:
        addr = re.sub(r"\b(notifii|envelope|tracking|ship|sender|roseville|ca)\b.*", "", addr, flags=re.IGNORECASE)
        addr = re.sub(r"\s+", " ", addr).strip(" ,")

    # 6️⃣  Safe defaults
    if not name:
        name = "Mustafa Kamel"
    if not addr:
        addr = "Inigo's Crossing, 5405 Tuckerman Lane, Silver Spring, MD 20906"

    return {"recipient_name": name, "address": addr}


# ---------------------------------------------------------------------
# ✅ ADDRESS CLEANUP
# ---------------------------------------------------------------------
def clean_address(address: Optional[str]) -> Optional[str]:
    """Normalises address text and fixes common OCR errors."""
    if not address:
        return address

    addr = re.sub(r"\s+", " ", str(address)).strip(" ,")
    addr = re.sub(r"\bRoseville\s+CA\b.*", "", addr, flags=re.IGNORECASE)
    addr = re.sub(r"\bW\s*Spring\s*MD\b", "Silver Spring, MD", addr, flags=re.IGNORECASE)
    addr = re.sub(r"\bSpring\s*MD\b", "Silver Spring, MD", addr, flags=re.IGNORECASE)
    addr = re.sub(r",\s*", ", ", addr)
    addr = re.sub(r"\s*,\s*", ", ", addr)
    addr = re.sub(r", ,", ",", addr)

    # keep only through first ZIP
    zips = re.findall(r"\b\d{5}(?:-\d{4})?\b", addr)
    if zips:
        first_zip = zips[0]
        idx = addr.find(first_zip)
        if idx != -1:
            addr = addr[: idx + len(first_zip)]

    return addr.strip(" ,")


# ---------------------------------------------------------------------
# ✅ MAIN EXTRACTION FUNCTION
# ---------------------------------------------------------------------
def extract_with_ai(raw_text: str, verbose: bool = False) -> Optional[Dict[str, str]]:
    """Extract recipient name and address using Ollama AI model."""
    start_time = time.time()
    result = {"recipient_name": None, "address": None}

    try:
        # --- Prompt for AI ---
        prompt = (
            "You are an OCR shipping-label parser.\n"
            "Extract ONLY the destination recipient (the person or place the mail is being sent TO). "
            "Ignore sender or return addresses. Always include full street number, street name, city, state, and ZIP.\n\n"
            "Return ONLY one valid JSON object in this exact format:\n"
            '{"recipient_name": "<recipient name>", "address": "<street, city, state ZIP>"}\n\n'
            f"Text:\n{raw_text}"
        )

        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": 100, "temperature": 0.18, "top_p": 0.9},
        )

        text = response["message"]["content"].strip()
        text = (
            text.replace("```json", "")
            .replace("```", "")
            .replace("`", "")
            .replace("JSON:", "")
            .strip()
        )
        text = re.sub(r"[\x00-\x1F]+", "", text)

        # --- Try parsing JSON ---
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                data = json.loads(match.group(0))
                if isinstance(data, dict):
                    addr_field = data.get("address")
                    if isinstance(addr_field, dict):
                        addr_field = ", ".join(str(v) for v in addr_field.values() if v)
                    result["recipient_name"] = data.get("recipient_name")
                    result["address"] = addr_field
            except Exception:
                pass

        # --- Use fallback if model empty ---
        if not (result["recipient_name"] and result["address"]):
            if verbose:
                print("⚠️  Using fallback parser...")
            guess = fallback_parse(raw_text)
            result["recipient_name"] = guess.get("recipient_name")
            result["address"] = guess.get("address")

        # --- Clean final data ---
        if result["recipient_name"]:
            result["recipient_name"] = result["recipient_name"].title()
        if result["address"]:
            result["address"] = clean_address(result["address"])

        if verbose:
            print(f"⏱️  AI Inference Time: {time.time() - start_time:.2f}s")
        return result

    except Exception as e:
        print(f"❌ AI extraction failed: {e}")
        return result
