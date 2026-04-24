import streamlit as st
import requests
import re
from datetime import datetime

# ==========================================
# LOGIKA PARSING (Copy dari scraper kamu)
# ==========================================
def extract_data_from_text(text):
    # (Di sini kamu bisa pakai fungsi extract_penyelenggara, dll. 
    # yang sudah kamu buat di script sebelumnya)
    # Sebagai contoh sederhana, kita ambil logika dasar:
    data = {
        "judul": "Judul Lomba (Terdeteksi)",
        "penyelenggara": "DEMA FEBI UIN SATU", # Contoh logika
        "deadline": datetime.now().strftime("%Y-%m-%d"),
        "biaya": "Gratis",
        "link": "-",
        "deskripsi": text[:100] + "..."
    }
    return data

# ==========================================
# UI APLIKASI
# ==========================================
st.set_page_config(page_title="Input Data Lomba DIKLAT", layout="wide")
st.title("🚀 Input Data Lomba - KSE UNRI")

# Sidebar untuk input mentah
raw_text = st.text_area("Paste Data Mentah Lomba di Sini:", height=200)

if st.button("Proses Data"):
    if raw_text:
        # Panggil fungsi parsing
        parsed = extract_data_from_text(raw_text)
        st.session_state['data'] = parsed
        st.success("Data berhasil diproses! Silakan periksa kembali di bawah.")
    else:
        st.warning("Mohon masukkan teks terlebih dahulu.")

# Form Input (Pre-filled dengan data hasil parsing)
if 'data' in st.session_state:
    d = st.session_state['data']
    
    with st.form("form_submission"):
        col1, col2 = st.columns(2)
        
        with col1:
            judul = st.text_input("Judul Kegiatan", value=d['judul'])
            kategori = st.selectbox("Kategori", ["Nasional", "Internasional", "Regional"])
            penyelenggara = st.text_input("Penyelenggara", value=d['penyelenggara'])
        
        with col2:
            deadline = st.date_input("Deadline")
            biaya = st.selectbox("Biaya", ["Gratis", "Berbayar"])
            link = st.text_input("Link Pendaftaran", value=d['link'])
            
        deskripsi = st.text_area("Deskripsi Singkat", value=d['deskripsi'])
        divisi = st.text_input("Divisi", value="DIKLAT", disabled=True)
        
        submitted = st.form_submit_button("Kirim ke Google Form")
        
        if submitted:
            # Panggil fungsi kirim() kamu di sini
            # kirim(data_dari_form)
            st.success(f"Data '{judul}' berhasil dikirim!")