import streamlit as st
import pandas as pd
import time
from sqlalchemy import create_engine, text
from components import html_card_parkir 

st.set_page_config(page_title="Smart Parking FILKOM", layout="wide")

# CSS Styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
try:
    local_css("dashboard/style.css") 
except FileNotFoundError:
    pass

# Koneksi Database
db_connection_str = 'postgresql://admin:password123@localhost:5432/parking_db'
db_connection = create_engine(db_connection_str)

# State Memory untuk Log
if 'last_status' not in st.session_state:
    st.session_state['last_status'] = {}

def update_activity_log(df_baru):
    """Mencatat Log hanya jika STATUS berubah (Masuk/Keluar/Anomali)"""
    current_time = pd.to_datetime('now')
    log_entries = []
    
    for index, row in df_baru.iterrows():
        slot_id = row['slot_id']
        status_baru = row['status']
        jarak = row['distance_cm']
        
        # Cek status sebelumnya
        status_lama = st.session_state['last_status'].get(slot_id, "INIT")
        
        # Jika Status Berubah (Durasi nambah TIDAK dianggap perubahan status)
        if status_baru != status_lama and status_lama != "INIT":
            event = ""
            keterangan = ""
            
            if status_baru == "TERISI":
                event = "MOBIL MASUK"
                keterangan = "Kendaraan check-in"
            elif status_baru == "KOSONG":
                event = "MOBIL KELUAR"
                keterangan = "Selesai parkir"
            elif status_baru == "ANOMALI":
                event = "ANOMALI SENSOR"
                keterangan = f"Jarak tidak wajar: {jarak} cm"
            
            if event:
                log_entries.append({
                    "waktu": current_time,
                    "slot_id": slot_id,
                    "event": event,
                    "keterangan": keterangan
                })
        
        # Update memori status terakhir
        st.session_state['last_status'][slot_id] = status_baru
        
    if log_entries:
        df_log = pd.DataFrame(log_entries)
        df_log.to_sql('activity_logs', db_connection, if_exists='append', index=False)

# SIDEBAR
st.sidebar.title("NAVIGASI")
pilihan_menu = st.sidebar.radio("Pilih Menu:", ["Monitoring Real-Time", "Log Aktivitas"])
st.sidebar.markdown("---")
st.sidebar.info("Sistem Parkir Pintar v1.0\nProject Infrastruktur Data")

# HALAMAN 1: MONITORING
if pilihan_menu == "Monitoring Real-Time":
    st.title("Dashboard Monitoring Parkir")
    placeholder = st.empty()

    while True:
        # Cek perpindahan menu agar loop berhenti jika user pindah halaman
        if st.session_state.get('pilihan_sebelumnya') != pilihan_menu:
            st.session_state['pilihan_sebelumnya'] = pilihan_menu
            st.rerun()

        try:
            with db_connection.connect() as conn:
                # Ambil data terbaru
                df = pd.read_sql("SELECT * FROM sensor_logs", conn)
                
                # Cek perubahan status untuk Log
                update_activity_log(df)
                
                # Hitung Statistik
                query_analisis = text("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN status = 'TERISI' THEN 1 ELSE 0 END) as terisi,
                        SUM(CASE WHEN status = 'KOSONG' THEN 1 ELSE 0 END) as kosong,
                        SUM(CASE WHEN status = 'ANOMALI' THEN 1 ELSE 0 END) as anomali
                    FROM sensor_logs
                """)
                res = conn.execute(query_analisis).fetchone()
                total, terisi, kosong, anomali = res[0], res[1], res[2], res[3]

            # Sorting P-1 s/d P-20
            df['sort_key'] = df['slot_id'].apply(lambda x: int(x.split('-')[1]) if '-' in x else 0)
            df = df.sort_values('sort_key')
            
            with placeholder.container():
                lokasi_str = df['lokasi'].iloc[0] if not df.empty else "Unknown"
                last_update = pd.to_datetime(df['timestamp'].iloc[0]).strftime('%H:%M:%S') if not df.empty else "-"
                st.info(f"Lokasi: **{lokasi_str}** | Last Update: **{last_update}**")

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Slot", total)
                c2.metric("Terisi", terisi, delta_color="inverse")
                c3.metric("Kosong", kosong, delta_color="normal")
                c4.metric("Anomali", anomali, delta_color="off")
                st.markdown("---")

                # Grid Layout Kartu Parkir
                cols = st.columns(4) 
                for index, row in df.iterrows():
                    s_id = row['slot_id']
                    status = row['status']
                    jarak = row['distance_cm']
                    durasi_detik = row['durasi_menit'] # Nilai aslinya detik
                    
                    bg, icon, txt = "#607D8B", "UNK", "Unknown"
                    
                    if status == "KOSONG": 
                        bg, icon, txt = "#2E7D32", "FREE", "Siap Digunakan"
                    elif status == "TERISI": 
                        bg = "#C62828"
                        icon = "CAR"
                        
                        # [FORMAT STOPWATCH REAL-TIME]
                        if durasi_detik < 60:
                            txt = f"⏱ {durasi_detik} sec"
                        else:
                            menit = durasi_detik // 60
                            detik = durasi_detik % 60
                            txt = f"⏱ {menit}m {detik}s"
                            
                    elif status == "ANOMALI": 
                        bg, icon, txt = "#FF8F00", "ERR", "SENSOR ERROR!"

                    with cols[index % 4]:
                        html_code = html_card_parkir(s_id, icon, jarak, txt, bg)
                        st.markdown(html_code, unsafe_allow_html=True)
            
            # Refresh Dashboard setiap 1 detik
            time.sleep(1)

        except Exception as e:
            st.error(f"Error koneksi: {e}")
            time.sleep(5)

# HALAMAN 2: LOG AKTIVITAS
elif pilihan_menu == "Log Aktivitas":
    st.title("Log Keluar Masuk & Anomali")
    if st.button("Refresh Data Log"):
        st.rerun()

    try:
        query_log = "SELECT * FROM activity_logs ORDER BY waktu DESC LIMIT 100"
        df_log = pd.read_sql(query_log, db_connection)
        
        if not df_log.empty:
            df_log['waktu'] = pd.to_datetime(df_log['waktu']).dt.strftime('%d-%m-%Y %H:%M:%S')
            st.dataframe(df_log, use_container_width=True, hide_index=True)
        else:
            st.warning("Belum ada data aktivitas.")
    except Exception as e:
        st.error("Gagal mengambil data log.")