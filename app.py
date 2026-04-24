import streamlit as st
import pandas as pd
from parser import extract_data
from sheets import save_to_sheets, get_sheet

st.set_page_config(page_title="KSEUNRIPEDIA Admin", layout="wide")

st.title("👨‍💻 Admin Panel KSEUNRIPEDIA")
st.markdown("Gunakan tool ini untuk ekstraksi data lomba secara otomatis ke Google Sheets.")

# --- INPUT ---
raw_text = st.text_area("Paste Data Mentah Lomba:", height=200, placeholder="Masukkan caption IG atau teks pengumuman di sini...")

if st.button("🚀 Proses Data"):
    if raw_text:
        st.session_state['parsed'] = extract_data(raw_text)
        st.success("Ekstraksi berhasil! Silakan cek hasil di bawah.")
    else:
        st.error("Teks input tidak boleh kosong.")

# --- FORM REVIEW ---
if 'parsed' in st.session_state:
    d = st.session_state['parsed']
    st.divider()
    st.subheader("📝 Review & Validasi Data")
    
    with st.form("editor_form"):
        c1, c2 = st.columns(2)
        with c1:
            judul = st.text_input("JUDUL KEGIATAN", value=d['Judul'])
            kategori = st.selectbox("KATEGORI", ["Nasional", "Internasional", "Regional"])
            bidang = st.selectbox("BIDANG LOMBA", ["Akademik & Bahasa", "Teknologi & Digital", "Seni & Budaya", "Bisnis", "Olahraga"])
            partisipasi = st.selectbox("JENIS PARTISIPASI", ["Individu", "Kelompok", "Keduanya"])
            penyelenggara = st.text_input("PENYELENGGARA", value=d['Penyelenggara'])
            lokasi = st.selectbox("LOKASI", ["Online", "Offline", "Hybrid"])
            
        with c2:
            mulai = st.text_input("TANGGAL MULAI PENDAFTARAN", value=d['Mulai'])
            deadline = st.text_input("DEADLINE PENDAFTARAN", value=d['Deadline'])
            level = st.text_input("LEVEL PESERTA", value="Mahasiswa/Siswa")
            biaya = st.text_input("BIAYA PENDAFTARAN", value=d['Biaya'])
            link = st.text_input("LINK PENDAFTARAN", value=d['Link'])
            narahubung = st.text_input("NARAHUBUNG", value=d['Narahubung'])

        benefit = st.text_area("BENEFIT / HADIAH", value="-")
        deskripsi = st.text_area("DESKRIPSI SINGKAT", value=d['Deskripsi'])
        divisi = st.selectbox("DIVISI PENGINPUT", ["DIKLAT", "KOMINFO", "RAGAM", "COMDEV"])

        if st.form_submit_button("✅ Simpan & Publish ke Sheet"):
            final_data = {
                "Judul": judul, "Kategori": kategori, "Bidang": bidang,
                "Partisipasi": partisipasi, "Penyelenggara": penyelenggara,
                "Mulai": mulai, "Deadline": deadline, "Lokasi": lokasi,
                "Level": level, "Biaya": biaya, "Benefit": benefit,
                "Link": link, "Narahubung": narahubung, "Deskripsi": deskripsi,
                "Divisi": divisi
            }
            try:
                save_to_sheets(final_data)
                st.success("Data berhasil terkirim!")
                del st.session_state['parsed']
                st.rerun()
            except Exception as e:
                st.error(f"Gagal simpan: {e}")

# --- PREVIEW SHEET ---
st.divider()
st.subheader("📊 Data Terinput (Real-time)")
if st.button("Refresh Data"):
    st.rerun()

try:
    df = pd.DataFrame(get_sheet().get_all_records())
    st.dataframe(df.tail(10)) # Tampilkan 10 data terakhir
except:
    st.info("Koneksi ke Sheet belum tersedia atau Sheet masih kosong.")