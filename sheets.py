import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    # Menggunakan ID spreadsheet dari Google Sheets link
    spreadsheet = client.open_by_key("1tiJvmSgStMlXh54f-8HkW_vJeRyg0RvDC_qsu_N0FIg")
    # Mengakses sheet dengan ID 1305918544 (dari gid di link)
    return spreadsheet.worksheet(id=1305918544)

def save_to_sheets(data):
    sheet = get_sheet()
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Timestamp
        data['Judul'], 
        data['Kategori'], 
        data['Bidang'],
        data['Partisipasi'], 
        data['Penyelenggara'],
        data['Mulai'], 
        data['Deadline'], 
        data['Lokasi'],
        data['Level'], 
        data['Biaya'], 
        data['Benefit'],
        data['Link'], 
        data['Narahubung'], 
        data['Deskripsi'],
        data['Divisi'], 
        "Lomba",        # JENIS INFORMASI
        "APPROVED"      # STATUS_APPROVAL
    ]
    sheet.append_row(row)