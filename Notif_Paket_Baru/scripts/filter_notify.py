# scripts/filter_notify.py

import pandas as pd
import os
import sys
from utils import send_telegram

# ========= PATH ===========
BASE_DIR = "/Users/rayyy/Documents/KERJA/Notif_Paket_Baru"
DATA_DIR = os.path.join(BASE_DIR, "data")
hasil_scrap_file = os.path.join(DATA_DIR, "hasil_scrap.csv")
master_file = os.path.join(DATA_DIR, "data_master.csv")

# ========= KATA KUNCI ===========
keyword_list = [
    'computer', 'komputer', 'smart', 'peralatan', 'mesin', 'studio', 'teknologi', 'olah data', 
    'alat peraga', 'laptop', 'sinyal', 'server', 'audio', 'videotron', 'chromebook', 
    'digital', 'perlengkapan', 'elektronik', 'electronik', 'interactive', 
    'papan tulis digital', 'peralatan praktik', 'board', 'video', 'jaringan', 'sarana prasarana', 
    '4G', '5G', 'satelit', 'station', 'internet', 'komunikasi', 'sistem', 'system', 
    'aplikasi', 'tv', 'robotik', 'cloud', 'printer', 'analisis', 'otomatis', 'simulator', 'film', 
    'telepon', 'smartphone', 'navigasi', 'electric', 'pendingin', 'software', 'database', 'storage', 
    'perangkat lunak', 'drone', 'seluler', 'laptop', 'teknologi', 'notebook', 'air conditioner', 'ac split', 
    'genset', 'scanner', 'cctv', 'printing', 'mainframe', 'mesin hitung', 'dispenser', 'aio', 'acer', 'advan', 
    'asus', 'lenovo', 'all in one', 'desktop', 'axioo', 'zyrex', 'macbook', 'apple', 'samsung', 'toshiba', 'altyk', 
    'alienware', 'dell', 'hp', 'Microsoft', 'infinix', 'xiaomi', 'msi', 'huawei', 'Hewlett-Packard', 'razer', 
    'Gigabyte', 'daikin', 'sharp', 'Panasonic', 'daikin', 'samsung', 'mitsubishi electric', 'panasonic', 'gree', 
    'carrier', 'toshiba', 'aqua', 'frigidaire', 'hisense', 'samsung', 'sharp', 'hitachi', 'mitsubishi electric', 
    'haier', 'bosch', 'electrolux', 'toshiba', 'whirlpool', 'kelvinator', 'sanyo', 'fisher & paykel', 'ge appliances', 
    'smart technologies', 'promethean', 'benq', 'viewsonic', 'sharp', 'epson', 'cisco', 'clevertouch', 
    'vizio', 'polycom', 'maxhub', 'dell emc', 'hewlett packard enterprise', 'lenovo', 'cisco', 'ibm', 'supermicro', 
    'fujitsu', 'huawei', 'acer', 'oracle', 'gigabyte', 'inspur','command center','leptop','cetak','perlengkapan','fasilitas',
    'jasa', 'genset','generator','interaktif','interactive','smartboard','vidiotron','server','informasi','brankas','videotron'
    'meubelair', 'meja', 'kursi', 'lemari', 'rak', 'furnitur', 'furniture',
    'partisi', 'sofa', 'meja kerja', 'meja rapat', 'kursi kerja', 'brankas',
    'lemari arsip', 'rak buku', 'rak arsip', 'loker', 'meja komputer','mebel',
    'alat kesehatan', 'peralatan kesehatan', 'alkes',
    'kesehatan', 'puskesmas', 'rumah sakit', 'klinik', 'posyandu', 'dokter',
    'obat', 'obat-obatan', 'vitamin', 'vaksin', 'desinfektan', 'antiseptik',
    'masker', 'sarung tangan', 'hazmat', 'alat pelindung diri', 'apd', 'handsanitizer',
    'tensimeter', 'stetoskop', 'termometer', 'oximeter', 'alat suntik',
    'spuit', 'jarum suntik', 'infus', 'selang infus', 'kantong infus',
    'tabung oksigen', 'masker oksigen', 'nebulizer', 'alat bantu napas',
    'kursi roda', 'ranjang pasien', 'meja periksa', 'brankar',
    'rapid test', 'swab antigen', 'alat tes covid', 'alat tes darah', 'glukometer',
    'centrifuge', 'microscope', 'alat uji urin', 'inkubator medis', 'reagen',
    'walker', 'kruk', 'tongkat bantu', 'hearing aid', 'alat bantu dengar',
    'suction', 'kasur medis', 'bedpan', 'perlak medis', 'tisu medis',
    'botol urin', 'alas tempat tidur pasien', 'alat operasi', 'lampu operasi', 'meja operasi', 'monitor jantung',
    'defibrillator', 'alat bedah', 'alat steril', 'autoclave', 'alat EKG', 'alat USG',
    'proyektor', 'microphone', 'modem', 'router', 'switch', 'hub', 'monitor', 'sound', 'speaker', 
    'headset', 'projector', 'smart tv', 'touchscreen', 'pengolah data', 'earphone', 'power supply',
    'stabilizer', 'inverter', 'perangkat input', 'perangkat output', 'monitor pasien', 'infusion pump',
    'electrocardiograph', 'ekg', 'x-ray', 'ronde trolley', 'lemari obat', 'blood warmer', 'anestesi', 
    'neonatal', 'oksigen konsentrator', 'dental unit', 'alat gigi', 'otoskop', 'ophthalmoscope',
    'meja laboratorium', 'kursi pasien', 'alat steril', 'alat laboratorium', 'lab kit', 'refrigerator medis',
    'meja sidang', 'podium', 'meja belajar', 'kursi belajar',
    'meja resepsionis', 'meja operator', 'rak besi', 'lemari besi', 'kabinet', 'filling cabinet',
    'lemari dokumen'
]

# ========= LOAD DATA ===========
if not os.path.exists(hasil_scrap_file):
    print("❌ File hasil_scrap.csv belum ada. Silakan jalankan scraping.py dulu.")
    sys.exit(1)

df_scrap = pd.read_csv(hasil_scrap_file, dtype=str)

if os.path.exists(master_file):
    df_master = pd.read_csv(master_file, dtype=str)
    existing_ids = set(df_master["id"].astype(str))
else:
    df_master = pd.DataFrame(columns=df_scrap.columns)
    existing_ids = set()

# ========= FILTER ===========
new_rows = []
count_new = 0
count_with_keyword = 0
count_pagu_above = 0

for idx, row in df_scrap.iterrows():
    id_paket = str(row.get("id", "")).strip()
    nama_paket = str(row.get("paket", "")).lower()
    pagu_raw = str(row.get("pagu", "0")).replace(".", "").replace(",", "")
    try:
        pagu = int(float(pagu_raw))
    except:
        pagu = 0

    # Sudah ada di master
    if id_paket in existing_ids:
        continue

    count_new += 1

    has_keyword = any(keyword in nama_paket for keyword in keyword_list)
    if has_keyword:
        count_with_keyword += 1

    if pagu > 100_000_000:
        count_pagu_above += 1

    # Filter final
    if not has_keyword:
        continue
    if pagu <= 100_000_000:
        continue

    # Jika lolos semua
    new_rows.append(row)

    # ========= Kirim Notifikasi ===========
    message = (
        f"*Paket Baru*\n\n"
        f"*ID:* `{id_paket}`\n"
        f"*Paket:* {row.get('paket','-')}\n"
        f"*Pagu:* Rp{pagu:,.0f}\n"
        f"*Satuan Kerja:* {row.get('satuanKerja','-')}\n"
        f"*KLDI:* {row.get('kldi','-')}"
    )
    send_telegram(message)

# ========= Update Master ===========
if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_master = pd.concat([df_master, df_new], ignore_index=True)
    df_master.to_csv(master_file, index=False)

# ========= Ringkasan ===========
print("\n✅ Hasil Filter:")
print(f"- Data baru ditemukan: {count_new}")
print(f"- Mengandung kata kunci: {count_with_keyword}")
print(f"- Pagu >100jt: {count_pagu_above}")
print(f"- Lolos filter & dikirim notifikasi: {len(new_rows)}")

if not new_rows:
    print("\n✅ Tidak ada tender baru yang memenuhi kriteria.")
