import os
import zipfile
from shared.s3_upload import upload_file_to_s3
from shared.mytime import utc_now


LOG_DIR = "logs"
LOG_FILES = ["bids.log", "impressions.log", "clicks.log"]

def rotate_logs():
    now = utc_now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")

    for log_file in LOG_FILES:
        full_path = os.path.join(LOG_DIR, log_file)
        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
            zip_name = f"{log_file.replace('.log', '')}-{timestamp}.zip"
            zip_path = os.path.join(LOG_DIR, zip_name)

            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(full_path, arcname=log_file)

            upload_file_to_s3(zip_path, f"logs/{os.path.basename(zip_path)}")

            # Truncate the original log file
            with open(full_path, "w"):
                pass

            print(f"[Log Rotator] Archived {log_file} -> {zip_name}")

# def start_log_rotation(interval_seconds: int = 300):
#     def loop():
#         while True:
#             rotate_logs()
#             time.sleep(interval_seconds)
#
#     import threading
#     threading.Thread(target=loop, daemon=True).start()
