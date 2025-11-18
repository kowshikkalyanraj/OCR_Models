import json
import re

def extract_json(text):
    """
    Extract JSON object from model output, even if extra text exists.
    """
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        cleaned = text[start:end]
        return json.loads(cleaned)
    except:
        return {
            "Name": "",
            "Address": "",
            "TrackingNumber": ""
        }

def clean_address(addr):
    """
    Make address uppercase, fix spaces, remove double commas.
    """
    if not addr:
        return ""

    addr = addr.upper()
    addr = re.sub(r"\s+", " ", addr)
    addr = addr.replace(",,", ",")
    return addr.strip()
