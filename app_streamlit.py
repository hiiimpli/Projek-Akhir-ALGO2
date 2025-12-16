# app_streamlit.py (VERSI FINAL)

import streamlit as st
import time
import pandas as pd
from manajemen import ManajemenData

#cobacoba

# --- Fungsi Utility ---
def get_manager():
    """Menginisialisasi ManajemenData dan menyimpannya di session_state."""
    if 'manager' not in st.session_state:
        st.session_state['manager'] = ManajemenData()
    return st.session_state['manager']

def is_logged_in():
    """Mengecek status login dari session_state."""
    return st.session_state.get('logged_in', False)

# --- View: Form Login Sederhana ---
def view_login():
    st.title("PORTAL AKADEMIK MAHASISWA UNPAM")
    st.subheader("Login Admin")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # --- Metode Login Sederhana (Username dan Password Statis) ---
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun() 
            else:
                st.error("Username atau Password salah!")
        
        st.caption("Gunakan: admin / admin123")

# --- View: Form Tambah Data ---
def view_tambah_data(manager):
    st.header("➕ Input Data Mahasiswa Baru")
    
    with st.form("tambah_form"):
        st.subheader("Detail Mahasiswa")
        nim = st.text_input("NIM (12 digit):")
        nama = st.text_input("Nama:")
        email = st.text_input("Email:")
        jurusan = st.text_input("Jurusan:")
        # Gunakan value default agar field tidak kosong saat error muncul
        ipk_str = st.text_input("IPK (0.00 - 4.00):") 
        
        submitted = st.form_submit_button("Simpan Data")
        
        if submitted:
            try:
                manager.tambah_data(nim, nama, email, jurusan, ipk_str)
                st.success(f"✅ Data {nama} berhasil ditambahkan!")
                time.sleep(1)
                st.session_state['menu'] = 'dashboard'
                st.rerun() 
            except ValueError as e:
                st.error(f"❌ Kesalahan Validasi: {e}")

# --- View: Form Edit Data ---
def view_edit_data(manager, nim_to_edit):
    st.header(f"✏️ Edit Data Mahasiswa (NIM: {nim_to_edit})")

    index = manager.cari_index_nim(nim_to_edit)
    if index == -1:
        st.error("Data tidak ditemukan.")
        if st.button("Kembali"):
            st.session_state['menu'] = 'dashboard'
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
                
                # Cek IPK: jika nilai string IPK tidak berubah, set None
                ipk_baru_str = ipk_str
                if ipk_str and float(ipk_str) == mhs.get_ipk():
                    ipk_baru_str = None

                manager.edit_data(nim_to_edit, nama_baru, email_baru, jurusan_baru, ipk_baru_str)
                st.success(f"✅ Data NIM {nim_to_edit} berhasil diubah.")
                time.sleep(1)
                st.session_state['menu'] = 'dashboard'
                st.rerun() 
            except ValueError as e:
                st.error(f"❌ Kesalahan Validasi: {e}")
                
    if st.button("Batalkan Edit"):
        st.session_state['menu'] = 'dashboard'
        st.rerun() 

# --- View: Dashboard/Tampil Data ---
def view_dashboard(manager):
    st.header("🎓 Menu Data Mahasiswa")
    st.sidebar.title(f"Selamat Datang, {st.session_state['username']}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear(), key='logout_btn')
    
    # Navigasi Sidebar
    st.sidebar.radio(
        "Navigasi",
        ("Data Mahasiswa", "Input Data", "Kirim Email", "Analisis"),
        index=("Data Mahasiswa", "Input Data", "Kirim Email", "Analisis").index(st.session_state['menu_sidebar']) if 'menu_sidebar' in st.session_state else 0,
        key='menu_sidebar',
        on_change=lambda: st.session_state.update(menu=st.session_state['menu_sidebar'].replace(' ', '_').lower())
    )
    
    # Tombol Reload Data
    if st.button("🔄 Reload Data"):
        manager.muat_data()
        st.rerun() 

    st.markdown("---")
    
    # Tampilkan Data
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
        
        # Tambahkan kolom aksi dengan link yang memicu aksi melalui query params
        df['Aksi'] = [
            f"""
            <a target="_self" href="?aksi=edit&nim={mhs.get_nim()}">✏️ Edit</a> | 
            <a target="_self" href="?aksi=hapus&nim={mhs.get_nim()}" onclick="return confirm('Yakin ingin menghapus {mhs.get_nama()}?');">🗑️ Hapus</a>
            """
            for mhs in manager.data_mahasiswa
        ]
        
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # --- Penanganan Aksi (Hapus/Edit) dari Query Params ---
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
    st.header("🔬 Menu Analisis Data: Pencarian & Pengurutan")
    
    # Tab untuk Search dan Sort
    tab1, tab2 = st.tabs(["Pencarian", "Pengurutan"])
    
    with tab1:
        st.subheader("1. Pencarian Data (Linear Search: $\\mathcal{O}(n)$)")
        with st.form("search_form"):
            col_search1, col_search2 = st.columns(2)
            with col_search1:
                kunci = st.text_input("Kunci Pencarian:")
            with col_search2:
                atribut = st.selectbox("Cari Berdasarkan:", options=['nim', 'nama', 'email', 'jurusan', 'ipk'])
                
            search_submitted = st.form_submit_button("Cari Data")
            
            if search_submitted and kunci:
                hasil, waktu = manager.cari_data(kunci, atribut)
                st.info(f"Ditemukan {len(hasil)} hasil dalam {waktu:.6f} detik.")
                
                if hasil:
                    df_hasil = pd.DataFrame([{
                        'NIM': mhs.get_nim(), 'Nama': mhs.get_nama(), 'Jurusan': mhs.get_jurusan(), 'IPK': f"{mhs.get_ipk():.2f}"
                    } for mhs in hasil])
                    st.dataframe(df_hasil, use_container_width=True)
                else:
                    st.warning("Data tidak ditemukan.")

    with tab2:
        st.subheader("2. Pengurutan Data ($\\mathcal{O}(n^2)$)")
        with st.form("sort_form"):
            col_sort1, col_sort2, col_sort3 = st.columns(3)
            with col_sort1:
                algo = st.selectbox("Algoritma:", options=['bubble', 'insertion'], format_func=lambda x: x.title() + " Sort")
            with col_sort2:
                atribut = st.selectbox("Urutkan Berdasarkan:", options=['ipk', 'nim', 'nama'])
            with col_sort3:
                urutan = st.selectbox("Urutan:", options=['asc', 'desc'], format_func=lambda x: "Ascending" if x == 'asc' else "Descending")
                
            sort_submitted = st.form_submit_button("Urutkan Data")

            if sort_submitted and manager.data_mahasiswa:
                if algo == 'bubble':
                    arr_terurut, waktu = manager.bubble_sort(atribut, urutan)
                elif algo == 'insertion':
                    arr_terurut, waktu = manager.insertion_sort(atribut, urutan)

                st.info(f"Data berhasil diurutkan menggunakan {algo.title()} Sort ({urutan.upper()} berdasarkan {atribut.upper()}) dalam {waktu:.6f} detik.")
                
                df_terurut = pd.DataFrame([{
                    'NIM': mhs.get_nim(), 'Nama': mhs.get_nama(), 'Jurusan': mhs.get_jurusan(), 'IPK': f"{mhs.get_ipk():.2f}"
                } for mhs in arr_terurut])
                st.dataframe(df_terurut, use_container_width=True)
            elif sort_submitted:
                st.warning("Tidak ada data untuk diurutkan.")


# --- View: Kirim Email ---
def view_email(manager):
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
                    # Menangkap kesalahan dari manajemen.py
                    st.error(f"❌ Gagal mengirim email: {e}")


# --- MAIN APPLICATION LOGIC ---
def main():
    st.set_page_config(layout="wide")
    manager = get_manager()

    # Inisialisasi Menu Default jika belum ada
    if 'menu' not in st.session_state:
        st.session_state['menu'] = 'data_mahasiswa'
    if 'menu_sidebar' not in st.session_state:
        st.session_state['menu_sidebar'] = 'Data Mahasiswa'
        
    if not is_logged_in():
        view_login()
    else:
        # Panggil View sesuai state menu yang aktif
        # Nama menu di session state harus sesuai dengan opsi di radio button
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