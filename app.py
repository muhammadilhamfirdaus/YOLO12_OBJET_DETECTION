from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Koneksi ke MySQL (XAMPP)
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,  # atau 3306 kalau default
    user="root",
    password="",
    database="yolo_tracking"
)

@app.route("/")
def dashboard():
    cursor = conn.cursor()

    # Hitung total BOX naik/turun
    cursor.execute("SELECT direction, COUNT(*) FROM box_tracking GROUP BY direction")
    counts = dict(cursor.fetchall())
    box_up = counts.get("UP", 0)
    box_down = counts.get("DOWN", 0)

    # Ambil data harian untuk grafik
    cursor.execute("""
        SELECT DATE(timestamp) as date, direction, COUNT(*) 
        FROM box_tracking 
        GROUP BY DATE(timestamp), direction
        ORDER BY date
    """)
    rows = cursor.fetchall()

    # Format data untuk grafik
    daily_data = {}
    for date, direction, count in rows:
        date_str = str(date)
        if date_str not in daily_data:
            daily_data[date_str] = {"UP": 0, "DOWN": 0}
        daily_data[date_str][direction] = count

    dates = list(daily_data.keys())
    ups = [daily_data[d].get("UP", 0) for d in dates]
    downs = [daily_data[d].get("DOWN", 0) for d in dates]

    # Ambil 10 pelanggaran terakhir
   # Ambil 10 pelanggaran terakhir
    cursor.execute("""
        SELECT timestamp, track_id, violation_type, image_path 
        FROM apd_violations 
        ORDER BY timestamp DESC 
        LIMIT 10
    """)
    violations = cursor.fetchall()

    return render_template("dashboard.html",
                       box_up=box_up,
                       box_down=box_down,
                       dates=dates,
                       ups=ups,
                       downs=downs,
                       violations=violations)


if __name__ == "__main__":
    app.run(debug=True)
