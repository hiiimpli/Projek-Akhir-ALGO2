# app_streamlit.py (VERSI FINAL DENGAN LOGO DAN BACKGROUND)

import streamlit as st
import time
import pandas as pd
from manajemen import ManajemenData
import base64 # Import baru untuk base64 encoding

# --- CSS Injection Function ---
def add_bg_from_local(image_file):
    """Fungsi untuk menambahkan background image menggunakan CSS"""
    # Menentukan MIME type berdasarkan ekstensi (asumsi jpg/png)
    mime_type = 'jpeg' if image_file.lower().endswith(('.jpg', '.jpeg')) else 'png'

    try:
        with open(image_file, "rb") as image:
            # Mengenkode gambar ke base64 string untuk digunakan di CSS
            encoded_string = base64.b64encode(image.read()).decode()
        
        # Injeksi CSS ke Streamlit
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{mime_type};base64,{encoded_string}");
            background-size: cover; /* Memastikan gambar menutupi seluruh area */
            background-attachment: fixed; /* Memastikan background tidak bergerak saat scroll */
            background-repeat: no-repeat;
        }}
        /* Menyesuaikan warna teks/konten agar mudah dibaca di atas background gelap */
        h1, h2, h3, h4, .stSidebar * {{ 
            color: black; /* Ganti dengan warna yang lebih cocok (misal: white) jika background gelap */
        }}
        .stApp {{
            color: black; 
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Background image '{image_file}' not found. Please check filename.")

# --- Fungsi Utility ---
def get_manager():
    if 'manager' not in st.session_state:
        st.session_state['manager'] = ManajemenData()
    return st.session_state['manager']

def is_logged_in():
    return st.session_state.get('logged_in', False)

# --- View: Form Login Sederhana ---
def view_login():
    # Logo di halaman login
    try:
        st.image("logo_kampus.png", width=100)
    except FileNotFoundError:
        st.warning("Logo file 'logo_kampus.png' not found.")
        
    st.title("PORTAL AKADEMIK SMDM")
    st.subheader("Login Admin")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun() 
            else:
                st.error("Username atau Password salah!")
        
        st.caption("Gunakan: admin / admin123")

# --- View: Form Tambah Data ---
def view_tambah_data(manager):
    st.button("↩️ Kembali ke Dashboard", on_click=lambda: st.session_state.update(menu='data_mahasiswa'), key='back_tambah_data')
    st.header("➕ Input Data Mahasiswa Baru")
    
    with st.form("tambah_form"):
        st.subheader("Detail Mahasiswa")
        nim = st.text_input("NIM (12 digit):")
        nama = st.text_input("Nama:")
        email = st.text_input("Email:")
        jurusan = st.text_input("Jurusan:")
        ipk_str = st.text_input("IPK (0.00 - 4.00):") 
        
        submitted = st.form_submit_button("Simpan Data")
        
        if submitted:
            try:
                manager.tambah_data(nim, nama, email, jurusan, ipk_str)
                st.success(f"✅ Data {nama} berhasil ditambahkan!")
                time.sleep(1)
                st.session_state['menu'] = 'data_mahasiswa'
                st.rerun() 
            except ValueError as e:
                st.error(f"❌ Kesalahan Validasi: {e}")

# --- View: Form Edit Data ---
def view_edit_data(manager, nim_to_edit):
    st.button("↩️ Kembali ke Dashboard", on_click=lambda: st.session_state.update(menu='data_mahasiswa'), key='back_edit_data')
    st.header(f"✏️ Edit Data Mahasiswa (NIM: {nim_to_edit})")

    index = manager.cari_index_nim(nim_to_edit)
    if index == -1:
        st.error("Data tidak ditemukan.")
        if st.button("Kembali ke Data Mahasiswa"):
            st.session_state['menu'] = 'data_mahasiswa'
            st.rerun() 
        return

    mhs = manager.data_mahasiswa[index]

    st.warning("Kosongkan input jika tidak ingin mengubah data tersebut.")

    with st.form("edit_form"):
        nama = st.text_input("Nama:", value=mhs.get_nama())
        email = st.text_input("Email:", value=mhs.get_email())
        jurusan = st.text_input("Jurusan:", value=mhs.get_jurusan())
        ipk_str = st.text_input("IPK (0.00 - 4.00):", value=str(mhs.get_ipk()))

        submitted = st.form_submit_button("Update Data")

        if submitted:
            try:
                nama_baru = nama if nama != mhs.get_nama() else None
                email_baru = email if email != mhs.get_email() else None
                jurusan_baru = jurusan if jurusan != mhs.get_jurusan() else None
                
                ipk_baru_str = ipk_str
                if ipk_str and float(ipk_str) == mhs.get_ipk():
                    ipk_baru_str = None

                manager.edit_data(nim_to_edit, nama_baru, email_baru, jurusan_baru, ipk_baru_str)
                st.success(f"✅ Data NIM {nim_to_edit} berhasil diubah.")
                time.sleep(1)
                st.session_state['menu'] = 'data_mahasiswa'
                st.rerun() 
            except ValueError as e:
                st.error(f"❌ Kesalahan Validasi: {e}")
                
    if st.button("Batalkan Edit"):
        st.session_state['menu'] = 'data_mahasiswa'
        st.rerun() 

# --- View: Dashboard/Tampil Data ---
def view_dashboard(manager):
    # 2. Logo di Sidebar
    try:
        st.sidebar.image("logo_kampus.png", width=100) # Sesuaikan width jika perlu
    except FileNotFoundError:
        st.sidebar.warning("Logo file 'logo_kampus.png' not found.")
        
    st.sidebar.title(f"Selamat Datang, {st.session_state['username']}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear(), key='logout_btn')
    
    st.header("🎓 Menu Data Mahasiswa")
    # ... (lanjutan kode dashboard)

    # Navigasi Sidebar - Mengatur menu yang ditampilkan di main content
    st.sidebar.radio(
        "Navigasi",
        ("Data Mahasiswa", "Input Data", "Kirim Email", "Analisis"),
        index=("Data Mahasiswa", "Input Data", "Kirim Email", "Analisis").index(st.session_state['menu_sidebar']) if 'menu_sidebar' in st.session_state else 0,
        key='menu_sidebar',
        on_change=lambda: st.session_state.update(menu=st.session_state['menu_sidebar'].replace(' ', '_').lower())
    )
    
    if st.button("🔄 Reload Data"):
        manager.muat_data()
        st.rerun() 

    st.markdown("---")
    
    st.subheader(f"Data Mahasiswa (Total: {len(manager.data_mahasiswa)})")
    
    if manager.data_mahasiswa:
        data_dicts = [{
            'NIM': mhs.get_nim(),
            'Nama': mhs.get_nama(),
            'Email': mhs.get_email(),
            'Jurusan': mhs.get_jurusan(),
            'IPK': f"{mhs.get_ipk():.2f}"
        } for mhs in manager.data_mahasiswa]
        
        df = pd.DataFrame(data_dicts)
        
        df['Aksi'] = [
            f"""
            <a target="_self" href="?aksi=edit&nim={mhs.get_nim()}">✏️ Edit</a> | 
            <a target="_self" href="?aksi=hapus&nim={mhs.get_nim()}" onclick="return confirm('Yakin ingin menghapus {mhs.get_nama()}?');">🗑️ Hapus</a>
            """
            for mhs in manager.data_mahasiswa
        ]
        
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        query_params = st.query_params 
        aksi = query_params.get('aksi')
        nim_aksi = query_params.get('nim')

        if aksi == 'hapus' and nim_aksi:
            try:
                manager.hapus_data(nim_aksi)
                st.success(f"🗑️ Data NIM {nim_aksi} berhasil dihapus.")
                time.sleep(1)
            except ValueError as e:
                st.error(f"❌ Gagal Hapus: {e}")
            
            st.query_params.clear()
            st.rerun() 

        if aksi == 'edit' and nim_aksi:
            st.session_state['nim_edit'] = nim_aksi
            st.session_state['menu'] = 'edit'
            
            st.query_params.clear()
            st.rerun() 
            
    else:
        st.info("Tidak ada data mahasiswa yang tersedia.")

# --- View: Analisis Data (Search & Sort) ---
def view_analisis(manager):
    st.button("↩️ Kembali ke Dashboard", on_click=lambda: st.session_state.update(menu='data_mahasiswa'), key='back_analisis_menu')
    st.header("🔬 Menu Analisis Data: Pencarian & Pengurutan")
    
    tab1, tab2 = st.tabs(["Pencarian", "Pengurutan"])
    
    # ... (kode pencarian dan pengurutan)

# --- View: Kirim Email ---
def view_email(manager):
    st.button("↩️ Kembali ke Dashboard", on_click=lambda: st.session_state.update(menu='data_mahasiswa'), key='back_email_menu')
    st.header("📧 Kirim Email Data Mahasiswa")

    st.warning("""
    ⚠️ Perhatian: Fitur ini membutuhkan konfigurasi `EMAIL_PENGIRIM` dan `PASSWORD_PENGIRIM` 
    yang benar di file `manajemen.py` (App Password Gmail disarankan).
    """)

    with st.form("email_form"):
        penerima = st.text_input("Email Penerima:")
        subjek = st.text_input("Subjek Email:", value="Data Mahasiswa Akademik Terbaru")
        
        submitted = st.form_submit_button("Kirim File CSV via Email")
        
        if submitted:
            if not manager.validasi_email(penerima):
                st.error("❌ Format Email Penerima tidak valid.")
            else:
                try:
                    manager.kirim_email_data(penerima, subjek)
                    st.success("✅ Email berhasil dikirim!")
                except Exception as e:
                    st.error(f"❌ Gagal mengirim email: {e}")


# --- MAIN APPLICATION LOGIC ---
def main():
    st.set_page_config(layout="wide")
    manager = get_manager()

    # 3. Panggil fungsi background
    # Ganti 'background_image.jpg' dengan nama file background Anda
    add_bg_from_local('background_image.jpg') 

    if 'menu' not in st.session_state:
        st.session_state['menu'] = 'data_mahasiswa'
    if 'menu_sidebar' not in st.session_state:
        st.session_state['menu_sidebar'] = 'Data Mahasiswa'
        
    if not is_logged_in():
        view_login()
    else:
        if st.session_state['menu'] == 'data_mahasiswa':
            view_dashboard(manager)
        elif st.session_state['menu'] == 'input_data':
            view_tambah_data(manager)
        elif st.session_state['menu'] == 'analisis':
            view_analisis(manager)
        elif st.session_state['menu'] == 'kirim_email':
            view_email(manager)
        elif st.session_state['menu'] == 'edit':
            if 'nim_edit' in st.session_state:
                view_edit_data(manager, st.session_state['nim_edit'])
            else:
                st.session_state['menu'] = 'data_mahasiswa'
                st.rerun() 
                
if __name__ == '__main__':
    main()