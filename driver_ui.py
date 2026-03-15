import customtkinter as ctk
from tkinter import ttk
import threading
from driver_scanner import DriverScanner
from driver_updater import DriverUpdater

class DriverUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YKZ Opti - Professional Driver Updater")
        self.geometry("1000x650")
        
        # Tema profesional Morado
        ctk.set_appearance_mode("Dark")
        self.accent_color = "#7a2cff"
        self.bg_color = "#0a0a0d"
        self.configure(fg_color=self.bg_color)
        
        self.scanner = DriverScanner(self.update_status)
        self.updater = DriverUpdater(self.update_status)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color="#121217", height=80, corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(self.header, text="YKZ DRIVER ENGINE", 
                                        font=("Segoe UI", 24, "bold"), text_color="white")
        self.title_label.pack(side="left", padx=30, pady=20)
        
        # Main Layout
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Stats Bar
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="#16161e", height=50)
        self.stats_frame.pack(fill="x", pady=(0, 15))
        
        self.status_lbl = ctk.CTkLabel(self.stats_frame, text="Listo para escanear hardware real...", 
                                       font=("Segoe UI", 13), text_color="#bbbbbb")
        self.status_lbl.pack(side="left", padx=20)

        # Progress
        self.progress = ctk.CTkProgressBar(self.main_container, height=4, progress_color=self.accent_color, fg_color="#1f1f2e")
        self.progress.pack(fill="x", pady=(0, 15))
        self.progress.set(0)
        
        # Treeview Styles (Using Standard Tkinter for the list to ensure performance)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#111116", 
                        foreground="white", 
                        fieldbackground="#111116", 
                        borderwidth=0,
                        rowheight=35,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading", 
                        background="#1a1a24", 
                        foreground="#7a2cff", 
                        font=("Segoe UI", 11, "bold"),
                        borderwidth=0)
        style.map("Treeview", background=[('selected', '#321463')])

        # Table Frame
        self.table_frame = ctk.CTkFrame(self.main_container, fg_color="#111116", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True)
        
        columns = ("device", "manufacturer", "version", "date", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("device", text="DISPOSITIVO")
        self.tree.heading("manufacturer", text="FABRICANTE")
        self.tree.heading("version", text="VER. INSTALADA")
        self.tree.heading("date", text="FECHA")
        self.tree.heading("status", text="ESTADO")
        
        self.tree.column("device", width=350)
        self.tree.column("manufacturer", width=120)
        self.tree.column("version", width=150)
        self.tree.column("date", width=120)
        self.tree.column("status", width=150)
        
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # Controls
        self.controls = ctk.CTkFrame(self, fg_color="#121217", height=80, corner_radius=0)
        self.controls.pack(fill="x", side="bottom")
        
        self.scan_btn = ctk.CTkButton(self.controls, text="ESCANEAR AHORA", 
                                      fg_color=self.accent_color, hover_color="#6221cc",
                                      font=("Segoe UI", 14, "bold"), width=200, height=45,
                                      command=self.start_scan)
        self.scan_btn.pack(side="left", padx=30, pady=15)
        
        self.update_all_btn = ctk.CTkButton(self.controls, text="ACTUALIZAR TODO", 
                                            fg_color="#1e5128", hover_color="#14361b",
                                            font=("Segoe UI", 14, "bold"), width=200, height=45,
                                            command=self.start_update, state="disabled")
        self.update_all_btn.pack(side="right", padx=30, pady=15)

        self.reboot_chk = ctk.CTkCheckBox(self.controls, text="Reiniciar al finalizar", 
                                          text_color="white", font=("Segoe UI", 12),
                                          fg_color=self.accent_color, hover_color="#6221cc")
        self.reboot_chk.pack(side="right", padx=10)

    def update_status(self, msg):
        self.status_lbl.configure(text=msg)

    def start_scan(self):
        self.scan_btn.configure(state="disabled")
        self.tree.delete(*self.tree.get_children())
        self.progress.set(0)
        self.progress.start()
        
        threading.Thread(target=self.run_scan_thread, daemon=True).start()

    def run_scan_thread(self):
        drivers = self.scanner.scan()
        self.after(0, lambda: self.finish_scan(drivers))

    def finish_scan(self, drivers):
        self.progress.stop()
        self.progress.set(1)
        
        for d in drivers:
            status = "Actualizado"
            if d['is_gpu']:
                status = "Update Available"
            
            tag = "up" if status == "Actualizado" else "new"
            self.tree.insert("", "end", values=(
                d['name'], 
                d['manufacturer'], 
                d['version'], 
                d['date'], 
                status
            ))
        
        self.update_status(f"Escaneo completado. {len(drivers)} dispositivos detectados.")
        self.scan_btn.configure(state="normal")
        self.update_all_btn.configure(state="normal")

    def start_update(self):
        # Confirmación y punto de restauración
        self.update_all_btn.configure(state="disabled")
        self.progress.start()
        threading.Thread(target=self.run_update_thread, daemon=True).start()

    def run_update_thread(self):
        self.updater.create_restore_point()
        do_reboot = self.reboot_chk.get() == 1
        proc = self.updater.install_all_drivers_ps(auto_reboot=do_reboot)
        
        if proc:
            self.update_status("Instalando drivers en segundo plano... No apague el PC.")
            # En una app real monitorearíamos el proceso de salida
        else:
            self.update_status("Error al iniciar el proceso de actualización.")

if __name__ == "__main__":
    app = DriverUI()
    app.mainloop()
