import csv
from datetime import datetime
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d") + ".csv")

if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Zaman", "Seviye", "Mesaj"])

def log_yaz(seviye, mesaj):
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([zaman, seviye, mesaj])

def log_info(mesaj):
    log_yaz("INFO", mesaj)

def log_warning(mesaj):
    log_yaz("WARNING", mesaj)

def log_error(mesaj):
    log_yaz("ERROR", mesaj)
