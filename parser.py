import re

def extract_data(text):
    # Bersihkan teks dari karakter non-ascii (emoji, dll) untuk stabilitas regex
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # --- LOGIKA TANGGAL (SMART SPLIT) ---
    mulai = "-"
    deadline = "-"
    
    # 1. Cari semua pola tanggal (Format: 13 Mei 2026 ATAU 13/05/2026)
    date_pattern = r'(\d{1,2}(?:[\s/])(?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Agu|Sep|Okt|Nov|Des|\d{1,2})(?:[\s/])\d{2,4})'
    found_dates = re.findall(date_pattern, text, re.IGNORECASE)
    
    # 2. Cari pola rentang (Contoh: 22 April - 13 Mei atau 01/03 - 15/03)
    range_pattern = r'(\d{1,2}(?:[\s/]\d{1,2})?)\s*[\-|–|sampai]\s*(\d{1,2}[\s/](?:Jan|Feb|Mar|Apr|Mei|Jun|Jul|Agu|Sep|Okt|Nov|Des|\d{1,2})[\s/]\d{2,4})'
    range_match = re.search(range_pattern, text, re.IGNORECASE)

    if range_match:
        mulai = range_match.group(1)
        deadline = range_match.group(2)
        # Jika 'mulai' hanya angka (misal: 22 - 25 April), tambahkan bulan & tahun dari deadline
        if len(mulai) <= 2:
            suffix = re.search(r'\s+([A-Za-z/]+\s+\d{4})', deadline)
            if suffix: mulai += suffix.group(0)
    elif len(found_dates) >= 2:
        mulai = found_dates[0]
        deadline = found_dates[-1]
    elif len(found_dates) == 1:
        deadline = found_dates[0]

    # --- EKSTRAKSI FIELD LAIN ---
    judul = lines[0].replace('*', '') if lines else "Tanpa Judul"
    
    # Link (Ambil yang pertama kali muncul)
    link = re.search(r'https?://[^\s]+', text)
    
    # Penyelenggara (Cari @ atau keyword organisasi)
    penyelenggara = "-"
    org_keywords = ["DEMA", "Himpunan", "UKM", "Girl Up", "Yapresindo", "Sentral", "Fakultas"]
    for line in lines:
        if any(key.lower() in line.lower() for key in org_keywords):
            penyelenggara = line.replace('*', '').strip()
            break
    if penyelenggara == "-":
        ig = re.search(r'@([\w\.]+)', text)
        penyelenggara = ig.group(0) if ig else "-"

    # Narahubung (Cari pola nomor HP)
    wa = re.findall(r'(?:\+62|08)[\d\-\s]{9,15}', text)
    wa_clean = ", ".join(list(set([w.strip() for w in wa]))) if wa else "-"

    # Biaya
    biaya = re.search(r'(?:HTM|Biaya|Rp)\s*[:\-]?\s*(Rp[\d\.\,]+|[\d\.\,]{4,})', text, re.I)
    
    return {
        "Judul": judul,
        "Penyelenggara": penyelenggara,
        "Link": link.group(0) if link else "-",
        "Mulai": mulai,
        "Deadline": deadline,
        "Biaya": biaya.group(1) if biaya else "Gratis/Cek Guidebook",
        "Narahubung": wa_clean,
        "Deskripsi": text[:300].replace('*', '') + "..."
    }