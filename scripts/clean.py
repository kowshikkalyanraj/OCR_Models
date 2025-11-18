import re

def clean_text(text):
    """
    Clean noisy OCR text before sending to Phi-3.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"[^A-Za-z0-9\- ,.#/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_tracking(text):
    """
    Extract USPS / UPS / FedEx / OnTrac tracking if Phi-3 fails.
    """
    patterns = [
        r"\b9\d{19}\b",                  # USPS 20–22 digits
        r"\b1Z[0-9A-Z]{16}\b",           # UPS
        r"\bTBA\d{12,}\b",               # Amazon TBA
        r"\b\d{12}\b",                   # Basic FedEx
    ]

    for p in patterns:
        m = re.search(p, text.replace(" ", ""))
        if m:
            return m.group(0)

    return ""
