import re
import json
import time
import ollama

OLLAMA_MODEL = "llama3.2:1b"
client = ollama.Client(host="http://localhost:11434")

VALID_STATES = {"CA","NY","TX","FL","WA","OR","NV","AZ","UT","CO","NM","ID",
                "WY","MT","ND","SD","NE","KS","OK","MN","IA","MO","AR","LA",
                "WI","IL","IN","MI","OH","KY","TN","MS","AL","GA","SC","NC",
                "VA","WV","PA","DE","MD","NJ","CT","RI","MA","VT","NH","ME"}

NOISE = {"united","states","fat1","dsm1","metr","ref","wi","stlklt","stkllt","g",
         "0f","of","us","notifil","notifii","paper","fedex","ground","tracking",
         "bill","sender","cycle","lbs","weight","roseville"}

STREET_SUFFIXES = ["st","street","ave","avenue","blvd","road","rd","drive","dr",
                   "lane","ln","way","court","ct","place","pl","ste","suite"]


def clean(x):
    if not x:
        return ""
    return re.sub(r"\s+", " ", x).strip()


# ----------------------------------------------------------
# ZIP (anchor)
# ----------------------------------------------------------
def get_zip(raw):
    m = re.search(r"\b(\d{5}(?:-\d{4})?)\b", raw)
    return (m.group(1), m.start()) if m else (None, None)


# ----------------------------------------------------------
# STREET
# ----------------------------------------------------------
def get_street(raw, zip_pos):
    if zip_pos is None:
        return (None, None)

    pattern = re.compile(
        r"(\d{1,6}\s+[A-Za-z0-9 .'-]{2,60}\s+(?:St|Street|Ave|Avenue|Blvd|Road|Rd|Drive|Dr|Ln|Lane|Way|Court|Ct|Place|Pl|Ste))",
        re.I,
    )

    best = None
    best_pos = -1

    for m in pattern.finditer(raw):
        if m.start() < zip_pos:
            best = clean(m.group(1)).title()
            best_pos = m.start()

    return (best, best_pos)


# ----------------------------------------------------------
# STATE
# ----------------------------------------------------------
def get_state(raw):
    for st in VALID_STATES:
        if re.search(fr"\b{st}\b", raw, re.I):
            return st
    return None


# ----------------------------------------------------------
# CITY (based on flexible patterns)
# ----------------------------------------------------------
def get_city(raw, state, zip_code):
    if not state:
        return None

    raw = raw.lower()

    # roseville ca 95661
    pattern1 = rf"([a-z .'-]{{3,40}})\s+{state.lower()}\s+{zip_code}"
    match = re.search(pattern1, raw)
    if match:
        city = clean(match.group(1)).title()
        return city

    # roseville, ca
    pattern2 = rf"([a-z .'-]{{3,40}})[, ]+\s*{state.lower()}"
    match2 = re.search(pattern2, raw)
    if match2:
        city = clean(match2.group(1)).title()
        return city

    # fallback
    return None


# ----------------------------------------------------------
# NAME (best human-like block)
def get_name(raw, street_pos):
    # name appears anywhere BEFORE street
    block = raw[:street_pos] if street_pos else raw

    candidates = re.findall(r"[A-Za-z][a-zA-Z'`.-]+(?:\s+[A-Za-z][a-zA-Z'`.-]+)+", block)

    good = []
    for c in candidates:
        low = c.lower()
        if any(n in low for n in NOISE):
            continue
        # must not contain street suffix
        if any(s in low for s in STREET_SUFFIXES):
            continue
        good.append(c)

    if not good:
        return None

    # longest name is usually real
    return max(good, key=len).title()


# ----------------------------------------------------------
# MAIN HYBRID EXTRACTOR
# ----------------------------------------------------------
def extract_with_ai(raw_text, model=OLLAMA_MODEL, verbose=False):
    raw = clean(raw_text)
    # AI inference (but regex will override if needed)
    ai_name = None
    ai_addr = None
    try:
        out = client.chat(
            model=model,
            messages=[{"role": "user", "content": f"Extract JSON with name/address: {raw}"}],
            options={"num_predict": 80, "temperature": 0.1}
        )
        j = re.search(r"\{[\s\S]*\}", out["message"]["content"])
        if j:
            data = json.loads(j.group())
            if isinstance(data.get("recipient_name"), str):
                ai_name = clean(data["recipient_name"])
            # Convert dict → string if needed
            addr = data.get("address")
            if isinstance(addr, dict):
                ai_addr = clean(" ".join(str(v) for v in addr.values()))
            elif isinstance(addr, str):
                ai_addr = clean(addr)
    except:
        pass

    # REGEX EXTRACTION
    zip_code, zip_pos = get_zip(raw)
    street, street_pos = get_street(raw, zip_pos)
    state = get_state(raw)
    city = get_city(raw, state, zip_code)
    name = get_name(raw, street_pos)

    final_name = name or ai_name

    # Build final address
    final_address = None
    if street and city and state and zip_code:
        final_address = f"{street}, {city}, {state} {zip_code}"
    else:
        final_address = ai_addr

    return {"recipient_name": final_name, "address": final_address}
