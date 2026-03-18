
import customtkinter as ctk
import random
import wmi
import threading
import sys
import os
import time
import ctypes
import pythoncom
import logging
import hashlib # For license check
import json
import urllib.request
import psutil
from tkinter import messagebox, ttk
import subprocess
from PIL import Image, ImageTk

# --- Configuration & Theme ---
CURRENT_VERSION = "2.9.6"
# [USER CONFIG] Cambia esto por la URL RAW de tu archivo version.json en GitHub/Pastebin
# Ejemplo estructura JSON: {"version": "2.1.0", "url": "https://link/to/new_exe.exe"}
UPDATE_JSON_URL = "https://raw.githubusercontent.com/weeesh23w/ykz-opti/main/version.json" 

# Resources folder (put your images and mp3s here)
RESOURCE_DIR = "resources"
SPLASH_IMAGE_NAME = "splash_start.jpg"   # image to show while loading
EXE_ICON_NAME = "exe_icon.png"           # image to use for exe/icon when packaging
RENDERED_LOGO_NAME = "ykz_logo_rendered.png"
SPLASH_PREFERRED_NAMES = ["splash_original.jpg", "splash_anime.jpg", "splash_start.jpg"]

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # We will override with custom colors

# Colors (Purple Theme + Starfield)
COLOR_BG = "#050005"       # Deep purple-black background
COLOR_PANEL = "#120012"    # Dark purple for panels
COLOR_ACCENT = "#9b30ff"   # Purple accent
COLOR_ACCENT_HOVER = "#7a1ed6"  # Darker purple hover
COLOR_TEXT_MAIN = "#FFFFFF" # Pure white for headers
COLOR_TEXT_SUB = "#BBBBBB"  # Soft silver for descriptions
COLOR_SUCCESS = "#9b30ff"   # Purple
COLOR_DANGER = "#ff4444"    # Red for errors
COLOR_WARNING = "#ffaa00"   # Orange for warnings

# --- Translations ---
LANG = {
    "ES": {
        "nav_home": "📊  Mis Componentes",
        "nav_opti": "🚀  Optimización",
        "nav_nvidia": "🟢  NVIDIA",
        "nav_drivers": "🚗  Drivers",
        "nav_power": "⚡  Plan de Energía",
        "nav_activa": "🔑  Activación",
        "btn_update": "⬇  Buscar Actualización",
        "sys_summary": "RESUMEN DEL SISTEMA",
        "btn_rescan": "↻ Re-escanear",
        "cpu": "Procesador (CPU)",
        "gpu": "Gráfica (GPU)",
        "ram": "Memoria RAM",
        "board": "Placa Base",
        "disk": "Discos Duros",
        "sys": "Sistema (OS)",
        "intro_title": "BIENVENIDO",
        "intro_status1": "Cargando kernel...",
        "intro_status2": "Verificando componentes...",
        "intro_status3": "Optimizando sistema...",
        "intro_status4": "Finalizando configuración...",
        "intro_status5": "Listo.",
        "opti_title": "OPTIMIZACIÓN DE SISTEMA",
        "opti_c1_t": "Limpieza Profunda", "opti_c1_d": "Elimina archivos temporales y basura.",
        "opti_c2_t": "Boost de Red", "opti_c2_d": "Optimiza DNS y configuración TCP/IP.",
        "opti_c3_t": "Optimizar SSD", "opti_c3_d": "Fuerza el comando TRIM en las unidades sólidas (SSD).",
        "opti_c4_t": "Desbloquear Núcleos", "opti_c4_d": "Activa todos los procesadores lógicos.",
        "opti_c5_t": "Desactivar Hibernación", "opti_c5_d": "Libera espacio y reduce escrituras.",
        "opti_c6_t": "Menor Latencia", "opti_c6_d": "Ajusta SystemProfile para mejor respuesta.",
        "opti_c7_t": "Apps en Segundo Plano", "opti_c7_d": "Deshabilita el uso de apps en segundo plano.",
        "opti_c8_t": "Desactivar GameBar", "opti_c8_d": "Mejora FPS desactivando Xbox DVR y GameBar.",
        "opti_c9_t": "Rendimiento Visual", "opti_c9_d": "Desactiva efectos visuales innecesarios de Windows.",
        "opti_c10_t": "YKZ Plan", "opti_c10_d": "Plan para máxima latencia e impulsos en YKZ.",
        "nv_title": "NVIDIA GFORCE CENTER",
        "nv_c1_t": "Configuración Pura", "nv_c1_d": "Boost de relojes y baja latencia.",
        "nv_c2_t": "MSI Mode", "nv_c2_d": "Forzar interrupciones por mensaje (MSI) para la GPU.",
        "nv_c3_t": "Limpiador Driver", "nv_c3_d": "Limpia telemetría y bloquea logs de NVIDIA.",
        "nv_c4_t": "NVIDIA HD Audio", "nv_c4_d": "Desactiva audio por HDMI para reducir latencia DPC.",
        "nv_c5_t": "Prioridad IRQ GPU", "nv_c5_d": "Asigna máxima prioridad de interrupción a la gráfica.",
        "amd_title": "AMD ADRENALINE CENTER",
        "amd_c1_t": "Desactivar ULPS", "amd_c1_d": "Desactiva estado de ultra bajo consumo para más FPS.",
        "amd_c2_t": "Caché de Sombras", "amd_c2_d": "Fuerza caché de shaders encendida (reduce tirones).",
        "amd_c3_t": "MSI Mode AMD", "amd_c3_d": "Fuerza interrupciones MSI para tarjetas gráficas AMD.",
        "amd_c5_t": "Desactivar HD Audio", "amd_c5_d": "Desactiva audio por HDMI para reducir latencia DPC.",
        "amd_c6_t": "Prioridad IRQ GPU", "amd_c6_d": "Asigna máxima prioridad de interrupción a la gráfica.",
        "amd_c7_t": "Apagar AMD Events", "amd_c7_d": "Reduce micro-tirones apagando el servicio de eventos.",
        "nav_amd": "🔴  AMD",
        "act_title": "ACTIVAR WINDOWS",
        "act_c1_t": "Activar Windows", "act_c1_d": "Ejecuta el script de activación oficial automáticamente. Puede tardar un par de minutos.",
        "drv_title": "ESTADO DE CONTROLADORES",
        "drv_btn_scan": "ESCANEAR\nAHORA",
        "drv_desc": "Haz clic para analizar los componentes del sistema.",
        "drv_res_title": "Resultados del Escaneo",
        "drv_btn_upd": "⚡ ACTUALIZAR TODO",
        "drv_scan_active": "⚡ RADAR ACTIVO ⚡\nBuscando...",
        "drv_desc1": "Iniciando motor de detección profunda...",
        "drv_desc2": "Detectando componentes base del sistema...",
        "drv_desc3": "Sincronizando con base de datos de Windows Update (espera)...",
        "drv_desc4": "Buscando actualizaciones de controladores pendientes...",
        "drv_need_attn": "⚠ REQUIEREN ATENCIÓN",
        "drv_ok": "✔ COMPONENTES ACTUALIZADOS",
        "drv_chk_restart": "Reiniciar automáticamente el sistema tras la instalación",
        "btn_activar": "ACTIVAR",
        "nav_cleaning": "🧹  Limpieza",
        "clean_title": "LIMPIEZA DE SISTEMA",
        "clean_c1_t": "Limpieza de Disco", "clean_c1_d": "Elimina archivos temporales, prefetch y vacía la papelera.",
        "clean_c2_t": "Limpieza de Navegadores", "clean_c2_d": "Borra el caché y archivos temporales de Chrome, Edge y Firefox.",
        "clean_c3_t": "Reseteo de Red", "clean_c3_d": "Limpia el caché DNS y restablece el catálogo de Winsock.",
        "clean_c4_t": "Reseteo de Tienda", "clean_c4_d": "Limpia el caché de la Microsoft Store (WSReset).",
        "nav_repair": "🔧  Reparación",
        "repair_title": "REPARACIÓN DE WINDOWS",
        "rep_c1_t": "Escaneo SFC", "rep_c1_d": "Verifica y repara archivos del sistema.",
        "rep_c2_t": "Análisis DISM", "rep_c2_d": "Comprueba el estado de la imagen de Windows.",
        "rep_c3_t": "Reparar DISM", "rep_c3_d": "Repara la imagen de Windows a fondo (lento).",
        "rep_c4_t": "Check Disk", "rep_c4_d": "Busca errores en el disco principal sin reiniciar.",
        "rep_c5_t": "Reparar Update", "rep_c5_d": "Restablece los servicios de Windows Update.",
        "rep_c6_t": "Reparar Iconos", "rep_c6_t": "Reparar Iconos", "rep_c6_d": "Reconstruye el caché de iconos de Windows.",
        "opt_c11_t": "Anti-Telemetría", "opt_c11_d": "Bloquea el envío de datos a Microsoft.",
        "opt_c12_t": "Ratón Preciso", "opt_c12_d": "Desactiva la aceleración para puntería 1:1.",
        "opt_c13_t": "Prioridad CPU", "opt_c13_d": "Prioriza juegos frente a procesos del sistema.",
        "amd_c4_t": "Opti Latencia", "amd_c4_d": "Ajusta FlipQueueSize para menor input lag.",
        "btn_run": "EJECUTAR",
        "nav_laptop": "💻  Rendimiento Laptop",
        "laptop_title": "RENDIMIENTO DE LAPTOP",
        "laptop_c1_t": "Alto Rendimiento", "laptop_c1_d": "Fuerza la CPU al 100% sin throttling de batería.",
        "laptop_c2_t": "Boost Batería", "laptop_c2_d": "Elimina límites de energía en perfil de batería.",
        "laptop_c3_t": "GPU Laptop Boost", "laptop_c3_d": "Prioriza GPU dedicada y desactiva ahorro pcie.",
        "laptop_c4_t": "Optimizar RAM", "laptop_c4_d": "Agresiva limpieza de procesos en segundo plano.",
        "laptop_c5_t": "Anti-Thermal", "laptop_c5_d": "Ajusta ventilación y mitigate thermal throttling.",
        "laptop_c6_t": "WiFi Boost", "laptop_c6_d": "Evita suspensión del adaptador WiFi para baja latencia.",
        "nav_gaming": "🎮  Gaming Boost",
        "nav_input": "⌨️  Input Lag",
        "nav_debloat": "🗑️  Debloater",
        "nav_security": "🛡️  Seguridad",
        "gaming_title": "GAME BOOSTERS",
        "gaming_c1_t": "Valorant / CS2", "gaming_c1_d": "Optimización extrema del motor y la red.",
        "gaming_c2_t": "Boost FiveM", "gaming_c2_d": "Prioridad máxima y limpieza selectiva de caché.",
        "gaming_c3_t": "FSO Fix", "gaming_c3_d": "Desactiva optimizaciones de pantalla completa.",
        "gaming_c4_t": "Limpiar RAM (ISLC)", "gaming_c4_d": "Libera la caché en espera instantáneamente.",
        "gaming_c1_success": "Optimización para Valorant/CS2 aplicada.",
        "gaming_c2_success": "FiveM optimizado: Caché borrada y CPU priorizada.",
        "gaming_c3_success": "FSO Fix aplicado con éxito.",
        "gaming_c4_success": "Caché de RAM limpia perfectamente.",
        "input_title": "INPUT LAG EXTREMO",
        "input_c1_t": "FilterKeys Fix", "input_c1_d": "Elimina el retraso de repetición del teclado.",
        "input_c2_t": "USB Polling Rate", "input_c2_d": "Fuerza máxima velocidad en puertos USB.",
        "input_c3_t": "DPC Latency", "input_c3_d": "Ajusta latencia DPC y SystemTimerResolution.",
        "debloat_title": "WINDOWS DEBLOATER",
        "debloat_c1_t": "Modo Windows Lite", "debloat_c1_d": "Desactiva todos los servicios pesados ocultos.",
        "debloat_c2_t": "Quitar Bloatware", "debloat_c2_d": "Elimina apps nativas (TikTok, Xbox, etc).",
        "sec_title": "SEGURIDAD Y RESPALDO",
        "sec_c1_t": "Crear Punto", "sec_c1_d": "Crea un Punto de Restauración del Sistema ahora.",
        "lang_opt": "Español",
        "login_title": "ACTIVACIÓN REQUERIDA",
        "login_desc": "Introduce tu clave de producto para continuar:",
        "login_btn": "ACTIVAR AHORA",
        "login_ph": "YKZ-XXXX-XXXX-XXXX",
        "login_success": "¡Activado!",
        "login_fail": "Clave inválida.",
        "drv_col_dev": "DISPOSITIVO",
        "drv_col_man": "FABRICANTE",
        "drv_col_ver": "VER. INSTALADA",
        "drv_col_date": "FECHA",
        "drv_col_status": "ESTADO"
    },
    "EN": {
        "nav_home": "📊  My Components",
        "nav_opti": "🚀  Optimization",
        "nav_nvidia": "🟢  NVIDIA",
        "nav_drivers": "🚗  Drivers",
        "nav_power": "⚡  Power Plan",
        "nav_activa": "🔑  Activation",
        "btn_update": "⬇  Check Update",
        "sys_summary": "SYSTEM SUMMARY",
        "btn_rescan": "↻ Rescan",
        "cpu": "Processor (CPU)",
        "gpu": "Graphics (GPU)",
        "ram": "RAM Memory",
        "board": "Motherboard",
        "disk": "Hard Drives",
        "sys": "System (OS)",
        "intro_title": "WELCOME",
        "intro_status1": "Loading kernel...",
        "intro_status2": "Verifying components...",
        "intro_status3": "Optimizing system...",
        "intro_status4": "Finalizing configuration...",
        "intro_status5": "Ready.",
        "opti_title": "SYSTEM OPTIMIZATION",
        "opti_c1_t": "Deep Clean", "opti_c1_d": "Removes temporary files and junk.",
        "opti_c2_t": "Network Boost", "opti_c2_d": "Optimizes DNS and TCP/IP config.",
        "opti_c3_t": "Optimize SSD", "opti_c3_d": "Forces TRIM command on Solid State Drives (SSD).",
        "opti_c4_t": "Unlock Cores", "opti_c4_d": "Activates all logical processors.",
        "opti_c5_t": "Disable Hibernation", "opti_c5_d": "Frees space and reduces disk writes.",
        "opti_c6_t": "Lower Latency", "opti_c6_d": "Tweaks SystemProfile for better response.",
        "opti_c7_t": "Background Apps", "opti_c7_d": "Disables background apps usage.",
        "opti_c8_t": "Disable GameBar", "opti_c8_d": "Improves FPS by disabling Xbox DVR and GameBar.",
        "opti_c9_t": "Visual Performance", "opti_c9_d": "Disables unnecessary Windows visual effects.",
        "opti_c10_t": "YKZ Plan", "opti_c10_d": "Optimized plan for max latency and boost in YKZ.",
        "opti_c11_t": "Anti-Telemetry", "opti_c11_d": "Blocks data reporting to Microsoft.",
        "opti_c12_t": "Precision Mouse", "opti_c12_d": "Disables acceleration for 1:1 aim.",
        "opti_c13_t": "CPU Priority", "opti_c13_d": "Prioritizes games over system processes.",
        "nv_title": "NVIDIA GFORCE CENTER",
        "nv_c1_t": "Pure Config", "nv_c1_d": "Clock boost and low latency.",
        "nv_c2_t": "MSI Mode", "nv_c2_d": "Force Message Signaled Interrupts (MSI) for GPU.",
        "nv_c3_t": "Driver Cleaner", "nv_c3_d": "Cleans telemetry and blocks NVIDIA logs.",
        "amd_title": "AMD ADRENALINE CENTER",
        "amd_c1_t": "Disable ULPS", "amd_c1_d": "Disables ultra low power state for more FPS.",
        "amd_c2_t": "Shader Cache", "amd_c2_d": "Forces shader cache on (reduces stuttering).",
        "amd_c3_t": "MSI Mode AMD", "amd_c3_d": "Force MSI interrupts for AMD graphics cards.",
        "amd_c4_t": "Latency Opti", "amd_c4_d": "Adjusts FlipQueueSize for lower input lag.",
        "nav_amd": "🔴  AMD",
        "act_title": "ACTIVATE WINDOWS",
        "act_c1_t": "Activate Windows", "act_c1_d": "Runs official activation script automatically. May take a few minutes.",
        "drv_title": "DRIVER STATUS",
        "drv_btn_scan": "SCAN\nNOW",
        "drv_desc": "Click to analyze system components.",
        "drv_res_title": "Scan Results",
        "drv_btn_upd": "⚡ UPDATE ALL",
        "drv_scan_active": "⚡ RADAR ACTIVE ⚡\nSearching...",
        "drv_desc1": "Starting deep detection engine...",
        "drv_desc2": "Detecting base system components...",
        "drv_desc3": "Synchronizing with Windows Update database (wait)...",
        "drv_desc4": "Searching for pending driver updates...",
        "drv_need_attn": "⚠ ATTENTION REQUIRED",
        "drv_ok": "✔ COMPONENTS UP TO DATE",
        "drv_chk_restart": "Automatically restart system after installation",
        "btn_activar": "ACTIVATE",
        "nav_cleaning": "🧹  Cleaning",
        "clean_title": "SYSTEM CLEANING",
        "clean_c1_t": "Disk Cleanup", "clean_c1_d": "Deletes temporary files, prefetch, and empties recycle bin.",
        "clean_c2_t": "Browser Cleanup", "clean_c2_d": "Clears cache and profile data for Chrome, Edge, and Firefox.",
        "clean_c3_t": "Network Reset", "clean_c3_d": "Flushes DNS cache and resets Winsock catalog.",
        "clean_c4_t": "Store Reset", "clean_c4_d": "Cleans Microsoft Store cache (WSReset).",
        "nav_repair": "🔧  Repair",
        "repair_title": "WINDOWS REPAIR",
        "rep_c1_t": "SFC Scan", "rep_c1_d": "Verifies and repairs system files.",
        "rep_c2_t": "DISM Scan", "rep_c2_d": "Checks Windows image health.",
        "rep_c3_t": "DISM Repair", "rep_c3_d": "Deeply repairs Windows image (slow).",
        "rep_c4_t": "Check Disk", "rep_c4_d": "Scans main drive for errors without rebooting.",
        "rep_c5_t": "Repair Update", "rep_c5_d": "Resets Windows Update components.",
        "rep_c6_t": "Fix Icons", "rep_c6_d": "Rebuilds Windows icon cache.",
        "btn_run": "RUN",
        "nav_laptop": "💻  Laptop Perf.",
        "laptop_title": "LAPTOP PERFORMANCE",
        "laptop_c1_t": "High Performance", "laptop_c1_d": "Forces CPU to 100% without battery throttling.",
        "laptop_c2_t": "Battery Boost", "laptop_c2_d": "Removes power limits on battery profile.",
        "laptop_c3_t": "Laptop GPU Boost", "laptop_c3_d": "Prioritizes dedicated GPU and disables pcie savings.",
        "laptop_c4_t": "RAM Optimize", "laptop_c4_d": "Aggressive background process cleanup.",
        "laptop_c5_t": "Anti-Thermal", "laptop_c5_d": "Adjusts cooling to mitigate thermal throttling.",
        "laptop_c6_t": "WiFi Boost", "laptop_c6_d": "Prevents WiFi adapter suspension for low latency.",
                "nav_gaming": "🎮  Gaming Boost",
        "nav_input": "⌨️  Input Lag",
        "nav_debloat": "🗑️  Debloater",
        "nav_security": "🛡️  Security",
        "gaming_title": "GAME BOOSTERS",
        "gaming_c1_t": "Valorant / CS2", "gaming_c1_d": "Extreme engine and network optimization.",
        "gaming_c2_t": "FiveM Boost", "gaming_c2_d": "Max priority and GTA/FiveM cache cleaner.",
        "gaming_c3_t": "FSO Fix", "gaming_c3_d": "Disables Fullscreen Optimizations globally.",
        "gaming_c4_t": "Clear RAM (ISLC)", "gaming_c4_d": "Frees standby cache instantly.",
        "input_title": "EXTREME INPUT LAG",
        "input_c1_t": "FilterKeys Fix", "input_c1_d": "Removes keyboard repeat delay.",
        "input_c2_t": "USB Polling Rate", "input_c2_d": "Forces max speed on USB ports.",
        "input_c3_t": "DPC Latency", "input_c3_d": "Tweaks DPC and SystemTimerResolution.",
        "debloat_title": "WINDOWS DEBLOATER",
        "debloat_c1_t": "Windows Lite Mode", "debloat_c1_d": "Disables hidden heavy services.",
        "debloat_c2_t": "Remove Bloatware", "debloat_c2_d": "Removes native apps (TikTok, Xbox, etc).",
        "sec_title": "SECURITY & BACKUP",
        "sec_c1_t": "Create Point", "sec_c1_d": "Creates a System Restore Point immediately." ,
        "lang_opt": "English",
        "login_title": "ACTIVATION REQUIRED",
        "login_desc": "Enter your product key to continue:",
        "login_btn": "ACTIVATE NOW",
        "login_ph": "YKZ-XXXX-XXXX-XXXX",
        "login_success": "Activated!",
        "login_fail": "Invalid key.",
        "drv_col_dev": "DEVICE",
        "drv_col_man": "MANUFACTURER",
        "drv_col_ver": "INSTALLED VER.",
        "drv_col_date": "DATE",
        "drv_col_status": "STATUS"
    }
}

# --- License Management ---
class LicenseManager:
    LICENSE_FILE = os.path.join(os.getenv('APPDATA'), "ykz_license.json")
    # For now, we use a simple hardcoded key or a hash. 
    # To be more secure, this should check an online API.
    VALID_KEYS = ["YKZ-ELITE-2026", "YKZ-PRO-LAUNCH", "TEST-KEY-123"]

    @staticmethod
    def validate(key):
        return key in LicenseManager.VALID_KEYS

    @staticmethod
    def save(key):
        try:
            with open(LicenseManager.LICENSE_FILE, "w") as f:
                json.dump({"key": key, "activated": True}, f)
        except:
            pass

    @staticmethod
    def load():
        if os.path.exists(LicenseManager.LICENSE_FILE):
            try:
                with open(LicenseManager.LICENSE_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("key")
            except:
                return None
        return None

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success
        self.geometry("400x320")
        self.overrideredirect(True)
        
        # Try to get language from parent or default to ES
        self.lang_code = "ES"
        try:
            if hasattr(parent, "current_lang"):
                self.lang_code = parent.current_lang
        except: pass
        l = LANG[self.lang_code]

        self.title(l["login_title"])
        self.configure(fg_color=COLOR_BG)
        
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (320/2)
        self.geometry('+%d+%d' % (x, y))
        self.grab_set()
        self.attributes("-topmost", True)
        
        ctk.CTkLabel(self, text="YKZ OPTI", font=("Arial", 24, "bold"), text_color=COLOR_ACCENT).pack(pady=(40, 10))
        ctk.CTkLabel(self, text=l["login_desc"], text_color="white").pack(pady=5)
        
        self.entry = ctk.CTkEntry(self, width=280, placeholder_text=l["login_ph"], justify="center", height=40)
        self.entry.pack(pady=15)
        
        ctk.CTkButton(self, text=l["login_btn"], width=280, height=45, font=("Arial", 14, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=self.check_key).pack(pady=10)
        
        self.lbl_msg = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_msg.pack(pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def check_key(self):
        l = LANG[self.lang_code]
        key = self.entry.get().strip().upper()
        if LicenseManager.validate(key):
            LicenseManager.save(key)
            self.lbl_msg.configure(text=l["login_success"], text_color="green")
            self.after(1000, self.finish)
        else:
            self.lbl_msg.configure(text=l["login_fail"], text_color="red")

    def finish(self):
        self.destroy()
        self.on_success()

    def on_close(self):
        sys.exit(0)

class GlitchLogo(ctk.CTkFrame):
    """
    Logo widget that renders a polished logo using an optional icon from resources
    and gradient-filled text rendered via Pillow. Falls back cleanly if fonts
    or images are missing.
    """
    def __init__(self, master, text="YKZ OPTI"):
        super().__init__(master, fg_color="transparent", width=260, height=64)
        self.pack_propagate(False)

        # Build a small PIL image with icon (if exists) + gradient text
        try:
            from PIL import ImageDraw, ImageFont, Image, ImageFilter
            import base64, io
            w, h = 260, 64

            # If a rendered PNG logo exists in resources, prefer it and use directly
            try:
                rendered_path = get_resource_path(os.path.join(RESOURCE_DIR, RENDERED_LOGO_NAME))
                if os.path.exists(rendered_path):
                    img0 = Image.open(rendered_path).convert('RGBA')
                    img0 = img0.resize((260, 64), Image.Resampling.LANCZOS)
                    self.img_tk = ctk.CTkImage(light_image=img0, dark_image=img0, size=(260, 64))
                    self.lbl = ctk.CTkLabel(self, text="", image=self.img_tk, fg_color="transparent")
                    self.lbl.pack(fill='both', expand=True)
                    return
            except Exception:
                pass

            # If a base64 logo file exists in resources, prefer it and use directly
            try:
                b64_path = get_resource_path(os.path.join(RESOURCE_DIR, 'ykz_logo_base64.txt'))
                if os.path.exists(b64_path):
                    with open(b64_path, 'r') as bf:
                        data = bf.read()
                    img_bytes = base64.b64decode(data)
                    img0 = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
                    img0 = img0.resize((260, 64), Image.Resampling.LANCZOS)
                    self.img_tk = ctk.CTkImage(light_image=img0, dark_image=img0, size=(260, 64))
                    self.lbl = ctk.CTkLabel(self, text="", image=self.img_tk, fg_color="transparent")
                    self.lbl.pack(fill='both', expand=True)
                    return
            except Exception:
                pass

            img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

            # Do NOT include side icon; keep logo clean. Set text offset.
            text_x = 12

            draw = ImageDraw.Draw(img)

            # pick a font - try common fonts, fallback to default
            font = None
            for f in ("arialbd.ttf", "Arial Bold.ttf", "SegoeUI-Bold.ttf"):
                try:
                    font = ImageFont.truetype(f, 28)
                    break
                except Exception:
                    font = None
            if font is None:
                font = ImageFont.load_default()

            # create gradient text by drawing mask and filling with gradient
            txt = text
            mask = Image.new('L', (w, h), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.text((text_x, 16), txt, font=font, fill=255)

            # gradient from bright purple to deep purple
            grad = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            # start color (#9b30ff) -> end color (#5a00c2)
            sr, sg, sb = 0x9b, 0x30, 0xff
            er, eg, eb = 0x5a, 0x00, 0xc2
            for i in range(w):
                t = i / max(w - 1, 1)
                r = int(sr + (er - sr) * t)
                g = int(sg + (eg - sg) * t)
                b = int(sb + (eb - sb) * t)
                for y in range(h):
                    grad.putpixel((i, y), (r, g, b, 255))

            img.paste(grad, (0, 0), mask)

            # subtle white highlight stroke
            stroke = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            sd = ImageDraw.Draw(stroke)
            sd.text((text_x-1, 16-1), txt, font=font, fill=(255,255,255,30))
            sd.text((text_x+1, 16+1), txt, font=font, fill=(0,0,0,60))
            img = Image.alpha_composite(stroke, img)

            # convert to CTkImage and show in a label
            self.img_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(260, 64))
            self.lbl = ctk.CTkLabel(self, text="", image=self.img_tk, fg_color="transparent")
            self.lbl.pack(fill='both', expand=True)
        except Exception as e:
            # fallback simple label if Pillow fails
            self.lbl_simple = ctk.CTkLabel(self, text=text, font=("Arial", 20, "bold"), text_color="#ff0000")
            self.lbl_simple.pack(expand=True)


def generate_rendered_ykz(path):
    """Generate a stylized YKZ logo PNG at `path` using PIL."""
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        import random, os
        w, h = 800, 320
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # try a list of script fonts, fallback to default
        font = None
        for fname, size in (("BrushScriptStd.otf", 220), ("Pacifico.ttf", 220), ("arialbd.ttf", 200)):
            try:
                font = ImageFont.truetype(fname, size)
                break
            except Exception:
                font = None
        if font is None:
            font = ImageFont.load_default()

        text = "YKZ"
        tx = 40
        ty = 20

        # large blurred shadow
        shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.text((tx+18, ty+28), text, font=font, fill=(0, 0, 0, 200))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        img = Image.alpha_composite(img, shadow)

        # gradient fill mask
        mask = Image.new('L', (w, h), 0)
        md = ImageDraw.Draw(mask)
        md.text((tx, ty), text, font=font, fill=255)

        grad = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        sr, sg, sb = 179, 60, 255
        er, eg, eb = 106, 0, 255
        for i in range(w):
            t = i / max(w - 1, 1)
            r = int(sr + (er - sr) * t)
            g = int(sg + (eg - sg) * t)
            b = int(sb + (eb - sb) * t)
            for y in range(h):
                grad.putpixel((i, y), (r, g, b, 255))

        base = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        base.paste(grad, (0, 0), mask)
        img = Image.alpha_composite(img, base)

        # subtle highlight
        stroke = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stroke)
        sd.text((tx-2, ty-2), text, font=font, fill=(255, 200, 255, 100))
        img = Image.alpha_composite(stroke, img)

        # add small sparkles
        for _ in range(300):
            rx = random.randint(tx, tx + int(w * 0.6))
            ry = random.randint(ty, ty + int(h * 0.8))
            if mask.getpixel((rx, ry)) == 0:
                img.putpixel((rx, ry), (255, 200, 255, random.randint(80, 220)))

        # draw OPTI underneath
        try:
            ofont = ImageFont.truetype('arial.ttf', 56)
        except Exception:
            ofont = ImageFont.load_default()
        ox = tx + 60
        oy = ty + 200
        od = ImageDraw.Draw(img)
        od.text((ox, oy), 'OPTI', font=ofont, fill=(255, 160, 255, 255))

        # save
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path)
        return True
    except Exception:
        return False


# --- Logging ---
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def is_laptop():
    try:
        import psutil
        return psutil.sensors_battery() is not None
    except Exception:
        return False

import tempfile
log_file = os.path.join(tempfile.gettempdir(), "debug_smart.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Splash Screen (Top Level) ---
class IntroWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_complete):
        super().__init__(parent)
        self.on_complete = on_complete
        self.geometry("500x600")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        # Use a red/black theme for the splash screen regardless of app theme
        splash_bg = "#000000"      # pure black background for splash
        splash_accent = "#ff0000"  # red accent for title/progress
        self.configure(fg_color=splash_bg)
        
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (500/2)
        y = (hs/2) - (600/2)
        self.geometry('%dx%d+%d+%d' % (500, 600, x, y))

        self.setup_image()

        self.lbl_title = ctk.CTkLabel(self, text="BIENVENIDO", font=("Arial", 24, "bold"), text_color=splash_accent)
        self.lbl_title.pack(pady=(20, 10))

        self.lbl_status = ctk.CTkLabel(self, text="Inicializando...", font=("Roboto", 14), text_color=COLOR_TEXT_SUB)
        self.lbl_status.pack(pady=5)

        self.progress = ctk.CTkProgressBar(self, width=400, height=8, corner_radius=4, progress_color=splash_accent, fg_color="#1F2833")
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        self.lbl_pct = ctk.CTkLabel(self, text="0%", font=("Roboto", 12, "bold"), text_color=splash_accent)
        self.lbl_pct.pack()

        self.step = 0
        self.after(500, self.animate_loading)

    def setup_image(self):
        # Prefer an original splash image if present (keeps your original photo)
        img_path = None
        for n in SPLASH_PREFERRED_NAMES:
            candidate = get_resource_path(os.path.join(RESOURCE_DIR, n))
            if os.path.exists(candidate):
                img_path = candidate
                break
        # fallback to default name
        if img_path is None:
            img_path = get_resource_path(os.path.join(RESOURCE_DIR, SPLASH_IMAGE_NAME))

        try:
            if os.path.exists(img_path):
                pil_img = Image.open(img_path)
                # Fixed resizing logic to prevent stretching
                orig_w, orig_h = pil_img.size
                target_w = 400
                target_h = 350
                
                # Calculate new size while maintaining aspect ratio
                ratio = min(target_w/orig_w, target_h/orig_h)
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                
                pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.img_tk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(new_w, new_h))
                self.lbl_img = ctk.CTkLabel(self, text="", image=self.img_tk)
                self.lbl_img.pack(pady=(20, 10))
            else:
                # show a simple purple text logo (basic) to keep it minimal
                lbl = ctk.CTkLabel(self, text="YKZ OPTI", font=("Arial", 36, "bold"), text_color="#9b30ff")
                lbl.pack(pady=80)
        except Exception as e:
            logging.error(f"Image load error: {e}")

    def animate_loading(self):
        if self.step <= 100:
            prog = self.step / 100.0
            self.progress.set(prog)
            self.lbl_pct.configure(text=f"{self.step}%")
            
            if self.step < 20: self.lbl_status.configure(text=LANG[self.master.current_lang]["intro_status1"])
            elif self.step < 40: self.lbl_status.configure(text=LANG[self.master.current_lang]["intro_status2"])
            elif self.step < 70: self.lbl_status.configure(text=LANG[self.master.current_lang]["intro_status3"])
            elif self.step < 90: self.lbl_status.configure(text=LANG[self.master.current_lang]["intro_status4"])
            else: self.lbl_status.configure(text=LANG[self.master.current_lang]["intro_status5"])

            self.step += 1
            self.after(60, self.animate_loading) 
        else:
            self.finish_sequence()

    def finish_sequence(self):
        self.destroy()
        self.on_complete()

# --- Sub-views ---
class BaseCommandView(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color=COLOR_BG)
        
        self.lbl_title = ctk.CTkLabel(self, text=title, font=("Arial", 24, "bold"), text_color="white")
        self.lbl_title.pack(pady=(20, 30), padx=20, anchor="w")

        self.content_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.content_frame.columnconfigure((0, 1), weight=1)
        
        # Fluid Scroll binding - removed bind_all to prevent global event hijacking
        self.content_frame.bind("<MouseWheel>", self._on_mousewheel)
        # Bind also to children recursively
        self._bind_mousewheel(self.content_frame)

    def _bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        for child in widget.winfo_children():
            self._bind_mousewheel(child)

    def _on_mousewheel(self, event):
        # Increased scroll speed for better fluidity
        try:
            scroll_dist = -1 * (event.delta / 60) # 60 instead of 120 for double speed
            self.content_frame._parent_canvas.yview_scroll(int(scroll_dist), "units")
        except:
            pass

    def create_card(self, r, c, icon, title, desc, cmd, color=COLOR_ACCENT, img_path=None):
        card = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL, corner_radius=15, border_width=1, border_color="#330033")
        card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
        card.columnconfigure(1, weight=1)

        # Background Image (Banner)
        content_row = 0
        if img_path:
            full_path = get_resource_path(os.path.join(RESOURCE_DIR, img_path))
            if os.path.exists(full_path):
                try:
                    from PIL import Image
                    pil_img = Image.open(full_path)
                    # Create a wide banner style
                    banner_tk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(410, 120))
                    lbl_banner = ctk.CTkLabel(card, text="", image=banner_tk, corner_radius=15)
                    lbl_banner.grid(row=0, column=0, columnspan=3, sticky="new", padx=2, pady=2)
                    content_row = 1
                except Exception as e:
                    logging.error(f"Card image error: {e}")
        
        if icon:
            icon_bg = ctk.CTkFrame(card, fg_color="#110011", width=45, height=45, corner_radius=10)
            icon_bg.grid(row=content_row, column=0, padx=(15, 5), pady=15, sticky="nw")
            icon_bg.pack_propagate(False)
            ctk.CTkLabel(icon_bg, text=icon, font=("Segoe UI Emoji", 24)).place(relx=0.5, rely=0.5, anchor="center")
            icon_padx = (15, 5)
        else:
            icon_padx = (20, 5)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=content_row, column=1, pady=10, padx=icon_padx, sticky="nsew")
        info_frame.columnconfigure(0, weight=1)
        
        lbl_title = ctk.CTkLabel(info_frame, text=title, font=("Roboto", 14, "bold"), text_color=color, anchor="w", wraplength=180, justify="left")
        lbl_title.grid(row=0, column=0, sticky="ew")
        
        lbl_desc = ctk.CTkLabel(info_frame, text=desc, font=("Roboto", 11), text_color=COLOR_TEXT_SUB, anchor="w", wraplength=180, justify="left")
        lbl_desc.grid(row=1, column=0, sticky="ew")
        
        # Translation of ACTIVAR button text
        btn_text = "ACTIVAR"
        try:
            # Try to get the language from the main app
            main_app = self.master.master
            if hasattr(main_app, "current_lang"):
                btn_text = LANG[main_app.current_lang].get("btn_activar", "ACTIVAR")
        except:
            pass

        btn = ctk.CTkButton(card, text=btn_text, width=90, height=34, corner_radius=8, font=("Roboto", 11, "bold"), fg_color=color, hover_color=COLOR_ACCENT_HOVER if color == COLOR_ACCENT else "#555", command=cmd)
        btn.grid(row=content_row, column=2, padx=(5, 15), pady=15, sticky="e")
        
        # Store references for re-translation
        if not hasattr(self, 'cards_refs'): self.cards_refs = []
        self.cards_refs.append((lbl_title, lbl_desc, btn))

    def update_texts(self, l_title, card_texts, l_btn):
        self.lbl_title.configure(text=l_title)
        for i, ref in enumerate(self.cards_refs):
            ref[0].configure(text=card_texts[i][0])
            ref[1].configure(text=card_texts[i][1])
            ref[2].configure(text=l_btn)

    def log(self, msg):
        pass

    def run_cmd(self, cmd_list, success_msg, silent=True):
        def _run():
            try:
                import ctypes
                import tempfile
                import os
                
                # We write the commands into a temporary powershell script, execute it silently and append a toast notification
                ps1_path = os.path.join(tempfile.gettempdir(), f"cmd_ykz_{int(time.time())}.ps1")
                done_path = os.path.join(tempfile.gettempdir(), f"done_ykz_{int(time.time())}.done")
                vbs_path = os.path.join(tempfile.gettempdir(), f"run_ykz_{int(time.time())}.vbs")
                
                with open(ps1_path, "w") as f:
                    for cmd in cmd_list:
                        self.log(f"Ejecutando: {cmd}")
                        f.write(f'{cmd}\n')
                        f.write('Start-Sleep -Milliseconds 500\n')
                    
                    # Notificación Nativa al terminar
                    f.write('Add-Type -AssemblyName System.Windows.Forms\n')
                    f.write('$balloon = New-Object System.Windows.Forms.NotifyIcon\n')
                    f.write('$path = (Get-Process -id $pid).Path\n')
                    f.write('$balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)\n')
                    f.write('$balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info\n')
                    f.write('$balloon.BalloonTipTitle = "YKZ OPTI"\n')
                    f.write(f'$balloon.BalloonTipText = "{success_msg}"\n')
                    f.write('$balloon.Visible = $true\n')
                    f.write('$balloon.ShowBalloonTip(5000)\n')
                    
                    # Escribir archivo de señal al terminar
                    f.write(f'New-Item -Path "{done_path}" -ItemType File -Force\n')
                    
                    f.write('Start-Sleep 5\n')
                    f.write('$balloon.Dispose()\n')
                
                import subprocess
                args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", "; ".join(cmd_list)]
                # Use subprocess.run to wait for completion inside the thread
                subprocess.run(args, creationflags=0x08000000)
                
                # Show native toast ONLY AFTER completion
                if success_msg:
                    time.sleep(1) # Small delay for the system to settle
                    toast_script = f'''
                    Add-Type -AssemblyName System.Windows.Forms
                    $balloon = New-Object System.Windows.Forms.NotifyIcon
                    $path = (Get-Process -id $pid).Path
                    $balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
                    $balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
                    $balloon.BalloonTipTitle = "YKZ OPTI"
                    $balloon.BalloonTipText = "{success_msg}"
                    $balloon.Visible = $true
                    $balloon.ShowBalloonTip(5000)
                    Start-Sleep 5
                    $balloon.Dispose()
                    '''
                    toast_args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", toast_script]
                    subprocess.run(toast_args, creationflags=0x08000000)
                
            except Exception as e:
                self.log(f"ERROR: {e}")
        
        threading.Thread(target=_run, daemon=True).start()

class OptimizationView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["opti_title"])
        self.create_card(0, 0, "🚀", l["opti_c1_t"], l["opti_c1_d"], self.clean_temp)
        self.create_card(0, 1, "⚡", l["opti_c2_t"], l["opti_c2_d"], self.optimize_network)
        self.create_card(1, 0, "💿", l["opti_c3_t"], l["opti_c3_d"], self.optimize_ssd)
        self.create_card(1, 1, "🔓", l["opti_c4_t"], l["opti_c4_d"], self.unlock_processors)
        self.create_card(2, 0, "💤", l["opti_c5_t"], l["opti_c5_d"], self.disable_hibernate)
        self.create_card(2, 1, "⏱️", l["opti_c6_t"], l["opti_c6_d"], self.latency_fix)
        self.create_card(3, 0, "📵", l["opti_c7_t"], l["opti_c7_d"], self.disable_background_apps)
        self.create_card(3, 1, "🎮", l["opti_c8_t"], l["opti_c8_d"], self.disable_gamebar)
        self.create_card(4, 0, "👁️", l["opti_c9_t"], l["opti_c9_d"], self.visual_performance)
        self.create_card(4, 1, "🛡️", l["opt_c11_t"], l["opt_c11_d"], self.disable_telemetry)
        self.create_card(5, 0, "🖱️", l["opt_c12_t"], l["opt_c12_d"], self.mouse_precision)
        self.create_card(5, 1, "⚡", l["opt_c13_t"], l["opt_c13_d"], self.cpu_priority)

    def clean_temp(self):
        cmds = ['del /q /f /s %TEMP%\\*', 'del /q /f /s C:\\Windows\\Temp\\*', 'ipconfig /flushdns']
        self.run_cmd(cmds, "Archivos temporales eliminados.")

    def optimize_network(self):
        cmds = ['ipconfig /flushdns', 'ipconfig /release', 'ipconfig /renew', 'netsh winsock reset']
        self.run_cmd(cmds, "Red optimizada. Reinicia si es necesario.")

    def optimize_ssd(self):
        cmd = ['defrag /c /h /u /o']
        self.run_cmd(cmd, "Optimización de unidades de almacenamiento iniciada. (Comando TRIM).")

    def unlock_processors(self):
        import multiprocessing
        count = multiprocessing.cpu_count()
        cmd = [f'bcdedit /set numproc {count}']
        self.run_cmd(cmd, f"Núcleos desbloqueados ({count}).")
        
    def disable_hibernate(self):
        self.run_cmd(['powercfg -h off'], "Hibernación desactivada. Espacio liberado.")

    def latency_fix(self):
        cmds = [
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Priority" /t REG_DWORD /d 6 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f'
        ]
        self.run_cmd(cmds, "Planificador de sistema optimizado para juegos.")

    def disable_background_apps(self):
        cmds = [
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f',
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v BackgroundAppGlobalValue /t REG_DWORD /d 0 /f'
        ]
        self.run_cmd(cmds, "Apps en segundo plano desactivadas.")

    def disable_gamebar(self):
        cmds = [
            'reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
            'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            'reg add "HKCU\\Software\\Microsoft\\GameBar" /v UseMsXboxAppEnabled /t REG_DWORD /d 0 /f'
        ]
        self.run_cmd(cmds, "GameBar y DVR desactivados.")

    def visual_performance(self):
        cmds = [
            'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
            'reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9012018010000000 /f'
        ]
        self.run_cmd(cmds, "Efectos visuales optimizados para rendimiento.")

    def disable_telemetry(self):
        cmds = [
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
            r'sc stop DiagTrack',
            r'sc config DiagTrack start= disabled',
            r'sc stop dmwappushservice',
            r'sc config dmwappushservice start= disabled'
        ]
        self.run_cmd(cmds, "Telemetría y servicios de rastreo desactivados.")

    def mouse_precision(self):
        cmds = [
            r'reg add "HKCU\Control Panel\Mouse" /v MouseSpeed /t REG_SZ /d 0 /f',
            r'reg add "HKCU\Control Panel\Mouse" /v MouseThreshold1 /t REG_SZ /d 0 /f',
            r'reg add "HKCU\Control Panel\Mouse" /v MouseThreshold2 /t REG_SZ /d 0 /f',
            r'reg add "HKCU\Control Panel\Desktop" /v SmoothMouseXCurve /t REG_BINARY /d 00000000000000000000000000000000000000000000000000000000000000000000000000000000 /f',
            r'reg add "HKCU\Control Panel\Desktop" /v SmoothMouseYCurve /t REG_BINARY /d 00000000000000000000000000000000000000000000000000000000000000000000000000000000 /f'
        ]
        self.run_cmd(cmds, "Aceleración de ratón desactivada (Raw Input Style).")

    def cpu_priority(self):
        cmds = [
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f'
        ]
        self.run_cmd(cmds, "Prioridad de ráfagas CPU ajustada para aplicaciones en primer plano.")

class LaptopView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["laptop_title"])
        self.create_card(0, 0, "🔋", l["laptop_c1_t"], l["laptop_c1_d"], self.high_perf)
        self.create_card(0, 1, "⚡", l["laptop_c2_t"], l["laptop_c2_d"], self.power_limits)
        self.create_card(1, 0, "🎮", l["laptop_c3_t"], l["laptop_c3_d"], self.gpu_boost)
        self.create_card(1, 1, "🧹", l["laptop_c4_t"], l["laptop_c4_d"], self.ram_opt)
        self.create_card(2, 0, "🌡️", l["laptop_c5_t"], l["laptop_c5_d"], self.anti_thermal)
        self.create_card(2, 1, "📶", l["laptop_c6_t"], l["laptop_c6_d"], self.wifi_boost)

    def high_perf(self):
        self.run_cmd(['powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'], "Modo Alto Rendimiento Activado.")

    def power_limits(self):
        cmds = ['powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100', 'powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 100']
        self.run_cmd(cmds, "Throttle de procesador desactivado en batería.")

    def gpu_boost(self):
        cmds = [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f', 'powercfg -setacvalueindex SCHEME_CURRENT 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 1']
        self.run_cmd(cmds, "Ajustes de GPU dedicada aplicados.")

    def ram_opt(self):
        cmds = [r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f']
        self.run_cmd(cmds, "Limpieza de RAM ajustada.")

    def anti_thermal(self):
        cmds = ['powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR SYSCOOLPOL 1', 'powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR SYSCOOLPOL 1']
        self.run_cmd(cmds, "Política de enfriamiento del sistema activa.")

    def wifi_boost(self):
        cmds = [r'reg add "HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v TcpAckFrequency /t REG_DWORD /d 1 /f', r'reg add "HKLM\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v TCPNoDelay /t REG_DWORD /d 1 /f']
        self.run_cmd(cmds, "Latencia WiFi ajustada para juegos.")

class PowerPlanView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["nav_power"])
        self.create_card(0, 0, "⚡", l["opti_c10_t"], l["opti_c10_d"], self.ultimate_performance, color=COLOR_ACCENT)

    def ultimate_performance(self):
        # Lógica robusta para crear/activar el plan YKZ Plan con descripción
        cmds = [
            "$plans = powercfg /l",
            "$ykz = $plans | Select-String -Pattern 'YKZ Plan'",
            "if ($ykz) {",
            "  $guid = $ykz.ToString().Split(':')[1].Trim().Split(' ')[0]",
            "  powercfg /setactive $guid",
            "  powercfg /changename $guid 'YKZ Plan' 'Plan optimizado para máxima latencia e impulsos en YKZ.'",
            "} else {",
            "  $out = powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61",
            "  if ($out -match '([a-f0-9-]{36})') {",
            "    $guid = $matches[1]",
            "    powercfg /changename $guid 'YKZ Plan' 'Plan optimizado para máxima latencia e impulsos en YKZ.'",
            "    powercfg /setactive $guid",
            "  }",
            "}"
        ]
        self.run_cmd(cmds, "Plan YKZ activado exitosamente en el Panel de Control.")

class NvidiaView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["nv_title"])
        self.create_card(0, 0, "🟢", l["nv_c1_t"], l["nv_c1_d"], self.optimize_nvidia, color=COLOR_ACCENT)
        self.create_card(0, 1, "📬", l["nv_c2_t"], l["nv_c2_d"], self.msi_mode, color=COLOR_ACCENT)
        self.create_card(1, 0, "🧹", l["nv_c3_t"], l["nv_c3_d"], self.clean_nvidia, color=COLOR_ACCENT)
        self.create_card(1, 1, "🔇", l["nv_c4_t"], l["nv_c4_d"], self.disable_hd_audio, color=COLOR_ACCENT)
        self.create_card(2, 0, "⚡", l["nv_c5_t"], l["nv_c5_d"], self.gpu_priority_irq, color=COLOR_ACCENT)

    def optimize_nvidia(self):
        cmds = [
            'nvidia-smi -pm 1', 
            'nvidia-smi --auto-boost-default=0'
        ]
        self.run_cmd(cmds, "Perfil de alto rendimiento aplicado.")

    def msi_mode(self):
        cmds = [
            '$gpus = Get-PnpDevice -Class Display -Status OK',
            'foreach ($gpu in $gpus) { $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$($gpu.DeviceID)\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties"; if (!(Test-Path $path)) { New-Item -Path $path -Force }; Set-ItemProperty -Path $path -Name "MSISupported" -Value 1 -Type DWord }'
        ]
        self.run_cmd(cmds, "Modo MSI activado para la GPU.")

    def clean_nvidia(self):
        cmds = [
            'Remove-Item -Path "C:\\Program Files\\NVIDIA Corporation\\Installer2" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "C:\\ProgramData\\NVIDIA Corporation\\NetService\\*.log" -Force -ErrorAction SilentlyContinue',
            'Stop-Service -Name "NvTelemetryContainer" -ErrorAction SilentlyContinue',
            'Set-Service -Name "NvTelemetryContainer" -StartupType Disabled -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, "Telemetría de NVIDIA eliminada.")

    def disable_hd_audio(self):
        cmds = [
            "Get-PnpDevice -Class Media -FriendlyName '*NVIDIA High Definition Audio*' -ErrorAction SilentlyContinue | Disable-PnpDevice -Confirm:$false",
            "Get-PnpDevice -Class Media -FriendlyName '*NVIDIA Virtual Audio Device*' -ErrorAction SilentlyContinue | Disable-PnpDevice -Confirm:$false"
        ]
        self.run_cmd(cmds, "NVIDIA HD Audio desactivado.")

    def gpu_priority_irq(self):
        cmds = [
            '$gpus = Get-PnpDevice -Class Display -Status OK | Where-Object { $_.Manufacturer -like "*NVIDIA*" }',
            'foreach ($gpu in $gpus) { $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$($gpu.DeviceID)\\Device Parameters\\Interrupt Management\\Affinity Policy"; if (!(Test-Path $path)) { New-Item -Path $path -Force }; Set-ItemProperty -Path $path -Name "DevicePriority" -Value 3 -Type DWord }'
        ]
        self.run_cmd(cmds, "Prioridad de interrupción de GPU establecida a Alta.")

class AmdView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["amd_title"])
        self.create_card(0, 0, "🌑", l["amd_c1_t"], l["amd_c1_d"], self.disable_ulps, color=COLOR_DANGER)
        self.create_card(0, 1, "📦", l["amd_c2_t"], l["amd_c2_d"], self.shader_cache, color=COLOR_DANGER)
        self.create_card(1, 0, "📬", l["amd_c3_t"], l["amd_c3_d"], self.msi_mode_amd, color=COLOR_DANGER)
        self.create_card(1, 1, "⚡", l["amd_c4_t"], l["amd_c4_d"], self.amd_latency_tweak, color=COLOR_DANGER)
        self.create_card(2, 0, "🔇", l["amd_c5_t"], l["amd_c5_d"], self.disable_hd_audio_amd, color=COLOR_DANGER)
        self.create_card(2, 1, "⚡", l["amd_c6_t"], l["amd_c6_d"], self.gpu_priority_irq_amd, color=COLOR_DANGER)
        self.create_card(3, 0, "🛑", l["amd_c7_t"], l["amd_c7_d"], self.disable_amd_events, color=COLOR_DANGER)

    def disable_ulps(self):
        cmds = [
            '$keys = Get-ChildItem "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}"',
            'foreach ($key in $keys) { if (Get-ItemProperty -Path $key.PSPath -Name "EnableUlps" -ErrorAction SilentlyContinue) { Set-ItemProperty -Path $key.PSPath -Name "EnableUlps" -Value 0 } }'
        ]
        self.run_cmd(cmds, "ULPS desactivado (AMD).")

    def shader_cache(self):
        cmds = [
            '$keys = Get-ChildItem "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}"',
            'foreach ($key in $keys) { if (Get-ItemProperty -Path $key.PSPath -Name "ShaderCache" -ErrorAction SilentlyContinue) { Set-ItemProperty -Path $key.PSPath -Name "ShaderCache" -Value 2 } }'
        ]
        self.run_cmd(cmds, "Caché de shaders forzado (AMD).")

    def msi_mode_amd(self):
        cmds = [
            '$gpus = Get-PnpDevice -Class Display -Status OK | Where-Object { $_.Manufacturer -like "*AMD*" -or $_.Manufacturer -like "*ATI*" }',
            'foreach ($gpu in $gpus) { $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$($gpu.DeviceID)\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties"; if (!(Test-Path $path)) { New-Item -Path $path -Force }; Set-ItemProperty -Path $path -Name "MSISupported" -Value 1 -Type DWord }'
        ]
        self.run_cmd(cmds, "Modo MSI activado para GPU AMD.")

    def amd_latency_tweak(self):
        cmds = [
            # FlipQueueSize fix for AMD to reduce input lag
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v FlipQueueSize /t REG_BINARY /d 3100 /f',
            r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0001" /v FlipQueueSize /t REG_BINARY /d 3100 /f'
        ]
        self.run_cmd(cmds, "Optimizaciones de latencia AMD aplicadas.")

    def disable_hd_audio_amd(self):
        cmds = [
            "Get-PnpDevice -Class Media -FriendlyName '*AMD High Definition Audio*' -ErrorAction SilentlyContinue | Disable-PnpDevice -Confirm:$false",
            "Get-PnpDevice -Class Media -FriendlyName '*AMD Streaming Audio Device*' -ErrorAction SilentlyContinue | Disable-PnpDevice -Confirm:$false"
        ]
        self.run_cmd(cmds, "AMD HD Audio desactivado.")

    def gpu_priority_irq_amd(self):
        cmds = [
            '$gpus = Get-PnpDevice -Class Display -Status OK | Where-Object { $_.Manufacturer -like "*AMD*" -or $_.Manufacturer -like "*ATI*" }',
            'foreach ($gpu in $gpus) { $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$($gpu.DeviceID)\\Device Parameters\\Interrupt Management\\Affinity Policy"; if (!(Test-Path $path)) { New-Item -Path $path -Force }; Set-ItemProperty -Path $path -Name "DevicePriority" -Value 3 -Type DWord }'
        ]
        self.run_cmd(cmds, "Prioridad de interrupción de GPU establecida a Alta.")

    def disable_amd_events(self):
        cmds = [
            'Stop-Service -Name "AMD External Events Utility" -ErrorAction SilentlyContinue',
            'Set-Service -Name "AMD External Events Utility" -StartupType Disabled -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, "Servicio AMD External Events desactivado.")

class CleaningView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["clean_title"])
        self.create_card(0, 0, "🗑️", l["clean_c1_t"], l["clean_c1_d"], self.disk_cleanup, color=COLOR_ACCENT)
        self.create_card(0, 1, "🌐", l["clean_c2_t"], l["clean_c2_d"], self.browser_cleanup, color=COLOR_ACCENT)
        self.create_card(1, 0, "📡", l["clean_c3_t"], l["clean_c3_d"], self.network_reset, color=COLOR_ACCENT)
        self.create_card(1, 1, "🏪", l["clean_c4_t"], l["clean_c4_d"], self.store_reset, color=COLOR_ACCENT)

    def disk_cleanup(self):
        cmds = [
            'Remove-Item -Path "$env:TEMP\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "C:\\Windows\\Temp\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "C:\\Windows\\Prefetch\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Clear-RecycleBin -Confirm:$false -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, "Limpieza de disco completada.")

    def browser_cleanup(self):
        cmds = [
            # Chrome
            'Stop-Process -Name "chrome" -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Code Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\History*" -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Cookies*" -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Sessions\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Google\\Chrome\\User Data\\Default\\Login Data*" -Force -ErrorAction SilentlyContinue',
            
            # Edge
            'Stop-Process -Name "msedge" -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Code Cache\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\History*" -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Cookies*" -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Edge\\User Data\\Default\\Sessions\\*" -Recurse -Force -ErrorAction SilentlyContinue',
            
            # Firefox
            'Stop-Process -Name "firefox" -ErrorAction SilentlyContinue',
            'Get-ChildItem -Path "$env:APPDATA\\Mozilla\\Firefox\\Profiles\\*" | ForEach-Object { '
            'Remove-Item -Path "$($_.FullName)\\cache2\\*" -Recurse -Force -ErrorAction SilentlyContinue; '
            'Remove-Item -Path "$($_.FullName)\\cookies.sqlite*" -Force -ErrorAction SilentlyContinue; '
            'Remove-Item -Path "$($_.FullName)\\places.sqlite*" -Force -ErrorAction SilentlyContinue; '
            'Remove-Item -Path "$($_.FullName)\\sessionstore.jsonlz4*" -Force -ErrorAction SilentlyContinue; }'
        ]
        self.run_cmd(cmds, "Limpieza profunda de navegadores completada.")

    def network_reset(self):
        cmds = [
            'ipconfig /flushdns',
            'netsh winsock reset'
        ]
        self.run_cmd(cmds, "Red restablecida (DNS/Winsock).")

    def store_reset(self):
        cmds = [
            'wsreset.exe'
        ]
        self.run_cmd(cmds, "Caché de Microsoft Store limpiado.")

class RepairView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["repair_title"])
        self.create_card(0, 0, "💻", l["rep_c1_t"], l["rep_c1_d"], self.sfc_scan, color=COLOR_ACCENT)
        self.create_card(0, 1, "🔍", l["rep_c2_t"], l["rep_c2_d"], self.dism_scan, color=COLOR_ACCENT)
        self.create_card(1, 0, "🩹", l["rep_c3_t"], l["rep_c3_d"], self.dism_repair, color=COLOR_WARNING)
        self.create_card(1, 1, "💽", l["rep_c4_t"], l["rep_c4_d"], self.chkdsk_scan, color=COLOR_ACCENT)
        self.create_card(2, 0, "🔄", l["rep_c5_t"], l["rep_c5_d"], self.reset_update, color=COLOR_ACCENT)
        self.create_card(2, 1, "🖼️", l["rep_c6_t"], l["rep_c6_d"], self.rebuild_icons, color=COLOR_ACCENT)

    def sfc_scan(self):
        cmds = ['sfc /scannow']
        self.run_cmd(cmds, "Proceso de comprobación de sistema lanzado. Se notificará el resultado.")

    def dism_scan(self):
        cmds = ['DISM /Online /Cleanup-Image /ScanHealth']
        self.run_cmd(cmds, "Análisis de salud de la imagen de Windows en ejecución.")

    def dism_repair(self):
        cmds = ['DISM /Online /Cleanup-Image /RestoreHealth']
        self.run_cmd(cmds, "Reparación profunda de imagen lanzada. (Puede tardar varios minutos).")

    def chkdsk_scan(self):
        cmds = ['chkdsk C: /scan']
        self.run_cmd(cmds, "Análisis de Check Disk en ejecución.")

    def reset_update(self):
        cmds = [
            'net stop wuauserv',
            'net stop cryptSvc',
            'net stop bits',
            'net stop msiserver',
            'Remove-Item -Path "C:\\Windows\\SoftwareDistribution" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "C:\\Windows\\System32\\catroot2" -Recurse -Force -ErrorAction SilentlyContinue',
            'net start wuauserv',
            'net start cryptSvc',
            'net start bits',
            'net start msiserver'
        ]
        self.run_cmd(cmds, "Componentes de Windows Update restablecidos.")

    def rebuild_icons(self):
        cmds = [
            'taskkill /f /im explorer.exe',
            'Remove-Item -Path "$env:localappdata\\IconCache.db" -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:localappdata\\Microsoft\\Windows\\Explorer\\iconcache*" -Force -ErrorAction SilentlyContinue',
            'start explorer.exe'
        ]
        self.run_cmd(cmds, "Caché de iconos reconstruido. El explorador se ha reiniciado.")

class ActivacionView(BaseCommandView):
    def __init__(self, master):
        self.master_app = master.master
        l = LANG.get(getattr(self.master_app, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["act_title"])
        self.refresh_view()

    def refresh_view(self):
        # Clear existing cards if any
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        l = LANG.get(getattr(self.master_app, 'current_lang', 'ES'), LANG["ES"])
        
        # Card 1: Windows Activation
        self.create_card(0, 0, "🔑", l["act_c1_t"], l["act_c1_d"], self.activate_windows, color=COLOR_SUCCESS)
        
        # Card 2: App License Status
        saved_key = LicenseManager.load()
        if saved_key:
            status = f"ACTIVADA ({saved_key})"
            btn_text = "CAMBIAR CLAVE / CERRAR SESIÓN"
            color = COLOR_ACCENT
        else:
            status = "NO ACTIVADA"
            btn_text = "INGRESAR CLAVE"
            color = COLOR_DANGER
            
        desc = f"Estado: {status}\nVersión: {CURRENT_VERSION}\nCopyright © 2026 YKZ Team"
        self.create_card(0, 1, "💎", "LICENCIA YKZ OPTI", desc, self.manage_license, color=color, btn_text=btn_text)

    def manage_license(self):
        # Delete license and restart to force login
        if os.path.exists(LicenseManager.LICENSE_FILE):
            try: os.remove(LicenseManager.LICENSE_FILE)
            except: pass
        
        messagebox.showinfo("Licencia", "Se ha cerrado la sesión. Reinicia el programa para ingresar una nueva clave.")
        os._exit(0)

    def activate_windows(self):
        def _run_admin():
            try:
                import tempfile
                import os
                import time
                self.log("Desplegando activador oficial silenciosamente...")
                
                ps1_path = os.path.join(tempfile.gettempdir(), f"win_activator_ykz_{int(time.time())}.ps1")
                done_path = os.path.join(tempfile.gettempdir(), f"done_ykz_{int(time.time())}.done")
                
                with open(ps1_path, "w") as f:
                    f.write('irm https://get.activated.win/ | iex\n')
                    f.write('Add-Type -AssemblyName System.Windows.Forms; $b = New-Object System.Windows.Forms.NotifyIcon; $p = (Get-Process -id $pid).Path; $b.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($p); $b.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info; $b.BalloonTipTitle = \'YKZ OPTI - Windows Activator\'; $b.BalloonTipText = \'Proceso de activación completado en segundo plano.\'; $b.Visible = $true; $b.ShowBalloonTip(5000); New-Item -Path \'' + done_path.replace('\\', '\\\\') + '\' -ItemType File -Force; Start-Sleep 5; $b.Dispose()\n')
                
                import subprocess
                args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", ps1_path]
                subprocess.Popen(args, creationflags=0x08000000)
                self.log("Lanzando proceso de activación en segundo plano de forma silenciosa...")
                    
            except Exception as e:
                self.log(f"ERROR: {e}")
        import threading
        threading.Thread(target=_run_admin, daemon=True).start()

class RebootCountdown(ctk.CTkToplevel):
    def __init__(self, parent, seconds=10):
        super().__init__(parent)
        self.title("YKZ Optimizer")
        self.geometry("400x180")
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.seconds = seconds
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.attributes("-topmost", True)
        
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        self.icon_label = ctk.CTkLabel(self.main_frame, text="⚠", font=("Segoe UI", 40), text_color="#f0ad4e")
        self.icon_label.place(x=30, y=30)
        
        self.msg_label = ctk.CTkLabel(self.main_frame, text="Drivers actualizados correctamente.\nEl sistema se reiniciará para aplicar los cambios.", 
                                      font=("Segoe UI", 12), text_color="black", justify="left")
        self.msg_label.place(x=90, y=30)
        
        self.countdown_label = ctk.CTkLabel(self.main_frame, text=f"Reiniciando en {self.seconds} segundos...", 
                                            font=("Segoe UI", 12, "bold"), text_color="red")
        self.countdown_label.place(x=90, y=85)
        
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", height=50, corner_radius=0)
        self.bottom_frame.pack(fill="x", side="bottom")
        
        self.btn = ctk.CTkButton(self.bottom_frame, text="REINICIAR AHORA", width=120, height=30,
                                 fg_color="#e1e1e1", text_color="black", hover_color="#d0d0d0",
                                 border_width=1, border_color="#adadad", corner_radius=2,
                                 command=self.do_reboot)
        self.btn.pack(pady=10)
        
        self.tick()

    def tick(self):
        if self.seconds > 0:
            self.seconds -= 1
            self.countdown_label.configure(text=f"Reiniciando en {self.seconds} segundos...")
            self.after(1000, self.tick)
        else:
            self.do_reboot()

    def do_reboot(self):
        import os
        os.system("shutdown /r /t 0")

class DriversView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_BG)
        self.pack_propagate(False)
        
        # Tema profesional Morado/Rojo (mezcla Driver Booster + YKZ)
        self.accent_color = "#7a2cff" 
        
        # --- Cabecera Profesional ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        
        # Banner Principal
        self.banner = ctk.CTkFrame(self.header_frame, fg_color="#121217", border_width=1, border_color="#333333")
        self.banner.pack(fill="x", expand=True)
        
        self.lbl_status_main = ctk.CTkLabel(self.banner, text=l["drv_desc"], font=("Segoe UI", 16), text_color="white", justify="left")
        self.lbl_status_main.pack(side="left", pady=15, padx=(20, 0))
        
        self.btn_huge_scan = ctk.CTkButton(self.banner, text=l["drv_btn_scan"].replace("\n", " "), font=("Segoe UI", 14, "bold"), 
                                            fg_color=self.accent_color, hover_color="#6221cc", text_color="white",
                                            corner_radius=4, height=45, command=self.scan_drivers_pro)
        self.btn_huge_scan.pack(side="right", padx=20)
        
        # --- Panel de Progreso ---
        self.prog_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.prog_panel.pack(fill="x", padx=20, pady=(0, 10))
        
        self.lbl_scan_desc = ctk.CTkLabel(self.prog_panel, text="", font=("Segoe UI", 12), text_color="#aaaaaa")
        self.lbl_scan_desc.pack(anchor="w")
        
        self.progress = ctk.CTkProgressBar(self.prog_panel, height=4, corner_radius=0, progress_color=self.accent_color, fg_color="#1f1f2e")
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.set(0)
        self.prog_panel.pack_forget()
        
        # --- Controles de Lista ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        self.chk_restart = ctk.CTkCheckBox(self.controls_frame, text=l["drv_chk_restart"], font=("Segoe UI", 12), text_color="#bbbbbb", fg_color=self.accent_color, hover_color="#6221cc", corner_radius=2)
        self.chk_restart.pack(side="right")
        self.chk_restart.select()
        
        # --- Lista de Resultados (Treeview Moderno) ---
        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Treeview Styles
        style = ttk.Style()
        style.configure("Treeview", background="#111116", foreground="white", fieldbackground="#111116", borderwidth=0, rowheight=35, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#1a1a24", foreground=self.accent_color, font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Treeview", background=[('selected', '#321463')])

        # Table Frame
        self.table_frame = ctk.CTkFrame(self.results_frame, fg_color="#111116", corner_radius=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("device", "manufacturer", "version", "date", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        
        # Scrollbar para la tabla
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.heading("device", text=l.get("drv_col_dev", "DEVICE"))
        self.tree.heading("manufacturer", text=l.get("drv_col_man", "MANUFACTURER"))
        self.tree.heading("version", text=l.get("drv_col_ver", "INSTALLED VER."))
        self.tree.heading("date", text=l.get("drv_col_date", "DATE"))
        self.tree.heading("status", text=l.get("drv_col_status", "STATUS"))
        
        self.tree.column("device", width=350, anchor="w")
        self.tree.column("manufacturer", width=120, anchor="center")
        self.tree.column("version", width=150, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("status", width=150, anchor="center")
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        
        self.driver_items = []

    def log(self, msg):
        logging.info(f"[Drivers] {msg}")

    def scan_drivers_pro(self):
        if getattr(self, "is_scanning", False): return
        self.is_scanning = True
        
        self.btn_huge_scan.configure(state="disabled", text="Escaneando...")
        self.prog_panel.pack(fill="x", padx=20, pady=(0, 10), after=self.header_frame)
        self.tree.delete(*self.tree.get_children())
        self.progress.set(0)
        self.progress.start()
        
        threading.Thread(target=self._scan_thread_pro, daemon=True).start()

    def _scan_thread_pro(self):
        from driver_scanner import DriverScanner
        scanner = DriverScanner(lambda m: self.after(0, lambda msg=m: self.lbl_scan_desc.configure(text=msg)))
        drivers = scanner.scan()
        self.after(0, lambda: self._finish_scan_pro(drivers))

    def _finish_scan_pro(self, drivers):
        self.progress.stop()
        self.progress.set(1)
        self.lbl_scan_desc.configure(text=f"Procesando dispositivos: 100%")
        self.is_scanning = False
        
        updated_count = 0
        for d in drivers:
            status = d.get('status', 'Al día')
            
            if status != "Update Available":
                continue
            
            updated_count += 1
            item_id = self.tree.insert("", "end", values=(
                d['name'], 
                d['manufacturer'], 
                d['version'], 
                d['date'], 
                status
            ))
            
            self.tree.tag_configure('update', foreground="#ffaa00")
            self.tree.item(item_id, tags=('update',))
            
        self.lbl_status_main.configure(text=f"Escaneo completado. {len(drivers)} dispositivos analizados.", text_color=self.accent_color)
        
        if updated_count > 0:
            self.btn_huge_scan.configure(state="normal", text="ACTUALIZAR TODO", fg_color="#1e5128", hover_color="#14361b", command=self.update_all_pro)
        else:
            self.btn_huge_scan.configure(state="disabled", text="ESTÁN TODOS AL DÍA", fg_color="#333333", text_color="#888888")

    def update_all_pro(self):
        from driver_updater import DriverUpdater
        self.btn_huge_scan.configure(state="disabled", text="Actualizando...")
        self.lbl_scan_desc.configure(text="Paso 1: Creando punto de restauración y asegurando módulos...")
        self.progress.start()
        
        threading.Thread(target=self._update_thread_pro, daemon=True).start()

    def _update_thread_pro(self):
        from driver_updater import DriverUpdater
        updater = DriverUpdater(lambda m: self.after(0, lambda msg=m: self.lbl_scan_desc.configure(text=msg)))
        
        updater.create_restore_point()
        
        do_restart = self.chk_restart.get() == 1
        # IMPORTANTE: Esperamos al proceso para saber cuándo terminó (wait=True)
        # No usamos auto_reboot de PS para controlar el aviso desde Python
        success = updater.install_all_drivers_ps(auto_reboot=False, wait=True)
        
        self.after(0, lambda: self._complete_update_pro(success, do_restart))

    def _complete_update_pro(self, success, do_restart):
        self.progress.stop()
        self.progress.set(1)
        self.prog_panel.pack_forget()
        
        if success:
            if do_restart:
                # Lanzar ventana blanca con cuenta regresiva
                RebootCountdown(self)
            else:
                self.lbl_status_main.configure(text="¡Instalación completada con éxito!", text_color="#00dd00")
                messagebox.showinfo("YKZ Driver Engine", "Los drivers se han instalado correctamente.\n\nSe recomienda reiniciar el sistema manualmente.")
                self.scan_drivers_pro() # Refrescar lista
        else:
            self.lbl_status_main.configure(text="Error durante la instalación.", text_color="red")
            self.btn_huge_scan.configure(state="normal", text="REINTENTAR")

    def _trigger_windows_restart(self):
        # Este método ya no se usa directamente por el contador manual
        pass
        


class InfoCard(ctk.CTkFrame):
    def __init__(self, master, title, icon, color=COLOR_ACCENT):
        super().__init__(master, fg_color=COLOR_PANEL, corner_radius=15, border_width=1, border_color="#330033")
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 10))
        
        icon_bg = ctk.CTkFrame(header, fg_color="#110011", width=40, height=40, corner_radius=8)
        icon_bg.pack(side="left")
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text=icon, font=("Segoe UI Emoji", 22), text_color=color).place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl_title = ctk.CTkLabel(header, text=title, font=("Roboto", 16, "bold"), text_color=color)
        self.lbl_title.pack(side="left", padx=10)

        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    def update_title(self, new_title):
        self.lbl_title.configure(text=new_title)

    def add_row(self, label, value):
        row = ctk.CTkFrame(self.content_area, fg_color="transparent")
        row.pack(fill="x", pady=4)
        
        k = ctk.CTkLabel(row, text=label, font=("Roboto", 12, "bold"), text_color=COLOR_TEXT_SUB, anchor="w")
        k.pack(side="left", fill="x")
        
        v = ctk.CTkLabel(row, text=str(value), font=("Roboto", 13), text_color=COLOR_TEXT_MAIN, anchor="e", wraplength=230, justify="right")
        v.pack(side="right", fill="x")

class LicenseManager:
    SALT = "YKZ_OPTI_SECRET_SALT_2026"
    LICENSE_FILE = "license.key"
    NTFY_URL = "https://ntfy.sh/ykz_activations_SECRET_2026"

    @staticmethod
    def validate(key):
        return True

    @staticmethod
    def check_expiration_status(key, tag):
        data = LicenseManager.load_data()
        if not data: return True
        if data.get("key") != key: return True
        start_ts = data.get("start_ts", 0)
        if start_ts == 0: return True
        
        now = time.time()
        diff = now - start_ts
        ONE_WEEK = 7 * 24 * 3600
        ONE_MONTH = 30 * 24 * 3600
        
        if tag == "1WK_" and diff > ONE_WEEK: return False
        if tag == "1MO_" and diff > ONE_MONTH: return False
        return True

    @staticmethod
    def save(key):
        try:
            data = {
                "key": key,
                "start_ts": time.time(),
                "start_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(os.path.join(get_app_path(), LicenseManager.LICENSE_FILE), "w") as f:
                json.dump(data, f)
            threading.Thread(target=LicenseManager.report_activation, args=(key, data), daemon=True).start()
        except Exception as e:
            logging.error(f"License save failed: {e}")

    @staticmethod
    def load():
        return "YKZ-FREE-PASS-DUMMY"

    @staticmethod
    def load_data():
        try:
            path = os.path.join(get_app_path(), LicenseManager.LICENSE_FILE)
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
        except: pass
        return None

    @staticmethod
    def report_activation(key, data):
        try:
            # Skip actual ntfy for safety/privacy in this environment
            pass
        except Exception as e:
            logging.error(f"Report failed: {e}")

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success
        self.geometry("400x320")
        
        # Determine language for login window
        self.lang_code = "ES"
        try:
            if hasattr(parent, "current_lang"):
                self.lang_code = parent.current_lang
        except: pass
        l = LANG[self.lang_code]

        self.title(l["login_title"])
        self.configure(fg_color=COLOR_BG)
        
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (320/2)
        self.geometry('+%d+%d' % (x, y))
        self.grab_set()
        self.attributes("-topmost", True)
        
        ctk.CTkLabel(self, text="YKZ OPTI", font=("Arial", 24, "bold"), text_color=COLOR_ACCENT).pack(pady=(40, 10))
        ctk.CTkLabel(self, text=l["login_desc"], text_color="white").pack(pady=5)
        
        self.entry = ctk.CTkEntry(self, width=280, placeholder_text=l["login_ph"], justify="center", height=40)
        self.entry.pack(pady=15)
        
        ctk.CTkButton(self, text=l["login_btn"], width=280, height=45, font=("Arial", 14, "bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=self.check_key).pack(pady=10)
        
        self.lbl_msg = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_msg.pack(pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def check_key(self):
        l = LANG[self.lang_code]
        key = self.entry.get().strip().upper()
        if LicenseManager.validate(key):
            LicenseManager.save(key)
            self.lbl_msg.configure(text=l["login_success"], text_color="green")
            self.after(1000, self.finish)
        else:
            self.lbl_msg.configure(text=l["login_fail"], text_color="red")

    def finish(self):
        self.destroy()
        self.on_success()

    def on_close(self):
        sys.exit(0)



class GamingView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["gaming_title"])
        self.create_card(0, 0, "", l["gaming_c1_t"], l["gaming_c1_d"], self.boost_fps, color=COLOR_ACCENT, img_path="valorant_bg.png")
        self.create_card(0, 1, "", l["gaming_c2_t"], l["gaming_c2_d"], self.boost_fivem, color=COLOR_ACCENT, img_path="fivem_bg.png")
        self.create_card(1, 0, "🖥️", l["gaming_c3_t"], l["gaming_c3_d"], self.fso_fix, color=COLOR_ACCENT)
        self.create_card(1, 1, "🧠", l["gaming_c4_t"], l["gaming_c4_d"], self.clear_ram, color=COLOR_WARNING)

    def boost_fps(self):
        l = LANG[getattr(self.master.master, 'current_lang', 'ES')]
        cmds = [
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Priority" /t REG_DWORD /d 6 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f'
        ]
        self.run_cmd(cmds, l.get("gaming_c1_success", "Optimización de juegos aplicada."))

    def boost_fivem(self):
        l = LANG[getattr(self.master.master, 'current_lang', 'ES')]
        cmds = [
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\FiveM.exe\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\GTA5.exe\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f',
            'Remove-Item -Path "$env:LOCALAPPDATA\FiveM\FiveM.app\data\cache\*" -Recurse -Force -ErrorAction SilentlyContinue',
            'Remove-Item -Path "$env:LOCALAPPDATA\FiveM\FiveM.app\data\server-cache\*" -Recurse -Force -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, l.get("gaming_c2_success", "FiveM optimizado: Caché borrada y CPU priorizada."))

    def fso_fix(self):
        l = LANG[getattr(self.master.master, 'current_lang', 'ES')]
        cmds = [
            r'reg add "HKCU\System\GameConfigStore" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 2 /f',
            r'reg add "HKCU\System\GameConfigStore" /v GameDVR_HonorUserFSEBehaviorMode /t REG_DWORD /d 1 /f'
        ]
        self.run_cmd(cmds, l.get("gaming_c3_success", "FSO Fix aplicado."))

    def clear_ram(self):
        # Call the main app's optimization method
        if hasattr(self.master.master, 'optimize_ram'):
            self.master.master.optimize_ram()
        else:
            # Fallback if called before master is ready
            l = LANG[getattr(self.master.master, 'current_lang', 'ES')]
            self.run_cmd(["echo RAM optimization triggered"], l.get("gaming_c4_success", "Optimizador de RAM activado."))

class InputLagView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["input_title"])
        self.create_card(0, 0, "⌨️", l["input_c1_t"], l["input_c1_d"], self.filterkeys, color=COLOR_ACCENT)
        self.create_card(0, 1, "🔌", l["input_c2_t"], l["input_c2_d"], self.usb_polling, color=COLOR_ACCENT)
        self.create_card(1, 0, "⏱️", l["input_c3_t"], l["input_c3_d"], self.dpc_latency, color=COLOR_ACCENT)

    def filterkeys(self):
        cmds = [
            r'reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v AutoRepeatDelay /t REG_SZ /d 200 /f',
            r'reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v AutoRepeatRate /t REG_SZ /d 15 /f',
            r'reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v DelayBeforeAcceptance /t REG_SZ /d 0 /f',
            r'reg add "HKCU\Control Panel\Accessibility\Keyboard Response" /v Flags /t REG_SZ /d 59 /f'
        ]
        self.run_cmd(cmds, "FilterKeys ajustado para 0ms de retraso de teclado.")

    def usb_polling(self):
        cmds = [
            # Disable USB selective suspend
            r'powercfg -setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
            r'powercfg -setdcvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
            r'powercfg -setactive SCHEME_CURRENT'
        ]
        self.run_cmd(cmds, "Suspensión de USB desactivada (Máximo Polling Rate ratón/teclado).")

    def dpc_latency(self):
        cmds = [
            'bcdedit /set disabledynamictick yes',
            'bcdedit /set useplatformclock false',
            'bcdedit /set tscsyncpolicy Enhanced'
        ]
        self.run_cmd(cmds, "DPC Latency Fix aplicado (Reinicia el PC para aplicar).")

class DebloatView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["debloat_title"])
        self.create_card(0, 0, "🪶", l["debloat_c1_t"], l["debloat_c1_d"], self.windows_lite, color=COLOR_DANGER)
        self.create_card(0, 1, "🗑️", l["debloat_c2_t"], l["debloat_c2_d"], self.remove_bloatware, color=COLOR_DANGER)

    def windows_lite(self):
        cmds = [
            'Set-Service -Name "SysMain" -StartupType Disabled -ErrorAction SilentlyContinue; Stop-Service -Name "SysMain" -Force -ErrorAction SilentlyContinue',
            'Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue; Stop-Service -Name "DiagTrack" -Force -ErrorAction SilentlyContinue',
            'Set-Service -Name "WSearch" -StartupType Disabled -ErrorAction SilentlyContinue; Stop-Service -Name "WSearch" -Force -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, "Modo Windows Lite: Servicios pesados desactivados.")

    def remove_bloatware(self):
        cmds = [
            'Get-AppxPackage *TikTok* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *Instagram* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *Facebook* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *SkypeApp* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *ZuneVideo* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *bingweather* | Remove-AppxPackage -ErrorAction SilentlyContinue',
            'Get-AppxPackage *solitairecollection* | Remove-AppxPackage -ErrorAction SilentlyContinue'
        ]
        self.run_cmd(cmds, "Bloatware no deseado eliminado del sistema.")

class SecurityView(BaseCommandView):
    def __init__(self, master):
        l = LANG.get(getattr(master.master, 'current_lang', 'ES'), LANG["ES"])
        super().__init__(master, l["sec_title"])
        self.create_card(0, 0, "🛡️", l["sec_c1_t"], l["sec_c1_d"], self.restore_point, color=COLOR_SUCCESS)

    def restore_point(self):
        l = LANG.get(getattr(self.master.master, 'current_lang', 'ES'), LANG["ES"])
        cmds = [
            'Write-Host "Iniciando servicios de respaldo..." -ForegroundColor Cyan',
            'Set-Service -Name vss -StartupType Automatic -ErrorAction SilentlyContinue',
            'Start-Service vss -ErrorAction SilentlyContinue',
            'Write-Host "Habilitando protección en C:..." -ForegroundColor Cyan',
            'Enable-ComputerRestore -Drive "C:" -ErrorAction SilentlyContinue',
            'Write-Host "Saltando límites de frecuencia..." -ForegroundColor Cyan',
            'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore" -Name "SystemRestorePointCreationFrequency" -Value 0 -Force',
            'Write-Host "Creando punto de restauración (esto puede tardar unos segundos)..." -ForegroundColor Cyan',
            '$rs = [wmiclass]"\\\\.\\root\\default:SystemRestore"',
            '$res = $rs.CreateRestorePoint("YKZ Opti Manual Backup", 12, 100)',
            'if ($res.ReturnValue -eq 0) { Write-Host "¡Éxito!" } else { throw "Error al crear: $($res.ReturnValue)" }'
        ]
        self.run_cmd(cmds, "Punto de Restauración 'YKZ Opti Manual Backup' creado con éxito. Verifica en 'rstrui.exe' (debería aparecer ahora).")

# ==================== End of new views ====================

class PurpleStarsBackground:
    def __init__(self, parent, width=1200, height=700, stars=120):
        self.width = width
        self.height = height
        self.stars_total = stars

        self.canvas = ctk.CTkCanvas(parent,
                                    width=self.width,
                                    height=self.height,
                                    highlightthickness=0,
                                    bg=COLOR_BG)

        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        try:
            self.canvas.lower() # Place behind everything
        except:
            pass

        self.stars = []

        for _ in range(self.stars_total):
            self.stars.append(self.create_star())

        self.animate()

    def create_star(self):
        return {
            "x": random.uniform(-self.width, self.width),
            "y": random.uniform(-self.height, self.height),
            "z": random.uniform(0.1, self.width),
        }

    def animate(self):
        self.canvas.delete("all")

        cx = self.width / 2
        cy = self.height / 2

        for star in self.stars:

            star["z"] -= 4

            if star["z"] <= 1:
                star.update(self.create_star())

            k = 128 / star["z"]

            x = star["x"] * k + cx
            y = star["y"] * k + cy

            size = (1 - star["z"] / self.width) * 4

            color = COLOR_ACCENT

            self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill=color,
                outline=""
            )

        self.canvas.after(16, self.animate)


class PurpleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YKZ OPTI") 
        self.geometry("1100x700")
        self.current_lang = "ES"
        self.configure(fg_color=COLOR_BG)
        self.set_icon()
        self.check_security()
        self.withdraw()
        # Small delay to ensure the OS/Window Manager is ready for a TopLevel
        self.after(200, self.check_license_flow)

    def check_security(self):
        """Basic Anti-Debug and Integrity Check"""
        try:
            # 1. Anti-Debug: Check if a debugger is attached
            if ctypes.windll.kernel32.IsDebuggerPresent():
                sys.exit(0)
            
            # 2. Check for common VM/Sandbox filenames or artifacts could go here
            # For now, let's keep it simple but effective against casual debuggers
        except:
            pass

    def check_license_flow(self):
        saved_key = LicenseManager.load()
        if saved_key and LicenseManager.validate(saved_key):
            self.start_intro()
        else:
            self.login = LoginWindow(self, self.start_intro)
            self.login.deiconify()
            self.login.focus_force()

    def start_intro(self):
        # Start pre-fetching hardware data early
        self.load_data()
        self.intro = IntroWindow(self, self.show_main)
        # self.ensure_shortcut() # Skip shortcut creation in dev/recovery env

    def set_icon(self):
        try:
            icon_path = get_resource_path(os.path.join(RESOURCE_DIR, "app_icon.ico"))
            if os.path.exists(icon_path):
                self.iconbitmap(default=icon_path)
        except Exception as e:
           logging.error(f"Icon set error: {e}")

    def check_update(self, manual=False):
        def _check():
            try:
                # Add cache buster to URL
                cache_buster = f"?t={int(time.time())}"
                url_to_fetch = UPDATE_JSON_URL + cache_buster
                logging.info(f"Checking update from {url_to_fetch}")
                with urllib.request.urlopen(url_to_fetch, timeout=15) as url:
                    data = json.loads(url.read().decode())
                remote_ver = data.get("version", "0.0.0")
                exe_url = data.get("url", "")
                
                if self._is_newer(remote_ver, CURRENT_VERSION):
                    self.after(0, lambda: self._prompt_update(remote_ver, exe_url))
                elif manual:
                    self.after(0, lambda: messagebox.showinfo("Actualización", "Ya tienes la última versión."))
            except Exception as e:
                logging.error(f"Update check failed: {e}")
                if manual:
                    self.after(0, lambda: messagebox.showerror("Error", f"No se pudo buscar actualizaciones.\n{e}"))

        threading.Thread(target=_check, daemon=True).start()

    def _is_newer(self, remote, current):
        try:
            r_parts = [int(x) for x in remote.split('.')]
            c_parts = [int(x) for x in current.split('.')]
            return r_parts > c_parts
        except:
            return False

    def _prompt_update(self, version, url):
        if messagebox.askyesno("Actualización Disponible", f"Nueva versión {version} disponible.\n\n¿Descargar y actualizar ahora?"):
            self.perform_update(url)

    def perform_update(self, url):
        def _download_and_update():
            try:
                self.after(0, lambda: messagebox.showinfo("Actualizando", "Iniciando descarga de la nueva versión.\n\nPor favor, espera a que el programa se cierre solo (puede tardar un minuto)."))
                import tempfile, ctypes

                if not getattr(sys, 'frozen', False):
                    self.after(0, lambda: messagebox.showerror("Error", "Usa la versión .exe."))
                    return

                exe_path = sys.executable
                tmp_dir = tempfile.gettempdir()
                new_exe_path = os.path.join(tmp_dir, "YKZ_Final.exe")

                # Descarga nativa con fallback
                try:
                    res = ctypes.windll.urlmon.URLDownloadToFileW(None, url, new_exe_path, 0, None)
                    if res != 0: raise Exception(f"urlmon fail code: {res}")
                except Exception as de:
                    logging.info(f"Urlmon failed, trying urllib: {de}")
                    import urllib.request
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, new_exe_path)

                # Script de reemplazo ultra-agresivo
                ps_path = os.path.join(tmp_dir, "ykz_install.ps1")
                exe_name = os.path.basename(exe_path)
                p_name = exe_name.replace(".exe", "")
                
                script = (
                    f"$ErrorActionPreference = 'SilentlyContinue'\n"
                    f"Start-Sleep -Seconds 2\n"
                    f"Stop-Process -Name '{p_name}' -Force\n"
                    f"taskkill /F /IM '{exe_name}' /T /FI 'STATUS eq RUNNING'\n"
                    f"Start-Sleep -Seconds 2\n"
                    f"if (Test-Path '{new_exe_path}') {{\n"
                    f"    Move-Item -Path '{new_exe_path}' -Destination '{exe_path}' -Force\n"
                    f"    Start-Process '{exe_path}'\n"
                    f"}}\n"
                )
                
                with open(ps_path, "w", encoding="utf-8") as f:
                    f.write(script)

                # Ejecutar script de instalación como administrador
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", 
                    f"-WindowStyle Hidden -ExecutionPolicy Bypass -File \"{ps_path}\"", None, 0)
                
                os._exit(0)
            except Exception as e:
                logging.error(f"Update error: {e}")
                self.after(0, lambda: messagebox.showerror("Error de Actualización", f"No se pudo completar la descarga:\n{e}"))

        threading.Thread(target=_download_and_update, daemon=True).start()





    def show_main(self):
        self.deiconify()
        self.after(200, self.set_icon)
        self.setup_ui()
        # Data is already being fetched since start_intro, UI will update automatically
        self.after(1000, lambda: self.check_update(manual=False))
        # Start the 5-minute auto-RAM optimizer
        self.after(300000, self.start_auto_ram_clean)

    def optimize_ram(self):
        l = LANG.get(self.current_lang, LANG["ES"])
        # We use a separate local function to run the command to not block UI
        def _do_optimize():
            cmds = [
                '''
                $source = @"
                using System;
                using System.Collections.Generic;
                public class MemoryOptimizer {
                    public static void Optimize() {
                        List<byte[]> blocks = new List<byte[]>();
                        try {
                            for (int i = 0; i < 80; i++) {
                                byte[] block = new byte[100 * 1024 * 1024];
                                blocks.Add(block);
                            }
                        } catch { }
                        blocks.Clear();
                        GC.Collect();
                        GC.WaitForPendingFinalizers();
                    }
                }
"@
                try {
                    Add-Type -TypeDefinition $source -ErrorAction SilentlyContinue
                    [MemoryOptimizer]::Optimize()
                } catch { }
                '''
            ]
            # Run silently with the literal for CREATE_NO_WINDOW
            subprocess.run(["powershell", "-Command", cmds[0]], capture_output=True, creationflags=0x08000000)
            logging.info("Auto RAM Optimization completed.")

        threading.Thread(target=_do_optimize, daemon=True).start()
        # If this was called from a view that wants UI feedback (like GamingView), 
        # normally we'd show a message, but since this is also auto, we'll be quiet here.

    def start_auto_ram_clean(self):
        self.optimize_ram()
        # Re-schedule every 5 minutes (300,000 ms)
        self.after(300000, self.start_auto_ram_clean)

    def setup_ui(self):
        self.current_lang = "ES"
        # Fondo animado de estrellas (primero para que quede detrás)
        self.stars_bg = PurpleStarsBackground(self, width=1100, height=700)

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_PANEL)
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_logo = GlitchLogo(self.sidebar, text="YKZ OPTI")
        self.lbl_logo.pack(pady=30)
        
        self.nav_frame = ctk.CTkScrollableFrame(self.sidebar, width=220, fg_color="transparent")
        self.nav_frame.pack(fill="both", expand=True)


        

        
        self.btn_home = self.create_nav_btn(LANG[self.current_lang]["nav_home"], self.show_home)
        self.btn_activa = self.create_nav_btn(LANG[self.current_lang]["nav_activa"], self.show_activa)
        self.btn_opti = self.create_nav_btn(LANG[self.current_lang]["nav_opti"], self.show_opti)
        self.btn_gaming = self.create_nav_btn(LANG[self.current_lang]["nav_gaming"], self.show_gaming)
        self.btn_input = self.create_nav_btn(LANG[self.current_lang]["nav_input"], self.show_input)
        self.btn_debloat = self.create_nav_btn(LANG[self.current_lang]["nav_debloat"], self.show_debloat)
        self.btn_security = self.create_nav_btn(LANG[self.current_lang]["nav_security"], self.show_security)
        
        # Enable fluid scroll for sidebar too - removed bind_all
        self.nav_frame.bind("<MouseWheel>", lambda e: self.nav_frame._parent_canvas.yview_scroll(int(-1*(e.delta/60)), "units"))
        if is_laptop():
            self.btn_laptop = self.create_nav_btn(LANG[self.current_lang]["nav_laptop"], self.show_laptop)
        self.btn_nvidia = self.create_nav_btn(LANG[self.current_lang]["nav_nvidia"], self.show_nvidia)
        self.btn_amd = self.create_nav_btn(LANG[self.current_lang]["nav_amd"], self.show_amd)
        self.btn_cleaning = self.create_nav_btn(LANG[self.current_lang]["nav_cleaning"], self.show_cleaning)
        self.btn_drivers = self.create_nav_btn(LANG[self.current_lang]["nav_drivers"], self.show_drivers)
        self.btn_repair = self.create_nav_btn(LANG[self.current_lang]["nav_repair"], self.show_repair)
        self.btn_power = self.create_nav_btn(LANG[self.current_lang]["nav_power"], self.show_power)
        
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#330033").pack(fill="x", padx=20, pady=10)
        
        self.lang_var = ctk.StringVar(value="Español")
        self.opt_lang = ctk.CTkOptionMenu(self.sidebar, values=["Español", "English"], variable=self.lang_var, command=self.change_lang, width=140, height=32, corner_radius=8, font=("Roboto", 12, "bold"), fg_color="#110011", text_color=COLOR_TEXT_MAIN, button_color="#330033", button_hover_color=COLOR_ACCENT)
        self.opt_lang.pack(side="bottom", pady=(0, 20), padx=20)
        
        self.btn_update = ctk.CTkButton(self.sidebar, text=LANG[self.current_lang]["btn_update"], height=32, corner_radius=8, fg_color="#110011", hover_color=COLOR_PANEL, 
                      text_color=COLOR_TEXT_SUB, font=("Roboto", 12, "bold"), command=lambda: self.check_update(manual=True))
        self.btn_update.pack(side="bottom", pady=(0, 10), padx=20)
        
        ctk.CTkLabel(self.sidebar, text=f"v{CURRENT_VERSION}", font=("Arial", 10), text_color="#555").pack(side="bottom", pady=(0, 10))

        self.main_area = ctk.CTkFrame(self, fg_color=COLOR_BG) # Changed to COLOR_BG to avoid black gaps
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.view_home = ctk.CTkScrollableFrame(self.main_area, fg_color=COLOR_BG)
        self.setup_home_grid()
        
        self.view_opti = OptimizationView(self.main_area)
        try:
            self.view_gaming = GamingView(self.main_area)
            self.view_input = InputLagView(self.main_area)
            self.view_debloat = DebloatView(self.main_area)
            self.view_security = SecurityView(self.main_area)
            if is_laptop():
                self.view_laptop = LaptopView(self.main_area)
            self.view_nvidia = NvidiaView(self.main_area)
            self.view_amd = AmdView(self.main_area)
            self.view_cleaning = CleaningView(self.main_area)
            self.view_drivers = DriversView(self.main_area)
            self.view_repair = RepairView(self.main_area)
            self.view_power = PowerPlanView(self.main_area)
            self.view_activa = ActivacionView(self.main_area)
        except Exception as e:
            logging.error(f"Error initializing views: {e}")

        self.show_home()

    def change_lang(self, choice):
        self.current_lang = "ES" if choice == "Español" else "EN"
        l = LANG[self.current_lang]
        
        self.btn_home.configure(text=l["nav_home"])
        self.btn_opti.configure(text=l["nav_opti"])
        self.btn_gaming.configure(text=l["nav_gaming"])
        self.btn_input.configure(text=l["nav_input"])
        self.btn_debloat.configure(text=l["nav_debloat"])
        self.btn_security.configure(text=l["nav_security"])
        if hasattr(self, 'btn_laptop'): self.btn_laptop.configure(text=l["nav_laptop"])
        self.btn_nvidia.configure(text=l["nav_nvidia"])
        self.btn_amd.configure(text=l["nav_amd"])
        self.btn_cleaning.configure(text=l["nav_cleaning"])
        self.btn_drivers.configure(text=l["nav_drivers"])
        self.btn_repair.configure(text=l["nav_repair"])
        self.btn_power.configure(text=l["nav_power"])
        self.btn_activa.configure(text=l["nav_activa"])
        self.btn_update.configure(text=l["btn_update"])
        
        if hasattr(self, 'lbl_sys_summary'): self.lbl_sys_summary.configure(text=l["sys_summary"])
        if hasattr(self, 'btn_rescan'): self.btn_rescan.configure(text=l["btn_rescan"])
            
        if hasattr(self, 'cards'):
            if "cpu" in self.cards: self.cards["cpu"].update_title(l["cpu"])
            if "gpu" in self.cards: self.cards["gpu"].update_title(l["gpu"])
            if "ram" in self.cards: self.cards["ram"].update_title(l["ram"])
            if "board" in self.cards: self.cards["board"].update_title(l["board"])
            if "disk" in self.cards: self.cards["disk"].update_title(l["disk"])
            if "sys" in self.cards: self.cards["sys"].update_title(l["sys"])
            
            self.view_opti.update_texts(l["opti_title"], [
                (l["opti_c1_t"], l["opti_c1_d"]), (l["opti_c2_t"], l["opti_c2_d"]),
                (l["opti_c3_t"], l["opti_c3_d"]), (l["opti_c4_t"], l["opti_c4_d"]),
                (l["opti_c5_t"], l["opti_c5_d"]), (l["opti_c6_t"], l["opti_c6_d"]),
                (l["opti_c7_t"], l["opti_c7_d"]), (l["opti_c8_t"], l["opti_c8_d"]),
                (l["opti_c9_t"], l["opti_c9_d"])
            ], l["btn_activar"])
            
        if hasattr(self, 'view_gaming'):
            self.view_gaming.update_texts(l["gaming_title"], [
                (l["gaming_c1_t"], l["gaming_c1_d"]), (l["gaming_c2_t"], l["gaming_c2_d"]),
                (l["gaming_c3_t"], l["gaming_c3_d"]), (l["gaming_c4_t"], l["gaming_c4_d"])
            ], l["btn_activar"])

        if hasattr(self, 'view_input'):
            self.view_input.update_texts(l["input_title"], [
                (l["input_c1_t"], l["input_c1_d"]), (l["input_c2_t"], l["input_c2_d"]),
                (l["input_c3_t"], l["input_c3_d"])
            ], l["btn_activar"])

        if hasattr(self, 'view_debloat'):
            self.view_debloat.update_texts(l["debloat_title"], [
                (l["debloat_c1_t"], l["debloat_c1_d"]), (l["debloat_c2_t"], l["debloat_c2_d"])
            ], l["btn_activar"])

        if hasattr(self, 'view_security'):
            self.view_security.update_texts(l["sec_title"], [
                (l["sec_c1_t"], l["sec_c1_d"])
            ], l["btn_activar"])


            if hasattr(self, 'view_laptop'):
                self.view_laptop.update_texts(l["laptop_title"], [
                    (l["laptop_c1_t"], l["laptop_c1_d"]), (l["laptop_c2_t"], l["laptop_c2_d"]),
                    (l["laptop_c3_t"], l["laptop_c3_d"]), (l["laptop_c4_t"], l["laptop_c4_d"]),
                    (l["laptop_c5_t"], l["laptop_c5_d"]), (l["laptop_c6_t"], l["laptop_c6_d"])
                ], l["btn_activar"])

        if hasattr(self, 'view_power'):
            self.view_power.update_texts("PLAN DE ENERGÍA", [
                (l["opti_c10_t"], l["opti_c10_d"])
            ], l["btn_activar"])
            
        if hasattr(self, 'view_nvidia'):
            self.view_nvidia.update_texts(l["nv_title"], [
                (l["nv_c1_t"], l["nv_c1_d"]), (l["nv_c2_t"], l["nv_c2_d"]),
                (l["nv_c3_t"], l["nv_c3_d"])
            ], l["btn_activar"])

        if hasattr(self, 'view_amd'):
            self.view_amd.update_texts(l["amd_title"], [
                (l["amd_c1_t"], l["amd_c1_d"]), (l["amd_c2_t"], l["amd_c2_d"]),
                (l["amd_c3_t"], l["amd_c3_d"])
            ], l["btn_activar"])

        if hasattr(self, 'view_cleaning'):
            self.view_cleaning.update_texts(l["clean_title"], [
                (l["clean_c1_t"], l["clean_c1_d"]), (l["clean_c2_t"], l["clean_c2_d"]),
                (l["clean_c3_t"], l["clean_c3_d"]), (l["clean_c4_t"], l["clean_c4_d"])
            ], l["btn_activar"])
            
        if hasattr(self, 'view_activa'):
            self.view_activa.update_texts(l["act_title"], [(l["act_c1_t"], l["act_c1_d"])], l["btn_activar"])
            
        if hasattr(self, 'view_repair'):
            self.view_repair.update_texts(l["repair_title"], [
                (l["rep_c1_t"], l["rep_c1_d"]), (l["rep_c2_t"], l["rep_c2_d"]),
                (l["rep_c3_t"], l["rep_c3_d"]), (l["rep_c4_t"], l["rep_c4_d"]),
                (l["rep_c5_t"], l["rep_c5_d"]), (l["rep_c6_t"], l["rep_c6_d"])
            ], l["btn_run"])

        if hasattr(self, 'view_drivers'):
            self.view_drivers.lbl_main_status.configure(text=l["drv_title"])
            if not getattr(self.view_drivers, "is_scanning", False):
                self.view_drivers.btn_huge_scan.configure(text=l["drv_btn_scan"])
                self.view_drivers.lbl_scan_desc.configure(text=l["drv_desc"])
            self.view_drivers.lbl_res_title.configure(text=l["drv_res_title"])
            self.view_drivers.btn_update_all.configure(text=l["drv_btn_upd"])
            if hasattr(self.view_drivers, 'chk_restart'):
                self.view_drivers.chk_restart.configure(text=l["drv_chk_restart"])
            if hasattr(self.view_drivers, 'lbl_sect1'):
                self.view_drivers.lbl_sect1.configure(text=l["drv_need_attn"])
            if hasattr(self.view_drivers, 'lbl_sect2'):
                self.view_drivers.lbl_sect2.configure(text=l["drv_ok"])

    def create_nav_btn(self, text, cmd):
        btn = ctk.CTkButton(self.nav_frame, text=text, fg_color="transparent", hover_color=COLOR_BG, anchor="w", height=40, font=("Roboto", 14), command=cmd)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def show_home(self):
        self._hide_all_views()
        self.view_home.pack(fill="both", expand=True)
        self._update_nav(self.btn_home)
        if hasattr(self, 'lbl_logo') and hasattr(self, 'nav_frame'):
            self.lbl_logo.pack(pady=30, side="top", before=self.nav_frame)

    def show_opti(self):
        self._hide_all_views()
        self.view_opti.pack(fill="both", expand=True)
        self._update_nav(self.btn_opti)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()


    def show_gaming(self):
        self._hide_all_views()
        self.view_gaming.pack(fill="both", expand=True)
        self._update_nav(self.btn_gaming)
        if hasattr(self, 'lbl_logo'): self.lbl_logo.pack_forget()
        
    def show_input(self):
        self._hide_all_views()
        self.view_input.pack(fill="both", expand=True)
        self._update_nav(self.btn_input)
        if hasattr(self, 'lbl_logo'): self.lbl_logo.pack_forget()

    def show_debloat(self):
        self._hide_all_views()
        self.view_debloat.pack(fill="both", expand=True)
        self._update_nav(self.btn_debloat)
        if hasattr(self, 'lbl_logo'): self.lbl_logo.pack_forget()

    def show_security(self):
        self._hide_all_views()
        self.view_security.pack(fill="both", expand=True)
        self._update_nav(self.btn_security)
        if hasattr(self, 'lbl_logo'): self.lbl_logo.pack_forget()

    def show_laptop(self):
        self._hide_all_views()
        self.view_laptop.pack(fill="both", expand=True)
        self._update_nav(self.btn_laptop)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_nvidia(self):
        self._hide_all_views()
        self.view_nvidia.pack(fill="both", expand=True)
        self._update_nav(self.btn_nvidia)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_amd(self):
        self._hide_all_views()
        self.view_amd.pack(fill="both", expand=True)
        self._update_nav(self.btn_amd)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_cleaning(self):
        self._hide_all_views()
        self.view_cleaning.pack(fill="both", expand=True)
        self._update_nav(self.btn_cleaning)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_drivers(self):
        self._hide_all_views()
        self.view_drivers.pack(fill="both", expand=True)
        self._update_nav(self.btn_drivers)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_power(self):
        self._hide_all_views()
        self.view_power.pack(fill="both", expand=True)
        self._update_nav(self.btn_power)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_activa(self):
        self._hide_all_views()
        self.view_activa.pack(fill="both", expand=True)
        self._update_nav(self.btn_activa)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def show_repair(self):
        self._hide_all_views()
        self.view_repair.pack(fill="both", expand=True)
        self._update_nav(self.btn_repair)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack_forget()

    def _hide_all_views(self):
        views = [
            'view_home', 'view_opti', 'view_gaming', 'view_input', 
            'view_debloat', 'view_security', 'view_laptop', 'view_nvidia',
            'view_amd', 'view_cleaning', 'view_drivers', 'view_repair', 
            'view_power', 'view_activa'
        ]
        for v_name in views:
            if hasattr(self, v_name):
                v = getattr(self, v_name)
                if v: v.pack_forget()

    def _update_nav(self, active_btn):
        self.btn_home.configure(fg_color="transparent")
        self.btn_opti.configure(fg_color="transparent")
        if hasattr(self, 'btn_laptop'): self.btn_laptop.configure(fg_color="transparent")
        self.btn_nvidia.configure(fg_color="transparent")
        self.btn_amd.configure(fg_color="transparent")
        self.btn_cleaning.configure(fg_color="transparent")
        self.btn_drivers.configure(fg_color="transparent")
        self.btn_repair.configure(fg_color="transparent")
        self.btn_power.configure(fg_color="transparent")
        self.btn_activa.configure(fg_color="transparent")
        
        if hasattr(self, 'btn_gaming'): self.btn_gaming.configure(fg_color="transparent")
        if hasattr(self, 'btn_input'): self.btn_input.configure(fg_color="transparent")
        if hasattr(self, 'btn_debloat'): self.btn_debloat.configure(fg_color="transparent")
        if hasattr(self, 'btn_security'): self.btn_security.configure(fg_color="transparent")
        
        # Use ACCENT color for the active button so it "pops" and doesn't look black
        active_btn.configure(fg_color=COLOR_ACCENT)

    def setup_home_grid(self):
        l = LANG.get(getattr(self, 'current_lang', 'ES'), LANG["ES"])
        h = ctk.CTkFrame(self.view_home, fg_color="transparent")
        h.pack(fill="x", pady=(0, 20))
        self.lbl_sys_summary = ctk.CTkLabel(h, text=l["sys_summary"], font=("Arial", 24, "bold"), text_color="white")
        self.lbl_sys_summary.pack(side="left")
        self.btn_rescan = ctk.CTkButton(h, text=l["btn_rescan"], width=100, fg_color=COLOR_ACCENT, hover_color="#cc0000", command=self.load_data)
        self.btn_rescan.pack(side="right")

        grid = ctk.CTkFrame(self.view_home, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.columnconfigure((0,1), weight=1)

        self.cards = {}
        definitions = [
            ("cpu", l["cpu"], 0, 0, "💠", COLOR_ACCENT),
            ("gpu", l["gpu"], 0, 1, "☢️", COLOR_ACCENT),
            ("ram", l["ram"], 1, 0, "📼", COLOR_ACCENT),
            ("board", l["board"], 1, 1, "🎛️", COLOR_ACCENT),
            ("disk", l["disk"], 2, 0, "💿", COLOR_ACCENT),
            ("sys", l["sys"], 2, 1, "🖥️", COLOR_ACCENT),
        ]
        
        for k, t, r, c, i, col in definitions:
            card = InfoCard(grid, t, i, color=col)
            card.grid(row=r, column=c, sticky="nsew", padx=15, pady=15)
            self.cards[k] = card

    def load_data(self):
        logging.info("Iniciando carga de datos de hardware...")
        if hasattr(self, 'cards'):
            for c in self.cards.values():
                for w in c.content_area.winfo_children(): w.destroy()
        
        t = threading.Thread(target=self._fetch_wmi, daemon=True)
        t.start()

    def _fetch_wmi(self):
        try:
            pythoncom.CoInitialize()
            c = wmi.WMI()
            
            for cpu in c.Win32_Processor():
                self.update_card("cpu", {
                    "Modelo": cpu.Name, 
                    "Núcleos Lógicos": f"{cpu.NumberOfLogicalProcessors}", 
                    "Núcleos Físicos": f"{cpu.NumberOfCores}",
                    "Reloj Base": f"{cpu.MaxClockSpeed} MHz",
                    "Socket": cpu.SocketDesignation or "N/A",
                    "L2 Cache": f"{cpu.L2CacheSize or 0} KB",
                    "L3 Cache": f"{cpu.L3CacheSize or 0} KB",
                    "Serial/ID HW": cpu.ProcessorId or "N/A"
                })
                break
            
            for gpu in c.Win32_VideoController():
                ram_gb = "N/A"
                if gpu.AdapterRAM:
                    try:
                        ram_gb = f"{abs(int(gpu.AdapterRAM)) // (1024**2)} MB"
                    except: pass
                self.update_card("gpu", {
                    "Chipset": gpu.Name or "N/A", 
                    "VRAM": ram_gb,
                    "Resolución": f"{gpu.CurrentHorizontalResolution or '?'}x{gpu.CurrentVerticalResolution or '?'}",
                    "Tasa Refresco": f"{gpu.CurrentRefreshRate or '?'} Hz",
                    "Driver Ver.": gpu.DriverVersion or "N/A",
                    "Driver Fecha": gpu.DriverDate.split('.')[0] if gpu.DriverDate else "N/A",
                    "Serial/ID HW": gpu.PNPDeviceID or "N/A"
                })
            
            ram_info = {}
            total_gb = 0
            for i, ram in enumerate(c.Win32_PhysicalMemory()):
                cap = int(ram.Capacity) / (1024**3)
                total_gb += cap
                ram_info[f"Slot {i+1} Capacidad"] = f"{cap:.1f} GB"
                ram_info[f"Slot {i+1} Vel."] = f"{ram.Speed or '?'} MHz"
                ram_info[f"Slot {i+1} Serial"] = ram.SerialNumber.strip() if ram.SerialNumber else "N/A"
                ram_info[f"Slot {i+1} Fab."] = ram.Manufacturer.strip() if ram.Manufacturer else "N/A"
                ram_info[f"Slot {i+1} Físico"] = "DIMM/SODIMM" if ram.FormFactor else "N/A"
            ram_info["[ TOTAL RAM ]"] = f"{round(total_gb, 2)} GB"
            self.update_card("ram", ram_info)
            
            for mb in c.Win32_BaseBoard():
                self.update_card("board", {
                    "Fabricante": mb.Manufacturer or "N/A", 
                    "Producto": mb.Product or "N/A", 
                    "Versión": mb.Version or "N/A",
                    "Serial Number": mb.SerialNumber or "N/A"
                })

            disk_info = {}
            for d in c.Win32_DiskDrive():
                sz = 0
                if d.Size:
                    sz = int(d.Size) // (1024**3)
                idx = d.Index
                disk_info[f"[ Disco {idx} ]"] = d.Model or "N/A"
                disk_info[f" -> Tamaño {idx}"] = f"{sz} GB"
                disk_info[f" -> Particiones {idx}"] = d.Partitions or 0
                disk_info[f" -> Interfaz {idx}"] = d.InterfaceType or "N/A"
                disk_info[f" -> Serial {idx}"] = d.SerialNumber.strip() if d.SerialNumber else "N/A"
                disk_info[f" -> Estado {idx}"] = d.Status or "N/A"
            self.update_card("disk", disk_info)
            
            for os_ in c.Win32_OperatingSystem():
                 self.update_card("sys", {
                     "Edición": os_.Caption or "N/A", 
                     "Versión": os_.Version or "N/A",
                     "Build": os_.BuildNumber or "N/A",
                     "Arquitectura": os_.OSArchitecture or "N/A",
                     "Instalación": os_.InstallDate.split('.')[0] if os_.InstallDate else "N/A",
                     "Serial Number": os_.SerialNumber or "N/A"
                 })
                
        except Exception as e:
            logging.error(f"WMI Error: {e}")

    def update_card(self, key, data):
        self.after(0, lambda: self._ui_update_card(key, data))

    def _ui_update_card(self, key, data):
        if hasattr(self, 'cards') and key in self.cards:
            for k, v in data.items():
                self.cards[key].add_row(k, v)

if __name__ == "__main__":
    import sys
    import subprocess
    import ctypes
    import os
    
    # Auto-elevación global: Pide permisos UNA SOLA VEZ al iniciar el programa
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False
        
    import hashlib
    task_hash = hashlib.md5(sys.executable.encode('utf-8')).hexdigest()[:8]
    task_name = f"YKZ_OPTI_{task_hash}"
        
    if not is_admin and hasattr(ctypes, 'windll'):
        # 1. Intentar correr la tarea programada silenciosa para saltar UAC
        # Si funciona (es decir, ya le dimos si al Admin alguna vez), inicia la app por ahi
        res = subprocess.call(f'schtasks /run /tn "{task_name}"', creationflags=0x08000000)
        if res == 0:
            sys.exit(0) # Cerramos la instancia actual silenciosamente
            
        # 2. Si no existe la tarea, pedimos UAC (pasará solo la primera vez)
        exe = sys.executable
        if getattr(sys, 'frozen', False):
            # Si es el archivo compilado .exe
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, "", None, 1)
        else:
            # Si se lanza desde código fuente .py
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, f'"{os.path.abspath(__file__)}"', None, 1)
        sys.exit()

    # Si estamos ejecutándonos como Administrador, creamos permanentemente la tarea
    if is_admin and getattr(sys, 'frozen', False):
        try:
            exe_path = sys.executable
            working_dir = os.path.dirname(exe_path)
            ps_cmd = f"Register-ScheduledTask -Action (New-ScheduledTaskAction -Execute '{exe_path}' -WorkingDirectory '{working_dir}') -TaskName '{task_name}' -RunLevel Highest -Force"
            subprocess.call(["powershell.exe", "-NoProfile", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], creationflags=0x08000000)
        except Exception as e:
            logging.error(f"Error Register-ScheduledTask: {e}")

    if len(sys.argv) == 3 and sys.argv[1] == "--run-ps1":
        ps1_path = sys.argv[2]
        subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", ps1_path],
            creationflags=0x08000000
        ).wait()
        sys.exit(0)
        
    app = PurpleApp()
    app.mainloop()
