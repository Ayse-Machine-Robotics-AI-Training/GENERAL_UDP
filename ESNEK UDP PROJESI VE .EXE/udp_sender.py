import socket
import json
import os
import struct
from datetime import datetime
import csv

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "log.csv")

# Log dosyası yoksa başlık satırını yaz
def initialize_log_file():
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "IP", "Port", "Mode", "CommandType", "Message", "Response"])

def log_message(ip, port, mode, command_type, message, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, ip, port, mode, command_type, message, response])

def send_udp_message(ip: str, port: int, message, mode: str = "single", command_type: str = "raw", timeout=3):
    """
    :param ip: IP adresi
    :param port: Port
    :param message: Gönderilecek komut (string veya dict)
    :param mode: "single" veya "multicast"
    :param command_type: "raw" (metin) veya "json" (nesne)
    :param timeout: Yanıt bekleme süresi (saniye)
    :return: Gelen yanıt veya timeout mesajı
    """
    initialize_log_file()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        if mode == "multicast":
            ttl = struct.pack('b', 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        if command_type == "json":
            msg_str = json.dumps(message)
            msg_bytes = msg_str.encode("utf-8")
        else:  # raw
            msg_str = str(message)
            msg_bytes = msg_str.encode("utf-8")

        sock.sendto(msg_bytes, (ip, port))

        try:
            data, addr = sock.recvfrom(1024)
            response = data.decode("utf-8")
            log_message(ip, port, mode, command_type, msg_str, response)
            return f"OK - Yanıt: {response}"
        except socket.timeout:
            log_message(ip, port, mode, command_type, msg_str, "TIMEOUT - Cevap gelmedi.")
            return "TIMEOUT - Cevap gelmedi."
    except Exception as e:
        log_message(ip, port, mode, command_type, message, f"HATA - {str(e)}")
        return f"HATA - {str(e)}"
    finally:
        sock.close()
