from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
import pandas as pd

# Inisialisasi FastAPI
app = FastAPI(title="Smart Parking API")

# KONFIGURASI CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Koneksi Database
db_connection_str = 'postgresql://admin:password123@localhost:5432/parking_db'
db_connection = create_engine(db_connection_str)

@app.get("/monitor", response_class=HTMLResponse)
def monitor_view():
    """
    Endpoint Visual: Menampilkan HTML dengan untuk mantau status API real-time
    """
    return """
    <html>
        <head>
            <title>API Real-time Monitor</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: sans-serif; padding: 20px; background: #222; color: #fff; }
                .box { border: 1px solid #555; padding: 10px; margin: 5px; border-radius: 5px; }
                .TERISI { background-color: #C62828; }
                .KOSONG { background-color: #2E7D32; }
                .ANOMALI { background-color: #FF8F00; color: black; }
            </style>
        </head>
        <body>
            <h2>📡 API Live Data</h2>
            <div id="container">Loading data...</div>

            <script>
                // Polling data ke API /status setiap 1 detik
                setInterval(async () => {
                    try {
                        const response = await fetch('/status');
                        const data = await response.json();
                        
                        let html = "";
                        data.forEach(slot => {
                            html += `
                            <div class="box ${slot.status}">
                                <b>${slot.slot_id}</b>: ${slot.status} <br>
                                <small>Jarak: ${slot.distance_cm} cm</small>
                            </div>`;
                        });
                        document.getElementById("container").innerHTML = html;
                        
                    } catch (e) {
                        console.log(e);
                    }
                }, 1000);
            </script>
        </body>
    </html>
    """

@app.get("/")
def read_root():
    """Endpoint root untuk cek status server"""
    return {"message": "Server Smart Parking Online!", "location": "Parkiran FILKOM"}

@app.get("/status")
def get_parking_status():
    """
    Endpoint Data: Kembaliin data JSON buat slot parkir
    """
    with db_connection.connect() as conn:
        df = pd.read_sql("SELECT * FROM sensor_logs", conn)
        # Sorting data
        df['sort_key'] = df['slot_id'].apply(lambda x: int(x.split('-')[1]) if '-' in x else 0)
        df = df.sort_values('sort_key')
        # Convert DataFrame ke JSON
        result = df.to_dict(orient="records")

    return result
