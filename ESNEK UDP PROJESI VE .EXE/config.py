# Ortak ayarlar (timeout vs.)
# config.py

from datetime import datetime
import os

# Varsayılan UDP ayarları
DEFAULT_IP = "192.168.10.1"
DEFAULT_PORT = 8889
DEFAULT_TIMEOUT = 3  # saniye
DEFAULT_COMMAND_TYPE = "raw"  # "json" da olabilir
DEFAULT_MODE = "single"  # veya "multicast"

# Log dosyası ayarları (CSV formatında)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, datetime.now().strftime("%Y-%m-%d") + ".csv")
