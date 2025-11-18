import csv
import time
from db_manager import init_db, get_existing_result, save_result, refresh_database_from_csv
from ai_extractor import extract_with_ai

INPUT = "ocr_raw_labels.csv"
OUTPUT = "ocr_structured_output.csv"


def run_pipeline():
    conn = init_db()
    refresh_database_from_csv(conn=conn)

    results = []

    with open(INPUT, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=1):
            raw = row["raw_text"].strip()

            print("-------------------------------------------")
            print(f"🧾 Label #{idx}")

            # -------- DATABASE CHECK (INSTANT) --------
            existing = get_existing_result(raw, conn)
            if existing:
                print("✅ Found in database")
                print("👤 Recipient:", existing["recipient_name"])
                print("🏠 Address:", existing["address"])
                results.append(existing)
                continue

            # -------- AI EXTRACTION --------
            print("🔍 New entry → Extracting with AI...")

            start_time = time.time()
            extracted = extract_with_ai(raw)
            elapsed = time.time() - start_time
            print(f"⏱️ AI Time: {elapsed:.2f}s")

            name = extracted.get("recipient_name")
            addr = extracted.get("address")

            # Save only complete valid results
            if name and addr:
                save_result(raw, name, addr, conn)
                print("✅ Extracted & Saved")
            else:
                print("⚠️ Incomplete extraction. Not saving.")

            print("👤 Recipient:", name)
            print("🏠 Address:", addr)
            results.append({"recipient_name": name, "address": addr})

    # -------- WRITE OUTPUT CSV --------
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["recipient_name", "address"])
        writer.writeheader()
        writer.writerows(results)

    print("\n🎉 Pipeline complete!")
