# scripts/scraping.py

import requests
import pandas as pd
import sys
import os

# Path base folder dinamis (root repo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Pastikan folder data/ ada
os.makedirs(DATA_DIR, exist_ok=True)

# URL API
url = "https://sirup.lkpp.go.id/sirup/caripaketctr/search"

# Headers request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}

# Penampung data
data_list = []

# Parameter pagination
start = 0
length = 100
draw = 2
tahun_anggaran = 2025

sys.stdout.write("Jumlah data yang berhasil diambil: 0")
sys.stdout.flush()

while True:
    # Parameter lengkap agar API merespons
    params = {
        "tahunAnggaran": tahun_anggaran,
        "jenisPengadaan": "",
        "metodePengadaan": "",
        "minPagu": "",
        "maxPagu": "",
        "bulan": "",
        "lokasi": "",
        "kldi": "600,586,590,790,778,587,597,539,545,546",
        "pdn": "",
        "ukm": "",
        "draw": draw,
        "columns[0][data]": "",
        "columns[0][name]": "",
        "columns[0][searchable]": "false",
        "columns[0][orderable]": "false",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "paket",
        "columns[1][name]": "",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "pagu",
        "columns[2][name]": "",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "jenisPengadaan",
        "columns[3][name]": "",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "isPDN",
        "columns[4][name]": "",
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "true",
        "columns[4][search][value]": "",
        "columns[4][search][regex]": "false",
        "columns[5][data]": "isUMK",
        "columns[5][name]": "",
        "columns[5][searchable]": "true",
        "columns[5][orderable]": "true",
        "columns[5][search][value]": "",
        "columns[5][search][regex]": "false",
        "columns[6][data]": "metode",
        "columns[6][name]": "",
        "columns[6][searchable]": "true",
        "columns[6][orderable]": "true",
        "columns[6][search][value]": "",
        "columns[6][search][regex]": "false",
        "columns[7][data]": "pemilihan",
        "columns[7][name]": "",
        "columns[7][searchable]": "true",
        "columns[7][orderable]": "true",
        "columns[7][search][value]": "",
        "columns[7][search][regex]": "false",
        "columns[8][data]": "kldi",
        "columns[8][name]": "",
        "columns[8][searchable]": "true",
        "columns[8][orderable]": "true",
        "columns[8][search][value]": "",
        "columns[8][search][regex]": "false",
        "columns[9][data]": "satuanKerja",
        "columns[9][name]": "",
        "columns[9][searchable]": "true",
        "columns[9][orderable]": "true",
        "columns[9][search][value]": "",
        "columns[9][search][regex]": "false",
        "columns[10][data]": "lokasi",
        "columns[10][name]": "",
        "columns[10][searchable]": "true",
        "columns[10][orderable]": "true",
        "columns[10][search][value]": "",
        "columns[10][search][regex]": "false",
        "columns[11][data]": "id",
        "columns[11][name]": "",
        "columns[11][searchable]": "true",
        "columns[11][orderable]": "true",
        "columns[11][search][value]": "",
        "columns[11][search][regex]": "false",
        "order[0][column]": 5,
        "order[0][dir]": "DESC",
        "start": start,
        "length": length,
        "search[value]": "",
        "search[regex]": "false"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"\n❌ Gagal request: {e}")
        break

    if response.text.strip():
        try:
            data = response.json()
            if "data" in data and data["data"]:
                data_list.extend(data["data"])
                start += length
                sys.stdout.write(f"\rJumlah data yang berhasil diambil: {len(data_list)}")
                sys.stdout.flush()
            else:
                break
        except Exception as e:
            print(f"\n❌ Gagal parsing JSON: {e}")
            break
    else:
        print("\n❌ Respons kosong, hentikan scraping.")
        break

# Konversi ke DataFrame
df = pd.DataFrame(data_list)

# Tampilkan 5 baris pertama
print("\n\nContoh data:")
print(df.head())

# Simpan CSV
output_file = os.path.join(DATA_DIR, "hasil_scrap.csv")
df.to_csv(output_file, index=False)

print(f"\n✅ Scraping selesai. Total data: {len(df)} baris.")
print(f"✅ Data disimpan di: {output_file}")

