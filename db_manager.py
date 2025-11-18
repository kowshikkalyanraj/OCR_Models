import sqlite3
import pandas as pd
import re

DB_NAME = "ocr_labels.db"

VALID_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
    "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
    "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
    "TX","UT","VT","VA","WA","WV","WI","WY"
}


# --------------------------------------
# VALID NAME
# --------------------------------------
def is_valid_name(name):
    if not name or not isinstance(name, str):
        return False

    name = name.strip()

    # Must contain at least 2 words
    if len(name.split()) < 2:
        return False

    # No digits
    if any(ch.isdigit() for ch in name):
        return False

    # No garbage tokens
    blacklist = ["notifii", "warehouse", "tracking", "fat1", "dsm1", "stkllt"]
    if any(b in name.lower() for b in blacklist):
        return False

    return True


# --------------------------------------
# VALID ADDRESS
# --------------------------------------
def is_valid_address(addr):
    if not addr or not isinstance(addr, str):
        return False

    addr = addr.lower()

    # Must contain 5-digit ZIP
    if not re.search(r"\b\d{5}(?:-\d{4})?\b", addr):
        return False

    # Must contain a street number
    if not re.search(r"\b\d{1,6}\b", addr):
        return False

    # Must contain a valid street suffix
    if not re.search(r"(st|street|ave|avenue|blvd|road|rd|drive|dr|lane|ln|court|ct|place|pl)", addr):
        return False

    # Must contain valid US state
    if not any(st.lower() in addr for st in VALID_STATES):
        return False

    return True


# --------------------------------------
# INIT DATABASE
# --------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS labels (
            raw_text TEXT PRIMARY KEY,
            recipient_name TEXT,
            address TEXT
        );
    """)
    conn.commit()
    return conn


# --------------------------------------
# GET EXISTING RESULT
# --------------------------------------
def get_existing_result(raw_text, conn=None):
    conn = conn or sqlite3.connect(DB_NAME)

    row = conn.execute(
        "SELECT recipient_name, address FROM labels WHERE raw_text=?",
        (raw_text,)
    ).fetchone()

    if not row:
        return None

    name, addr = row

    if is_valid_name(name) and is_valid_address(addr):
        return {"recipient_name": name, "address": addr}

    return None


# --------------------------------------
# SAVE RESULT
# --------------------------------------
def save_result(raw_text, name, addr, conn=None):
    conn = conn or sqlite3.connect(DB_NAME)

    # Validate before saving
    if not is_valid_name(name) or not is_valid_address(addr):
        return

    conn.execute(
        "INSERT OR REPLACE INTO labels (raw_text, recipient_name, address) VALUES (?, ?, ?)",
        (raw_text, name, addr)
    )
    conn.commit()


# --------------------------------------
# SYNC CSV TO DB
# --------------------------------------
def refresh_database_from_csv(csv_path="ocr_raw_labels.csv", conn=None):
    conn = conn or sqlite3.connect(DB_NAME)
    df = pd.read_csv(csv_path)

    existing_raw = {
        r[0] for r in conn.execute("SELECT raw_text FROM labels").fetchall()
    }

    for raw in df["raw_text"]:
        raw = str(raw).strip()
        if raw and raw not in existing_raw:
            conn.execute("INSERT OR IGNORE INTO labels(raw_text) VALUES (?)", (raw,))

    conn.commit()
