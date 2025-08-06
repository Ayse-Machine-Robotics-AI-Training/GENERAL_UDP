import argparse
import socket
import json
from logger import log_info, log_error, log_warning

DEFAULT_IP = "192.168.10.1"
DEFAULT_PORT = 8889
TIMEOUT = 3  # saniye

def send_udp(ip, port, message, msg_type):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    
    try:
        if msg_type == "json":
            json_obj = json.loads(message)
            data = json.dumps(json_obj).encode('utf-8')
        else:
            data = message.encode('utf-8')

        log_info(f"GÖNDERİLİYOR → IP: {ip}, PORT: {port}, TİP: {msg_type}, MESAJ: {message}")
        sock.sendto(data, (ip, port))
        response, _ = sock.recvfrom(4096)
        yanit = response.decode('utf-8')
        print("Cevap:", yanit)
        log_info(f"YANIT ← {yanit}")
    except socket.timeout:
        print("TIMEOUT - Cevap gelmedi.")
        log_warning("YANIT ALINAMADI - TIMEOUT")
    except json.JSONDecodeError:
        print("JSON format hatası!")
        log_error("JSON FORMAT HATASI")
    except Exception as e:
        log_error(f"GENEL HATA: {str(e)}")
    finally:
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="UDP CLI İstemci")
    parser.add_argument("--ip", default="192.168.1.100", help="Hedef IP adresi")
    parser.add_argument("--port", type=int, default=8889, help="Port numarası")
    parser.add_argument("--type", choices=["raw", "json"], default="raw", help="Mesaj tipi")
    parser.add_argument("--mode", choices=["single", "multicast"], default="single", help="Mod")
    parser.add_argument("--message", required=True, help="Gönderilecek mesaj")

    args = parser.parse_args()

    
    
    send_udp(args.ip, args.port, args.message, args.type)

if __name__ == "__main__":
    main()

#bash çalıştırma komutu : python cli_main.py --message "takeoff"
