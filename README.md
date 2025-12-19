🎓 Aplikasi Manajemen Data Mahasiswa (Streamlit)
Proyek ini adalah sistem manajemen data mahasiswa sederhana yang diimplementasikan sebagai aplikasi web interaktif menggunakan framework Streamlit, dan dibangun menggunakan prinsip-prinsip Pemrograman Berorientasi Objek (OOP) di Python.

✨ Fitur Utama
Proyek ini mencakup implementasi lengkap dari berbagai aspek ilmu komputer, termasuk struktur data, algoritma, dan web development:
1. Antarmuka Web Interaktif: Dibangun dengan Streamlit, memungkinkan administrator mengelola data melalui dashboard yang intuitif tanpa perlu coding.
2. CRUD Operations: Fungsionalitas penuh untuk Create (Tambah), Read (Lihat), Update (Edit), dan Delete (Hapus) data mahasiswa.
3. Penerapan OOP:
  - Encapsulation: Menggunakan kelas Mahasiswa dengan getter dan setter untuk melindungi integritas data.
  - Inheritance: Menggunakan kelas Admin yang mewarisi dari Pengguna.
4. Algoritma Pencarian & Pengurutan:
  - Pencarian: Menerapkan Linear Search untuk menemukan data berdasarkan NIM, Nama, atau Jurusan dengan kompleksitas waktu O(n).
  - Pengurutan: Menerapkan algoritma Bubble Sort dan Insertion Sort untuk mengurutkan data berdasarkan IPK, NIM, atau Nama.
5. Validasi & Keamanan Data: Menerapkan Regular Expression (Regex) untuk validasi format NIM, Email, dan rentang IPK (0.00 - 4.00), memastikan data yang disimpan valid.
6. File I/O & Persistensi Data: Menggunakan file CSV (data_mahasiswa.csv) sebagai database sederhana untuk menyimpan data secara permanen.
7. Fitur Email: Fungsionalitas untuk mengirim data mahasiswa yang tersimpan (sebagai lampiran CSV) ke alamat email tertentu menggunakan library smtplib.

🛠️ Teknologi yang Digunakan
1. Bahasa Pemrograman: Python
2. Framework Web: Streamlit
3. Library Pendukung: pandas, re (Regex), csv, smtplib (Email)

⚙️ Cara Menjalankan Projek Secara Lokal
Untuk menjalankan proyek ini di mesin Anda, ikuti langkah-langkah berikut:
Prasyarat
- Python terinstal.
- Git terinstal.
1. Clone Repository
  Bash : git clone <URL REPOSITORY ANDA>
       cd Manajemen-Mahasiswa-Streamlit
2. Instal Dependensi
  Bash : pip install -r requirements.txt
3. Konfigurasi (Opsional)
Jika Anda ingin menguji fitur Kirim Email, ubah variabel EMAIL_PENGIRIM dan PASSWORD_PENGIRIM di file manajemen.py dengan kredensial Gmail dan App Password Anda.
4. Jalankan Aplikasi
Gunakan perintah python -m untuk menjalankan aplikasi Streamlit:
   Bash : python -m streamlit run app_streamlit.py
Aplikasi akan terbuka secara otomatis di browser Anda.
6. Detail Login
Username: admin
Password: admin123

📂 Struktur Folder Proyek
algooo/
├── .gitignore               # Daftar file yang tidak diunggah ke GitHub
├── README.md                # Deskripsi dan panduan penggunaan proyek
├── requirements.txt         # Daftar library Python yang dibutuhkan (streamlit, pandas)
├── data_mahasiswa.csv       # File database lokal (otomatis terbuat/terisi)
│
├── mahasiswa.py             # Model: Definisi class Mahasiswa (OOP)
├── manajemen.py             # Logic: Fungsi CRUD, Sorting, Searching, & Email
├── app_streamlit.py         # View/UI: Antarmuka web utama Streamlit
│
├── logo_kampus.png          # Aset: Logo untuk sidebar (pastikan nama sesuai kode)
└── background_image.jpg     # Aset: Foto latar belakang (pastikan nama sesuai kode)


