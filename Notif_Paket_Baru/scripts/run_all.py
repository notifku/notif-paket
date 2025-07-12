# python scripts/run_all.py

import subprocess
import os

# Path base folder kamu
BASE_DIR = "/Users/rayyy/Documents/KERJA/Notif_Paket_Baru"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# ====== Jalankan scraping.py ======
print("🚀 Menjalankan scraping.py ...\n")
scraping_path = os.path.join(SCRIPTS_DIR, "scraping.py")
result_scraping = subprocess.run(["python", scraping_path])

# Cek apakah scraping sukses
if result_scraping.returncode != 0:
    print("\n❌ scraping.py gagal atau error. Hentikan proses.")
    exit(1)

# ====== Jalankan filter_notify.py ======
print("\n🚀 Menjalankan filter_notify.py ...\n")
filter_path = os.path.join(SCRIPTS_DIR, "filter_notify.py")
result_filter = subprocess.run(["python", filter_path])

if result_filter.returncode != 0:
    print("\n❌ filter_notify.py gagal atau error.")
else:
    print("\n✅ Semua proses selesai.")
