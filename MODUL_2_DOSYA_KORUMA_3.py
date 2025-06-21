
import customtkinter as ctk
import threading
import subprocess
import os
import time
import pydivert
import win32file
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import Listbox, messagebox
from plyer import notification
import shutil
import docx
import pandas as pd
import PyPDF2
import re
import urllib.request
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl

# Görsel ve grafik stil ayarları
mpl.rcParams.update({
    'axes.edgecolor': '#FFFFFF',
    'axes.labelcolor': '#FFFFFF',
    'text.color': '#FFFFFF',
    'xtick.color': '#AAAAAA',
    'ytick.color': '#AAAAAA',
    'figure.facecolor': '#1e1e1e',
    'axes.facecolor': '#2c2c2c'
})

# --- Açılış animasyonu ---
açılıs_ekrani = ctk.CTk()
açılıs_ekrani.title("Yükleniyor...")
açılıs_ekrani.geometry("400x250")
açılıs_ekrani.configure(bg="#1e1e1e")
açılıs_label = ctk.CTkLabel(açılıs_ekrani, text="LOKAL SIZINTI MODÜLÜ YÜKLENİYOR...", font=("Arial", 16, "bold"), text_color="#ffffff")
açılıs_label.pack(pady=40)
progress = ctk.CTkProgressBar(açılıs_ekrani, width=300)
progress.pack(pady=10)
progress.set(0)

def ilerlet():
    for i in range(101):
        progress.set(i / 100)
        açılıs_ekrani.update()
        time.sleep(0.015)
    açılıs_ekrani.destroy()

ilerlet()

# --- Ana pencere ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
pencere = ctk.CTk()
pencere.title("Siber Güvenlik Kontrol Paneli")
pencere.geometry("1200x850")

# --- Üst Frame: Logolar ve Başlık ---
ust_frame = ctk.CTkFrame(pencere)
ust_frame.pack(pady=10, fill="x")

logo_url1 = "https://cdn.teknofest.org/media/upload/userFormUpload/t3-logo-ING_a4X3b_8v3oj.png"
logo_url2 = "https://cdn.teknofest.org/media/upload/userFormUpload/KK_MTH_0FtA7.png"

for url in [logo_url1, logo_url2]:
    try:
        u = urllib.request.urlopen(url)
        raw_data = u.read()
        u.close()
        im = Image.open(io.BytesIO(raw_data)).resize((120, 60))
        white_bg = Image.new("RGB", im.size, (255, 255, 255))
        white_bg.paste(im, mask=im.split()[3] if im.mode == 'RGBA' else None)
        photo = ImageTk.PhotoImage(white_bg)
        label = tk.Label(ust_frame, image=photo, bg="#FFFFFF")
        label.image = photo
        label.pack(side="left", padx=20)
    except Exception as e:
        print(f"Logo yüklenemedi: {e}")

ctk.CTkLabel(ust_frame, text="LOKAL SIZINTI ÖNLEME VE BİLDİRİM MODÜLÜ", font=("Arial", 22, "bold"), text_color="#ffffff").pack(side="left", padx=40)

# --- Grafik ve Banner Alanı ---
BANNER_YOLU = r"G:\Drive'ım\TEKNOFEST KKTC\KKTC_FINAL_PROJE_4\banner.jpg"

grafik_frame = ctk.CTkFrame(pencere, corner_radius=20)
grafik_frame.pack(fill="both", expand=False, pady=10, padx=20)

# Sol banner çerçevesi
sol_banner_frame = ctk.CTkFrame(grafik_frame, width=150)
sol_banner_frame.pack(side="left", fill="y", padx=10)

# Orta grafik çerçevesi
grafik_govde_frame = ctk.CTkFrame(grafik_frame)
grafik_govde_frame.pack(side="left", fill="both", expand=True)

# Sağ banner çerçevesi
sag_banner_frame = ctk.CTkFrame(grafik_frame, width=150)
sag_banner_frame.pack(side="right", fill="y", padx=10)

# Banner resmi yükle
try:
    banner_resim = Image.open(BANNER_YOLU)
    banner_resim = banner_resim.resize((460, 350))
    banner_foto = ImageTk.PhotoImage(banner_resim)

    sol_banner_label = ctk.CTkLabel(sol_banner_frame, image=banner_foto, text="")
    sol_banner_label.image = banner_foto
    sol_banner_label.pack(pady=10)

    sag_banner_label = ctk.CTkLabel(sag_banner_frame, image=banner_foto, text="")
    sag_banner_label.image = banner_foto
    sag_banner_label.pack(pady=10)

except Exception as e:
    print(f"[HATA] Banner yüklenemedi: {e}")

# Grafik alanı
fig = plt.figure(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=grafik_govde_frame)
canvas.get_tk_widget().pack()

# --- Log Alanı ---
log_frame = ctk.CTkFrame(pencere, corner_radius=20)
log_frame.pack(pady=10, fill="both", expand=True, padx=20)
log_label = ctk.CTkLabel(log_frame, text="Canlı Güvenlik Logları:", font=("Arial", 18))
log_label.pack(pady=5)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")
log_listbox = Listbox(log_frame, height=20, font=("Consolas", 12), bg="#1e1e1e", fg="#CCCCCC", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
log_listbox.pack(fill="both", expand=True, padx=15, pady=10)
scrollbar.config(command=log_listbox.yview)

risk_sayac = {"DÜŞÜK": 0, "ORTA": 0, "YÜKSEK": 0}

def guncelle_grafik():
    fig.clear()
    ax = fig.add_subplot(projection='3d')
    xpos = [0, 1, 2]
    ypos = [0, 0, 0]
    zpos = [0, 0, 0]
    dx = dy = [0.5, 0.5, 0.5]
    dz = [risk_sayac["DÜŞÜK"], risk_sayac["ORTA"], risk_sayac["YÜKSEK"]]
    colors = ["limegreen", "orange", "red"]
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
    ax.set_xticks([0.25, 1.25, 2.25])
    ax.set_xticklabels(["DÜŞÜK", "ORTA", "YÜKSEK"])
    ax.set_yticks([])
    ax.set_zticks(range(max(dz) + 1 if max(dz) > 0 else 1))
    ax.set_title("3D Risk Dağılımı")
    canvas.draw()

def logla(mesaj, seviye="DÜŞÜK"):
    print(mesaj)
    notification.notify(title="Güvenlik Uyarısı", message=mesaj, timeout=5)
    renk = "green" if seviye == "DÜŞÜK" else "orange" if seviye == "ORTA" else "red"
    log_listbox.insert(0, mesaj)
    log_listbox.itemconfig(0, {"fg": renk})
    risk_sayac[seviye] += 1
    guncelle_grafik()

# --- AI içerik analizi, izleme ve koruma işlevleri ---
riskli_regexler = [
    r"\b\d{11}\b",  # TC kimlik
    r"\bTR\d{2}(?: ?\d{4}){5}\b",  # IBAN
    r"\b\d{4} ?\d{4} ?\d{4} ?\d{4}\b",  # Kredi kartı
    r"\b(?:iban|tc kimlik|şifre|gizli|mahrem|banka|maaş|parola|admin|kullanıcı adı|adı|soyadı)\b"
]

KORUNAN_KLASOR = r"G:\Drive'ım\TEKNOFEST KKTC\KKTC_FINAL_PROJE_4\ORNEK_DATA_DOSYASI"
UZANTILAR = [".pdf", ".docx", ".xlsx"]
RISKLI_KLASOR = os.path.join(KORUNAN_KLASOR, "RISKLI")
os.makedirs(RISKLI_KLASOR, exist_ok=True)

def metinden_risk_skoru(metin):
    metin = metin.lower()
    skor = sum(len(re.findall(regex, metin)) for regex in riskli_regexler)
    if len(metin) > 1000:
        skor += 1
    return skor

def dosya_icerik_analizi_yap(dosya_yolu):
    try:
        if dosya_yolu.endswith(".docx"):
            doc = docx.Document(dosya_yolu)
            metin = " ".join([p.text for p in doc.paragraphs])
        elif dosya_yolu.endswith(".pdf"):
            reader = PyPDF2.PdfReader(open(dosya_yolu, "rb"))
            metin = " ".join([page.extract_text() or "" for page in reader.pages])
        elif dosya_yolu.endswith(".xlsx"):
            df = pd.read_excel(dosya_yolu, engine="openpyxl")
            metin = " ".join(df.astype(str).values.flatten())
        else:
            return 0
        return metinden_risk_skoru(metin)
    except Exception as e:
        logla(f"[AI HATA] {e}", "DÜŞÜK")
        return 0

class KorumaHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory and os.path.splitext(event.src_path)[1].lower() in UZANTILAR:
            risk = dosya_icerik_analizi_yap(event.src_path)
            if risk >= 3:
                logla(f"[YÜKSEK RİSK] {event.src_path}", "YÜKSEK")
                shutil.copy(event.src_path, os.path.join(RISKLI_KLASOR, os.path.basename(event.src_path)))
            elif risk == 2:
                logla(f"[ORTA RİSK] {event.src_path}", "ORTA")
            else:
                logla(f"[DÜŞÜK RİSK] {event.src_path}", "DÜŞÜK")

def dosya_izlemeyi_baslat():
    observer = Observer()
    observer.schedule(KorumaHandler(), KORUNAN_KLASOR, recursive=True)
    observer.start()
    while True:
        time.sleep(1)

def ag_trafigini_engelle():
    dosyalar = [f.lower() for f in os.listdir(KORUNAN_KLASOR) if any(f.endswith(ext) for ext in UZANTILAR)]
    with pydivert.WinDivert("outbound and tcp.PayloadLength > 0") as w:
        for paket in w:
            try:
                data = paket.tcp.payload.decode(errors="ignore").lower()
                if any(d in data for d in dosyalar):
                    w.drop(paket)
                    logla(f"[ENGELLENDİ] Ağ gönderimi", "YÜKSEK")
                else:
                    w.send(paket)
            except:
                pass

def usb_engelle():
    while True:
        mask = win32file.GetLogicalDrives()
        for i in range(1, 26):
            bit = 1 << i
            if mask & bit:
                disk = f"{chr(65+i)}:\\"
                if win32file.GetDriveType(disk) == win32file.DRIVE_REMOVABLE:
                    for dosya in os.listdir(disk):
                        if any(dosya.endswith(ext) for ext in UZANTILAR):
                            try:
                                os.remove(os.path.join(disk, dosya))
                                logla(f"[USB ENGELLENDİ] {dosya}", "YÜKSEK")
                            except:
                                pass
        time.sleep(1)

def baslat():
    threading.Thread(target=dosya_izlemeyi_baslat, daemon=True).start()
    threading.Thread(target=ag_trafigini_engelle, daemon=True).start()
    threading.Thread(target=usb_engelle, daemon=True).start()
    logla("Koruma sistemi aktif.", "DÜŞÜK")

# Başlat butonu
ctk.CTkButton(ust_frame, text="Koruma Sistemini Başlat", font=("Arial", 16), command=baslat).pack(side="right", padx=40, pady=10)

# Ana pencere çalıştır
pencere.mainloop()
