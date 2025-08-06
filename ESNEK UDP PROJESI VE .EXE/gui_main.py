# Tkinter arayüz
import tkinter as tk
from tkinter import ttk, messagebox
import json
from udp_sender import send_udp_message
from config import DEFAULT_IP, DEFAULT_PORT, DEFAULT_COMMAND_TYPE, DEFAULT_MODE


class UDPSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Gönderici")
        self.root.geometry("400x400")
        
        # IP adresi
        ttk.Label(root, text="IP Adresi:").pack(pady=(10, 0))
        self.ip_entry = ttk.Entry(root)
        self.ip_entry.insert(0, "192.168.10.1")
        self.ip_entry.pack()

        # Port
        ttk.Label(root, text="Port:").pack(pady=(10, 0))
        self.port_entry = ttk.Entry(root)
        self.port_entry.insert(0, "8889")
        self.port_entry.pack()

        # Gönderim modu: single/multicast
        ttk.Label(root, text="Gönderim Modu:").pack(pady=(10, 0))
        self.mode_var = tk.StringVar(value="single")
        ttk.Combobox(root, textvariable=self.mode_var, values=["single", "multicast"]).pack()

        # Komut tipi: raw/json
        ttk.Label(root, text="Komut Tipi:").pack(pady=(10, 0))
        self.type_var = tk.StringVar(value="raw")
        ttk.Combobox(root, textvariable=self.type_var, values=["raw", "json"]).pack()

        # Komut girme alanı
        ttk.Label(root, text="Komut:").pack(pady=(10, 0))
        self.command_entry = tk.Text(root, height=4)
        self.command_entry.pack(pady=5)

        # Gönder butonu
        ttk.Button(root, text="Gönder", command=self.send_command).pack(pady=10)

        # Yanıt gösterim alanı
        self.response_label = ttk.Label(root, text="Yanıt burada görünecek.")
        self.response_label.pack(pady=10)

    def send_command(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        mode = self.mode_var.get()
        command_type = self.type_var.get()
        raw_command = self.command_entry.get("1.0", tk.END).strip()

        if not raw_command:
            messagebox.showwarning("Uyarı", "Komut boş olamaz.")
            return

        # JSON türü ise nesneye çevrilmeli
        if command_type == "json":
            try:
                message = json.loads(raw_command)
            except json.JSONDecodeError:
                messagebox.showerror("Hata", "Geçersiz JSON formatı.")
                return
        else:
            message = raw_command

        # UDP mesajı gönder
        yanit = send_udp_message(
            ip=ip,
            port=port,
            message=message,
            mode=mode,
            command_type=command_type
        )
        self.response_label.config(text=yanit)

if __name__ == "__main__":
    root = tk.Tk()
    app = UDPSenderApp(root)
    root.mainloop()





#Kullanım (CLI veya GUI tarafından çağrılabilir)
from udp_sender import send_udp_message

# Örnek kullanım
response = send_udp_message(
    ip="192.168.10.1",
    port=8889,
    message="takeoff",
    mode="single",
    command_type="raw",  # veya "json"
    timeout=5
)
print(response)
