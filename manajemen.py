# manajemen.py

import re
import csv
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from mahasiswa import Mahasiswa 

# --- Class ManajemenData (Logika Inti) ---
class ManajemenData:
    def __init__(self, nama_file="data_mahasiswa.csv"):
        self.data_mahasiswa = [] 
        self.nama_file = nama_file
        self.muat_data() 

    # --- Penanganan File I/O ---
    def simpan_data(self):
        """Menyimpan data mahasiswa ke file CSV."""
        try:
            with open(self.nama_file, 'w', newline='', encoding='utf-8') as file: 
                writer = csv.writer(file)
                writer.writerow(['NIM', 'Nama', 'Email', 'Jurusan', 'IPK'])
                for mhs in self.data_mahasiswa:
                    writer.writerow([
                        mhs.get_nim(), mhs.get_nama(), mhs.get_email(),
                        mhs.get_jurusan(), mhs.get_ipk()
                    ])
        except IOError as e:
            print(f"❌ Error saat menyimpan file: {e}")

    def muat_data(self):
        """Memuat data mahasiswa dari file CSV."""
        self.data_mahasiswa = []
        try:
            with open(self.nama_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader) 
                for row in reader:
                    if len(row) == 5:
                        try:
                            nim, nama, email, jurusan, ipk = row
                            mhs = Mahasiswa(nim, nama, email, jurusan, float(ipk))
                            self.data_mahasiswa.append(mhs)
                        except ValueError:
                            print(f"⚠️ Peringatan: Data '{row}' memiliki IPK tidak valid dan dilewati.")
            # print("✅ Data berhasil dimuat.") # Komentar untuk Streamlit
        except FileNotFoundError:
            # print("⚠️ File data belum ditemukan.") # Komentar untuk Streamlit
            pass
        except IOError as e:
            print(f"❌ Error saat memuat file: {e}")

    # --- Validasi Input (Regex) ---
    def validasi_email(self, email):
        """Validasi format email menggunakan Regular Expression (Regex)."""
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email, re.IGNORECASE):
            return True
        return False

    def validasi_nim(self, nim):
        """Validasi NIM: 12 digit angka."""
        regex = r'^\d{12}$'
        if re.search(regex, nim):
            return True
        return False
        
    def validasi_ipk(self, ipk_str):
        """Validasi IPK: format angka float antara 0.00 sampai 4.00."""
        try:
            ipk = float(str(ipk_str).replace(',', '.'))
            if 0.00 <= ipk <= 4.00:
                return True, ipk
            return False, None
        except ValueError:
            return False, None

    # --- Operasi CRUD ---
    def tambah_data(self, nim, nama, email, jurusan, ipk_str):
        """Menambahkan objek Mahasiswa baru."""
        if not self.validasi_nim(nim):
            raise ValueError("Format NIM tidak valid. Harus 12 digit angka.")
            
        if any(mhs.get_nim() == nim for mhs in self.data_mahasiswa):
            raise ValueError(f"NIM {nim} sudah terdaftar.")

        if not self.validasi_email(email):
            raise ValueError("Format Email tidak valid.")

        is_valid_ipk, ipk = self.validasi_ipk(ipk_str)
        if not is_valid_ipk:
            raise ValueError("IPK tidak valid. Harus angka antara 0.00 dan 4.00.")

        mahasiswa_baru = Mahasiswa(nim, nama, email, jurusan, ipk)
        self.data_mahasiswa.append(mahasiswa_baru)
        self.simpan_data()

    def cari_index_nim(self, nim):
        """Mencari index objek Mahasiswa berdasarkan NIM."""
        for i, mhs in enumerate(self.data_mahasiswa):
            if mhs.get_nim() == nim:
                return i
        return -1
        
    def edit_data(self, nim, nama=None, email=None, jurusan=None, ipk_str=None):
        """Mengedit data Mahasiswa berdasarkan NIM."""
        index = self.cari_index_nim(nim)
        if index == -1:
            raise ValueError(f"NIM {nim} tidak ditemukan.")

        mhs = self.data_mahasiswa[index]

        if nama:
            mhs.set_nama(nama)
        if email:
            if not self.validasi_email(email):
                raise ValueError("Format Email baru tidak valid.")
            mhs.set_email(email)
        if jurusan:
            mhs.set_jurusan(jurusan)
        if ipk_str:
            is_valid_ipk, ipk = self.validasi_ipk(ipk_str)
            if not is_valid_ipk:
                raise ValueError("IPK baru tidak valid. Harus angka antara 0.00 dan 4.00.")
            mhs.set_ipk(ipk)
            
        self.simpan_data()

    def hapus_data(self, nim):
        """Menghapus data Mahasiswa berdasarkan NIM."""
        index = self.cari_index_nim(nim)
        if index == -1:
            raise ValueError(f"NIM {nim} tidak ditemukan.")

        del self.data_mahasiswa[index]
        self.simpan_data()

    # --- Pencarian Data (Linear Search) ---
    def cari_data(self, kunci_cari, atribut='nim'):
        """Melakukan pencarian data Mahasiswa (Linear Search)."""
        hasil = []
        waktu_mulai = time.time()
        
        for mhs in self.data_mahasiswa:
            try:
                nilai_atribut = getattr(mhs, f'get_{atribut}')()
            except AttributeError:
                nilai_atribut = mhs.get_nim()
                
            if kunci_cari.lower() in str(nilai_atribut).lower():
                hasil.append(mhs)
                
        waktu_akhir = time.time()
        waktu_eksekusi = waktu_akhir - waktu_mulai
        
        return hasil, waktu_eksekusi

    # --- Pengurutan Data (Bubble Sort & Insertion Sort) ---
    def bubble_sort(self, atribut='nim', urutan='asc'):
        """Pengurutan data menggunakan Bubble Sort."""
        n = len(self.data_mahasiswa)
        arr = self.data_mahasiswa[:] 
        waktu_mulai = time.time()

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                key_a = getattr(arr[j], f'get_{atribut}')()
                key_b = getattr(arr[j+1], f'get_{atribut}')()
                
                if atribut == 'ipk':
                     key_a = float(key_a)
                     key_b = float(key_b)

                kondisi_swap = (key_a > key_b) if urutan == 'asc' else (key_a < key_b)

                if kondisi_swap:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swapped = True
            if not swapped:
                break
                
        waktu_akhir = time.time()
        return arr, waktu_akhir - waktu_mulai

    def insertion_sort(self, atribut='nim', urutan='asc'):
        """Pengurutan data menggunakan Insertion Sort."""
        arr = self.data_mahasiswa[:] 
        waktu_mulai = time.time()
        
        for i in range(1, len(arr)):
            key_mhs = arr[i]
            j = i - 1
            
            key_val = getattr(key_mhs, f'get_{atribut}')()
            if atribut == 'ipk':
                key_val = float(key_val)
            
            while j >= 0:
                current_val = getattr(arr[j], f'get_{atribut}')()
                if atribut == 'ipk':
                    current_val = float(current_val)
                
                kondisi_pindah = (current_val > key_val) if urutan == 'asc' else (current_val < key_val)
                
                if kondisi_pindah:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
                    
            arr[j + 1] = key_mhs
            
        waktu_akhir = time.time()
        return arr, waktu_akhir - waktu_mulai

    # --- Fitur Kirim Email ---
    def kirim_email_data(self, penerima_email, subjek="Data Mahasiswa Akademik", pesan_tambahan="Terlampir data mahasiswa terbaru."):
        """Mengirim data mahasiswa yang tersimpan di file CSV sebagai lampiran email."""
        
        # GANTI DENGAN KREDENSIAL ANDA! 
        EMAIL_PENGIRIM = "inibarupli@gmail.com"  
        PASSWORD_PENGIRIM = "kuga ltvf bmdl pkoj" 

        self.simpan_data()

        if EMAIL_PENGIRIM == "email.anda@gmail.com":
            raise Exception("Harap ganti EMAIL_PENGIRIM dan PASSWORD_PENGIRIM di manajemen.py.")

        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_PENGIRIM
            msg['To'] = penerima_email
            msg['Subject'] = subjek

            msg.attach(MIMEText(pesan_tambahan, 'plain'))

            with open(self.nama_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            part.add_header('Content-Disposition', f"attachment; filename= {self.nama_file}")
            
            msg.attach(part)
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() 

            server.login(EMAIL_PENGIRIM, PASSWORD_PENGIRIM) 
            
            server.sendmail(EMAIL_PENGIRIM, penerima_email, msg.as_string())
            
            server.quit()

        except smtplib.SMTPAuthenticationError:
            raise Exception("Autentikasi SMTP gagal. Cek App Password/username/password Gmail Anda.")
        except FileNotFoundError:
            raise Exception(f"File {self.nama_file} tidak ditemukan untuk dilampirkan.")
        except Exception as e:
            raise Exception(f"Gagal mengirim email: {e}")