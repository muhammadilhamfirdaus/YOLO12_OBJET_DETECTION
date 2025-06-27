import cv2
import os
from ultralytics import YOLO
import cvzone
import mysql.connector
from datetime import datetime

# ======== KONEKSI KE MYSQL ========
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="",
    database="yolo_tracking"
)
cursor = conn.cursor()

# ======== SIMPAN TRACKING BOX ========
def log_to_mysql(box_id, direction):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
            INSERT INTO box_tracking (timestamp, box_id, direction, duration)
            VALUES (%s, %s, %s, %s)
        '''
        values = (timestamp, int(box_id), direction, 0.0)
        cursor.execute(query, values)
        conn.commit()
        print(f"✅ BOX {direction} | ID={box_id} | {timestamp}")
    except Exception as e:
        print(f"❌ Gagal simpan box_tracking: {e}")

# ======== SIMPAN PELANGGARAN NON_VEST ========
def log_violation(track_id, label, frame=None):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"static/violations/{timestamp.replace(':', '-').replace(' ', '_')}_id{track_id}.jpg"
        if frame is not None:
            os.makedirs("static/violations", exist_ok=True)
            cv2.imwrite(filename, frame)

        query = '''
            INSERT INTO apd_violations (timestamp, track_id, violation_type, image_path)
            VALUES (%s, %s, %s, %s)
        '''
        values = (timestamp, int(track_id), label, filename)
        cursor.execute(query, values)
        conn.commit()
        print(f"🚨 NON_VEST | ID={track_id} | {timestamp}")
    except Exception as e:
        print(f"❌ Gagal simpan apd_violations: {e}")

# ======== INISIALISASI YOLO MODEL ========
model = YOLO('best3.pt')
names = model.names
cv2.namedWindow("RGB")

# ======== VIDEO SOURCE ========
cap = cv2.VideoCapture("box.mp4")

line_y = 326
frame_count = 0
hist = {}
box_up = 0
box_down = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 3 != 0:
        continue

    frame = cv2.resize(frame, (1020, 500))
    results = model.track(frame, persist=True)

    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.int().cpu().tolist()

        for track_id, box, class_id in zip(ids, boxes, class_ids):
            x1, y1, x2, y2 = box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            label = names[class_id].upper()

            if label == "NON_VEST":
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"{label} [{track_id}]", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                log_violation(track_id, label, frame)

            elif label == "VEST":
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            elif label == "BOX":
                if track_id in hist:
                    prev_cx, prev_cy = hist[track_id]

                    if prev_cy < line_y <= cy:
                        box_up += 1
                        log_to_mysql(track_id, "UP")
                        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    if prev_cy > line_y >= cy:
                        box_down += 1
                        log_to_mysql(track_id, "DOWN")
                        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

                hist[track_id] = (cx, cy)

    # ======== TAMPILKAN INFO GARIS DAN STATISTIK ========
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 255, 255), 2)
    cvzone.putTextRect(frame, f'BOX_UP: {box_up}', (30, 40), 2, 2)
    cvzone.putTextRect(frame, f'BOX_DOWN: {box_down}', (30, 140), 2, 2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# ======== TUTUP SEMUA ========
cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
