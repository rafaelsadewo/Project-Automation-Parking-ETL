# Project-Automation-Parking-ETL

# Sistem Parkir Pintar Berbasis IoT (Smart Parking System)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)

**Proyek Akhir Pemrosesan Infrastruktur Data - FILKOM Universitas Brawijaya**

Sistem ini adalah simulasi *End-to-End Data Engineering* untuk memantau kondisi parkiran secara *real-time*. Menggunakan pendekatan **ETL (Extract, Transform, Load)** untuk memproses data sensor simulasi, menyimpannya ke Data Warehouse (PostgreSQL), dan memvisualisasikannya melalui Dashboard interaktif.

## Anggota Tim
[cite_start]Proyek ini disusun oleh[cite: 51]:
* **Rafael Sadewo Ai Sakti** (235150301111029)
* **Ibadurahman Faiz Usman** (235150301111032)
* **Margaretha Eka Melani Saputra** (235150307111017)
* **Muhammad Rasyid Hidayatullah** (235150307111037)

## Fitur Utama
1.  [cite_start]**Real-Time Monitoring:** Memantau status 20 slot parkir (Kosong, Terisi, Anomali)[cite: 77].
2.  **Live Stopwatch Duration:** Menghitung durasi parkir kendaraan detik-demi-detik secara *real-time* (1s, 2s, 3s...).
3.  [cite_start]**Anomaly Detection:** Otomatis mendeteksi kesalahan sensor jika jarak < 15 cm[cite: 154].
4.  [cite_start]**Activity Logging:** Mencatat riwayat keluar-masuk kendaraan dan error sensor ke database[cite: 233].
5.  **REST API Support:** Menyediakan endpoint JSON untuk integrasi dengan aplikasi mobile.

---

## Arsitektur Sistem (ETL Pipeline)
[cite_start]Sistem ini tidak menggunakan pendekatan ELT, melainkan **ETL** untuk menangani logika simulasi yang kompleks[cite: 112].

1.  [cite_start]**Extract (Simulasi Sensor):** Script Python (`simulator.py`) membangkitkan data jarak (*distance*) secara acak untuk 20 slot[cite: 114].
2.  **Transform (Python Pandas):** * Validasi data sensor.
    * Penentuan status: 
        * `< 15 cm` : **ANOMALI** (Error)
        * `15 - 25 cm` : **TERISI** (Mobil)
        * `> 25 cm` : **KOSONG**
    * Perhitungan durasi parkir berbasis waktu nyata.
3.  [cite_start]**Load (PostgreSQL):** Data bersih disimpan ke database `parking_db` dalam container Docker[cite: 114].
4.  [cite_start]**Visualization:** Streamlit membaca data dari database dan menampilkannya[cite: 135].

## Struktur Folder
```text
smart-parking/
├── api/                # Backend API (FastAPI) untuk Mobile Apps
│   └── main.py
├── dashboard/          # Frontend Dashboard (Streamlit)
│   ├── app.py          # Logic tampilan utama
│   ├── components.py   # Komponen UI (Kartu Parkir HTML)
│   └── style.css       # Styling CSS
├── db/                 # Konfigurasi Database
│   └── init.sql        # Script pembuatan tabel awal
├── etl/                # Core System
│   └── simulator.py    # Script ETL & Simulasi Sensor
├── docker-compose.yml  # Konfigurasi Container Docker
└── requirements.txt    # Daftar library Python
```

## Cara Menjalankan Project
Prasyarat
Python 3.9+

Docker & Docker Compose

1. Setup Database (Docker)
Jalankan perintah ini untuk menyiapkan database PostgreSQL:
```
docker-compose up -d
```
Pastikan container parking_db sudah berjalan.

2. Install Library
Install semua kebutuhan Python:
```
pip install -r requirements.txt
```

4. Jalankan Simulator (ETL)
Buka terminal baru dan jalankan simulasi sensor. Script ini harus tetap berjalan agar data terus terupdate.
```
python etl/simulator.py
```
Output: Anda akan melihat log update status parkir setiap detik di terminal.

5. Jalankan Dashboard
Buka terminal baru lagi untuk menjalankan visualisasi web:
```
streamlit run dashboard/app.py
```
Akses dashboard di browser: http://localhost:8501

6. Jalankan API (Opsional)
Jika ingin mengakses data via JSON untuk aplikasi HP:
```
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
Dokumentasi API bisa dilihat di: http://localhost:8000/docs

## Teknologi yang Digunakan
Language: Python

Data Processing: Pandas

Database: PostgreSQL

Infrastructure: Docker

Web Framework: Streamlit

API Framework: FastAPI
ORM: SQLAlchemy
