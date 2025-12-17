# Modul Komponen UI
# Digunakan untuk memisahkan kode HTML dari logika utama (app.py)

def html_card_parkir(slot_id, icon, jarak, info_text, bg_color):
    """
    Membuat string HTML untuk kartu slot parkir.
    
    Args:
        slot_id (str): Label slot (P-1, P-2, dst)
        icon (str): Teks icon singkat (TERISI, KOSONG, ERR)
        jarak (float): Data jarak sensor
        info_text (str): Keterangan status/durasi
        bg_color (str): Warna background (HEX code)
        
    Returns:
        str: Kode HTML siap render
    """
    return f"""
    <div class="card-container" style="background-color: {bg_color};">
        <div class="slot-id">{slot_id}</div>
        <div class="icon-display">{icon}</div>
        <div class="metric-label">Jarak: {jarak} cm</div>
        <div class="metric-value">{info_text}</div>
    </div>
    """