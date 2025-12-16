# mahasiswa.py

# --- Class Mahasiswa (Enkapsulasi) ---
class Mahasiswa:
    """
    Kelas untuk merepresentasikan data seorang Mahasiswa.
    Menerapkan Enkapsulasi data.
    """
    def __init__(self, nim, nama, email, jurusan, ipk):
        # Menggunakan double underscore __ untuk enkapsulasi (konvensi Python)
        self.__nim = nim
        self.__nama = nama
        self.__email = email
        self.__jurusan = jurusan
        self.__ipk = ipk

    # Metode Getter
    def get_nim(self):
        return self.__nim

    def get_nama(self):
        return self.__nama

    def get_email(self):
        return self.__email

    def get_jurusan(self):
        return self.__jurusan

    def get_ipk(self):
        return self.__ipk

    # Metode Setter
    def set_nama(self, nama_baru):
        self.__nama = nama_baru

    def set_email(self, email_baru):
        self.__email = email_baru

    def set_jurusan(self, jurusan_baru):
        self.__jurusan = jurusan_baru

    def set_ipk(self, ipk_baru):
        self.__ipk = ipk_baru

    def __str__(self):
        return (f"NIM: {self.__nim}, Nama: {self.__nama}, Email: {self.__email}, "
                f"Jurusan: {self.__jurusan}, IPK: {self.__ipk}")

# --- Class Pengguna dan Admin (Pewarisan/Inheritance & Polimorfisme) ---
class Pengguna:
    """Kelas Dasar untuk Pengguna Sistem."""
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def tampilkan_menu(self):
        """Metode dasar yang akan dioverride."""
        print("Selamat datang di Portal Akademik!")

class Admin(Pengguna):
    """Kelas Admin, mewarisi dari Pengguna."""
    def __init__(self, username, password):
        super().__init__(username, password)
            
    def tampilkan_menu(self):
        """Metode khusus untuk Admin (Tidak digunakan di Streamlit)."""
        pass