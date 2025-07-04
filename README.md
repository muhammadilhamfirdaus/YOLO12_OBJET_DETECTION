
# 📦 YOLO Box Tracking & APD Violation Monitoring

Proyek ini merupakan sistem deteksi dan pemantauan otomatis menggunakan model YOLO (You Only Look Once) untuk:

- 📦 Mendeteksi dan menghitung jumlah **box** (naik & turun) secara real-time.
- 👷‍♂️ Mendeteksi pelanggaran penggunaan **rompi/APD (Alat Pelindung Diri)**.
- 📊 Menyajikan data dalam bentuk **dashboard interaktif** (jumlah box per hari & notifikasi pelanggaran).

---

## 🔧 Teknologi yang Digunakan

- [YOLOv12 (Ultralytics)](https://github.com/ultralytics/ultralytics) - Model deteksi objek.
- `OpenCV` + `cvzone` - Untuk visualisasi dan pengolahan video real-time.
- `MySQL` - Penyimpanan data pelacakan & pelanggaran.
- `Flask` - Backend untuk mengakses data dan menampilkan dashboard.
- `Chart.js` - Visualisasi grafik box.
- HTML/CSS (Responsive) - Tampilan dashboard.

---

## 🚀 Fitur Utama

### 1. 🎯 Deteksi & Hitung Box

- Sistem dapat mendeteksi objek berlabel `BOX` dari video.
- Melacak arah pergerakan: `UP` (naik) dan `DOWN` (turun).
- Menyimpan log ke MySQL setiap kali box melewati garis.

### 2. 🚨 Deteksi APD (Rompi)

- Mendeteksi apakah seseorang memakai `VEST` atau tidak (`NON_VEST`).
- Jika ditemukan pelanggaran (`NON_VEST`), maka:
  - Kotak merah akan muncul pada objek.
  - Data pelanggaran (waktu, ID, jenis) dan **gambar snapshot** akan disimpan ke database.

### 3. 📊 Dashboard Kontrol

Menampilkan data pelacakan secara visual:

- **Statistik BOX UP dan DOWN** terkini.
- **Grafik harian** jumlah box per tanggal.
- **Tabel notifikasi pelanggaran rompi (APD)** terbaru, lengkap dengan:
  - Waktu kejadian
  - ID pelanggar
  - Jenis pelanggaran
  - Gambar bukti (klik untuk memperbesar)

---

## 🗂️ Struktur Database

### Table: `box_tracking`
| Field       | Tipe Data      |
|-------------|----------------|
| id          | INT (AUTO_INCREMENT) |
| timestamp   | DATETIME       |
| box_id      | INT            |
| direction   | ENUM('UP','DOWN') |
| duration    | FLOAT          |

### Table: `apd_violations`
| Field           | Tipe Data      |
|------------------|----------------|
| id               | INT (AUTO_INCREMENT) |
| timestamp        | DATETIME       |
| track_id         | INT            |
| violation_type   | VARCHAR(255)   |
| image_path       | VARCHAR(255) _(opsional)_ |

---

## 📁 Cara Menjalankan

1. Pastikan Python dan MySQL sudah terinstall.
2. Install dependensi:

```bash
pip install ultralytics opencv-python mysql-connector-python flask cvzone
```

3. Jalankan skrip deteksi:

```bash
python main.py
```

4. Jalankan Flask app untuk dashboard:

```bash
python app.py
```

5. Buka browser: `http://localhost:5000`

---

## 📌 Catatan Tambahan

- Dataset model YOLO harus dilatih terlebih dahulu untuk mengenali `BOX`, `VEST`, dan `NON_VEST`.
- Gambar pelanggaran bisa disimpan dari `cv2.imwrite()` saat pelanggaran terdeteksi.
- Untuk keperluan pengujian, bisa digunakan video sample (misal: `box.mp4`).

---

## 📷 Tampilan Dashboard

![xampp](img/dashboard_box.png)
![xampp](img/dashboard_vest.png)
![xampp](img/vest.png)

## 📷 Tampilan Object Detection
![xampp](img/object.jpeg)

---

## 🙌 Kontributor
- Muhammad Ilham Firdaus (312310021)
- Indra Maha Resi (312310044)
- Alisya Katsulya Syaukani (312310046)
- Reza Fadlillah Ardi (312310032)
