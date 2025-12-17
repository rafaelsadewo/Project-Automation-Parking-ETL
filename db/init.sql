DROP TABLE IF EXISTS sensor_logs;
DROP TABLE IF EXISTS activity_logs; -- Tambahan baru

-- Tabel untuk Real-Time (Data Grid)
CREATE TABLE sensor_logs (
    id SERIAL PRIMARY KEY,
    slot_id VARCHAR(10) NOT NULL,
    status VARCHAR(20),
    distance_cm FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lokasi VARCHAR(50),
    durasi_menit INTEGER
);

-- Tabel untuk Riwayat (Log Aktivitas)
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    slot_id VARCHAR(10),
    event VARCHAR(50), -- Isinya: "MOBIL MASUK", "MOBIL KELUAR", "ANOMALI DETECTED"
    keterangan VARCHAR(100)
);