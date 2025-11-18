import time, os, subprocess

csv = "ocr_raw_labels.csv"
last_modified = os.path.getmtime(csv)

print("👀 Watching for dataset changes...")
while True:
    new_time = os.path.getmtime(csv)
    if new_time != last_modified:
        print("📂 Dataset changed — refreshing database and warming model...")
        subprocess.run(["python", "db_manager.py"])
        subprocess.run(["python", "optimize_for_speed.py"])
        last_modified = new_time
    time.sleep(5)
