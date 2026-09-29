# Steganography Analyzer

Aplikasi desktop dan CLI untuk menyisipkan pesan rahasia ke dalam gambar dengan teknik **LSB (Least Significant Bit)**. Sebelum disisipkan, pesan dienkripsi memakai **AES-256-GCM**. Aplikasi juga menyediakan analisis perbandingan gambar melalui histogram RGB, metrik MSE/PSNR, dan visualisasi LSB.

## Fitur

- Menyisipkan pesan ke gambar RGB dan menyimpan hasil sebagai PNG atau BMP.
- Mengenkripsi pesan dengan AES-256-GCM. Password yang sama diperlukan untuk ekstraksi.
- Mengekstrak dan mendekripsi pesan dari stego image.
- Menghitung kapasitas gambar.
- GUI dengan tab **Embed**, **Analysis**, dan **Extract**, serta CLI berbasis menu.
- Membandingkan cover image (gambar asli) dan stego image (gambar setelah penyisipan).

## Persyaratan

- Python **3.12**.
- Tkinter untuk menjalankan GUI (umumnya tersedia bersama Python di Windows; di Linux mungkin perlu dipasang terpisah).
- Git untuk clone project.

Dependensi Python tercantum di `requirements.txt`: Pillow untuk pemrosesan gambar dan `cryptography` untuk AES-GCM.

## Instalasi dan menjalankan

### 1. Clone project

Buka terminal, lalu jalankan:

```bash
git clone https://github.com/DwiAriaPutra/steganographi.git
cd steganographi
```

### 2. Buat dan aktifkan virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak aktivasi karena kebijakan skrip, gunakan Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Pasang dependensi

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Di Debian/Ubuntu, jika Tkinter belum tersedia, pasang paket sistemnya:

```bash
sudo apt install python3-tk
```

### 4. Jalankan aplikasi

Untuk membuka GUI:

```bash
python -m gui
```

Untuk menjalankan CLI:

```bash
python app.py
```

## Alur kerja GUI

1. **Embed:** pilih cover image, tulis pesan, masukkan stego key, lalu tentukan lokasi output. Aplikasi menampilkan perkiraan kapasitas gambar. Setelah embed berhasil, hasil tersimpan dan tab Analysis diperbarui otomatis.
2. **Analysis:** bandingkan cover dan stego image. Tab ini menampilkan pratinjau, MSE/PSNR, histogram, dan analisis LSB.
3. **Extract:** pilih stego image, masukkan stego key yang sama, kemudian jalankan ekstraksi. Jika data utuh dan kunci benar, pesan asli ditampilkan.

CLI menyediakan menu **Embed message**, **Extract message**, **Check image capacity**, dan **Exit**. Ikuti prompt untuk memasukkan path file, pesan, dan kunci.

## Alur penyisipan dan ekstraksi

Saat penyisipan, aplikasi mengubah pesan teks menjadi byte UTF-8, mengenkripsinya dengan AES-256-GCM, lalu membentuk data berisi header, salt, nonce, ciphertext, dan authentication tag. Password diproses menjadi kunci AES menggunakan PBKDF2-HMAC-SHA256 dengan salt acak. Bit data kemudian ditulis ke bit paling rendah (LSB) channel warna RGB pada posisi pseudorandom yang dibangkitkan dari stego key. Hasil akhirnya adalah stego image.

Saat ekstraksi, aplikasi membangkitkan urutan posisi yang sama dari kunci, membaca header untuk mengetahui panjang payload, mengambil payload, lalu memverifikasi dan mendekripsinya dengan AES-GCM. Kunci yang salah, data yang rusak, atau gambar yang sudah mengalami kompresi lossy dapat menyebabkan ekstraksi gagal.

Setiap piksel RGB menyediakan tiga bit kapasitas, satu bit untuk masing-masing channel merah, hijau, dan biru. Jadi kapasitas mentah adalah `lebar × tinggi × 3` bit. Sebagian kapasitas dipakai oleh header dan data enkripsi; ukuran pesan maksimum yang ditampilkan aplikasi sudah memperhitungkan overhead tersebut. Pesan yang terlalu besar akan ditolak.

## Memahami hasil Analysis

Analisis membandingkan **cover image** (gambar sebelum pesan disisipkan) dengan **stego image** (gambar hasil). Analisis ini membantu melihat perubahan visual dan statistik; hasilnya bukan bukti pasti bahwa sebuah gambar mengandung atau tidak mengandung pesan.

### MSE dan PSNR

- **MSE (Mean Squared Error)** adalah rata-rata kuadrat selisih nilai seluruh channel RGB antara cover dan stego. Nilai rendah berarti perubahan rata-rata kecil; nilai `0` berarti kedua gambar identik.
- **PSNR (Peak Signal-to-Noise Ratio)** menyatakan rasio kualitas dalam desibel (dB), dihitung dari MSE. Untuk MSE yang rendah, PSNR biasanya tinggi dan perubahan gambar relatif kecil. Jika gambar identik, PSNR tak terhingga (`∞ dB`).

### Histogram RGB

Histogram menghitung jumlah piksel pada setiap intensitas **0–255**, terpisah untuk channel merah (R), hijau (G), dan biru (B). Sumbu horizontal menunjukkan intensitas warna, sedangkan sumbu vertikal menunjukkan banyaknya channel piksel pada intensitas tersebut. Grafik cover dan stego dapat dibandingkan untuk melihat perubahan distribusi nilai setelah penyisipan.

Karena LSB mengubah nilai channel paling banyak satu tingkat (contohnya 100 menjadi 101 atau sebaliknya), histogram cover dan stego sering tampak mirip. Perubahan kecil pada bin histogram tidak dengan sendirinya membuktikan adanya pesan. Grafik dapat di-zoom dan digeser; tombol **Zoom LSB** memusatkan tampilan pada intensitas rendah 0–32 untuk pemeriksaan lebih dekat.

### LSB Analysis

LSB adalah bit paling kanan pada representasi biner nilai channel. Contohnya, `100` dalam desimal adalah `01100100` dalam biner dan LSB-nya `0`; mengubah nilai menjadi `101` menghasilkan `01100101`, sehingga hanya nilai paling rendah yang berubah.

Panel LSB menampilkan tiga visualisasi:

- **Cover LSB Plane:** hitam/putih berdasarkan bit LSB cover. Sebuah piksel ditampilkan putih jika setidaknya satu channel RGB memiliki LSB `1`.
- **Stego LSB Plane:** visualisasi yang sama untuk stego image.
- **LSB Difference:** putih jika LSB pada setidaknya satu channel piksel berubah antara cover dan stego; hitam jika tidak ada channel yang berubah.

Perubahan LSB yang tersebar dapat terlihat seperti pola/noise, tetapi tekstur gambar asli juga memengaruhi tampilannya. Karena itu, visualisasi ini sebaiknya dibaca sebagai perbandingan perubahan, bukan sebagai detektor steganografi yang memberi keputusan pasti.

## Catatan penggunaan

- Gunakan PNG atau BMP untuk menyimpan stego image. Keduanya mempertahankan nilai piksel; JPEG dan format lossy lain dapat mengubah bit LSB sehingga pesan tidak bisa dipulihkan.
- Simpan stego key dengan aman. Tanpa kunci yang benar, payload tidak dapat diekstrak dan didekripsi.
- Hasil stego image harus tetap berukuran sama dan tidak boleh diedit atau dikompresi ulang sebelum ekstraksi.
