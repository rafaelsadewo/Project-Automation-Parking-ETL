import time
import random
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# KONEKSI DATABASE
db_connection_str = 'postgresql://admin:password123@localhost:5432/parking_db'
db_connection = create_engine(db_connection_str)

# KONFIGURASI
JUMLAH_SLOT = 20
LOKASI_PARKIR = "Parkiran Utama FILKOM"

waktu_masuk_kendaraan = {} 

def generate_sensor_data():
    data_log = []     
    current_time = datetime.now()
    
    for i in range(1, JUMLAH_SLOT + 1):
        slot_label = f"P-{i}"
        slot_key = i
        
        is_occupied = slot_key in waktu_masuk_kendaraan
        chance = random.random()
        
        distance = 0
        status = ""
        durasi = 0 
        
        # LOGIKA SIMULASI
        if not is_occupied:
            if chance < 0.1: # Masuk
                waktu_masuk_kendaraan[slot_key] = current_time
                distance = random.uniform(15, 25) 
                status = "TERISI"
            else: # Kosong
                distance = random.uniform(26, 200) 
                status = "KOSONG"
        else:
            if chance < 0.05: # Keluar
                del waktu_masuk_kendaraan[slot_key]
                distance = random.uniform(26, 200)
                status = "KOSONG"
            else: # Diam
                waktu_awal = waktu_masuk_kendaraan[slot_key]
                selisih = current_time - waktu_awal
                durasi = int(selisih.total_seconds()) # Hitung Detik
                
                distance = random.uniform(15, 25)
                status = "TERISI"

        # LOGIKA ANOMALI
        if random.random() < 0.15:  
            distance = random.uniform(0, 14.9)
            durasi = 0 

        # FINAL STATUS CHECK
        if distance < 15:
            status = "ANOMALI"
        elif 15 <= distance <= 25:
            status = "TERISI"
        else:
            status = "KOSONG"

        data_log.append({
            "slot_id": slot_label,
            "status": status,
            "distance_cm": round(distance, 2),
            "timestamp": current_time,
            "lokasi": LOKASI_PARKIR,
            "durasi_menit": durasi 
        })
        
    return data_log

print("--- Simulasi Smart Parking (Mode: Real-Time) ---")

try:
    while True:
        realtime_data = generate_sensor_data()
        
        # Update Database
        df_realtime = pd.DataFrame(realtime_data)
        df_realtime.to_sql('sensor_logs', db_connection, if_exists='replace', index=False)
        
        # Hitung Jumlah Status
        terisi = len(df_realtime[df_realtime['status'] == 'TERISI'])
        kosong = len(df_realtime[df_realtime['status'] == 'KOSONG'])
        anomali = len(df_realtime[df_realtime['status'] == 'ANOMALI'])
        
        # OUTPUT TERMINAL
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] UPDATE \nKosong : {kosong} | Terisi : {terisi} | Error : {anomali}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Simulasi berhenti.")