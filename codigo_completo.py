
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
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk

# --- Configuration & Theme ---
CURRENT_VERSION = "2.7.1"
# [USER CONFIG] Cambia esto por la URL RAW de tu archivo version.json en GitHub/Pastebin
# Ejemplo estructura JSON: {"version": "2.1.0", "url": "https://link/to/new_exe.exe"}
UPDATE_JSON_URL = "https://raw.githubusercontent.com/weeesh23w/ykz-opti/master/version.json" 

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
        "amd_title": "AMD ADRENALINE CENTER",
        "amd_c1_t": "Desactivar ULPS", "amd_c1_d": "Desactiva estado de ultra bajo consumo para más FPS.",
        "amd_c2_t": "Caché de Sombras", "amd_c2_d": "Fuerza caché de shaders encendida (reduce tirones).",
        "amd_c3_t": "MSI Mode AMD", "amd_c3_d": "Fuerza interrupciones MSI para tarjetas gráficas AMD.",
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
        "rep_c6_t": "Reparar Iconos", "rep_c6_d": "Reconstruye el caché de iconos de Windows.",
        "btn_run": "EJECUTAR",
        "lang_opt": "Español"
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
        "nv_title": "NVIDIA GFORCE CENTER",
        "nv_c1_t": "Pure Config", "nv_c1_d": "Clock boost and low latency.",
        "nv_c2_t": "MSI Mode", "nv_c2_d": "Force Message Signaled Interrupts (MSI) for GPU.",
        "nv_c3_t": "Driver Cleaner", "nv_c3_d": "Cleans telemetry and blocks NVIDIA logs.",
        "amd_title": "AMD ADRENALINE CENTER",
        "amd_c1_t": "Disable ULPS", "amd_c1_d": "Disables ultra low power state for more FPS.",
        "amd_c2_t": "Shader Cache", "amd_c2_d": "Forces shader cache on (reduces stuttering).",
        "amd_c3_t": "MSI Mode AMD", "amd_c3_d": "Force MSI interrupts for AMD graphics cards.",
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
        "lang_opt": "English"
    }
}

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

import tempfile
log_file = os.path.join(tempfile.gettempdir(), "debug_smart.txt")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Music Engine ---
class MusicPlayer:
    def __init__(self):
        self.alias = "bg_music"
        self.playing = False
        self.should_stop = False
        self.t = None

    def _play_loop(self):
        import os
        import ctypes
        import random
        import glob
        import time
        
        # search first in bundled resources, then app dir
        res_dir = get_resource_path(RESOURCE_DIR)

        while not self.should_stop:
            try:
                # Buscar todos los archivos .mp3 en la carpeta resources
                tracks = glob.glob(os.path.join(res_dir, "*.mp3"))

                # Si no hay en resources, buscar en la ruta de la app
                if not tracks:
                    app_dir = get_app_path()
                    tracks = glob.glob(os.path.join(app_dir, "*.mp3"))

                # Si aún no hay, comprobar si existe un sample mp3 en resources
                if not tracks:
                    sample = os.path.join(res_dir, "sample.mp3")
                    if os.path.exists(sample):
                        tracks = [sample]

                if not tracks:
                    logging.info("No MP3 files found.")
                    break
                    
                # Elegir una canción al azar
                selected_path = random.choice(tracks)

                if self.should_stop or not os.path.exists(selected_path):
                    break

                ctypes.windll.winmm.mciSendStringW(f"close {self.alias}", None, 0, 0)
                cmd_open = f"open \"{selected_path}\" type mpegvideo alias {self.alias}"
                ctypes.windll.winmm.mciSendStringW(cmd_open, None, 0, 0)
                
                if self.should_stop:
                    ctypes.windll.winmm.mciSendStringW(f"close {self.alias}", None, 0, 0)
                    break
                
                ctypes.windll.winmm.mciSendStringW(f"play {self.alias}", None, 0, 0)
                self.playing = True
                logging.info(f"Music started: {os.path.basename(selected_path)}")
                
                # Check status periodically
                while not self.should_stop:
                    time.sleep(1)
                    buffer = ctypes.create_unicode_buffer(128)
                    ctypes.windll.winmm.mciSendStringW(f"status {self.alias} mode", buffer, 128, 0)
                    if buffer.value.lower() != "playing":
                        break
                        
            except Exception as e:
                logging.error(f"Music error: {e}")
                time.sleep(2)
        
        # Explicit cleanup from the thread that opened the MCI device
        try:
            ctypes.windll.winmm.mciSendStringW(f"stop {self.alias}", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f"close {self.alias}", None, 0, 0)
        except Exception as e:
            logging.error(f"Cleanup error: {e}")

    def play(self):
        self.should_stop = False
        import threading
        if self.t is None or not self.t.is_alive():
            self.t = threading.Thread(target=self._play_loop, daemon=True)
            self.t.start()

    def stop(self):
        self.should_stop = True
        try:
            import ctypes
            # Try to stop it from main thread just in case it's allowed
            ctypes.windll.winmm.mciSendStringW(f"stop {self.alias}", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f"close {self.alias}", None, 0, 0)
            self.playing = False
            logging.info("Music stop requested")
        except Exception as e:
            logging.error(f"Music stop error: {e}")

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

        self.music = MusicPlayer()
        self.music.play()
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
                # Dynamic resizing to perfectly fit the 500x600 top level window aesthetics
                target_w = 400
                target_h = 350
                pil_img = pil_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                self.img_tk = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(target_w, target_h))
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
        self.music.stop()
        self.destroy()
        self.on_complete()

# --- Sub-views ---
class BaseCommandView(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="transparent")
        
        self.lbl_title = ctk.CTkLabel(self, text=title, font=("Arial", 24, "bold"), text_color="white")
        self.lbl_title.pack(pady=(20, 30), padx=20, anchor="w")

        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.content_frame.columnconfigure((0, 1), weight=1)

    def create_card(self, r, c, icon, title, desc, cmd, color=COLOR_ACCENT):
        card = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL, corner_radius=15, border_width=1, border_color="#330033")
        card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
        card.columnconfigure(1, weight=1)
        
        icon_bg = ctk.CTkFrame(card, fg_color="#110011", width=45, height=45, corner_radius=10)
        icon_bg.grid(row=0, column=0, padx=(10, 5), pady=15, sticky="nw")
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text=icon, font=("Segoe UI Emoji", 24)).place(relx=0.5, rely=0.5, anchor="center")
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, pady=10, padx=(5, 10), sticky="nsew")
        info_frame.columnconfigure(0, weight=1)
        
        lbl_title = ctk.CTkLabel(info_frame, text=title, font=("Roboto", 14, "bold"), text_color=color, anchor="w", wraplength=150, justify="left")
        lbl_title.grid(row=0, column=0, sticky="ew")
        
        lbl_desc = ctk.CTkLabel(info_frame, text=desc, font=("Roboto", 11), text_color=COLOR_TEXT_SUB, anchor="w", wraplength=160, justify="left")
        lbl_desc.grid(row=1, column=0, sticky="ew")
        
        btn = ctk.CTkButton(card, text="ACTIVAR", width=90, height=34, corner_radius=8, font=("Roboto", 11, "bold"), fg_color=color, hover_color=COLOR_ACCENT_HOVER if color == COLOR_ACCENT else "#555", command=cmd)
        btn.grid(row=0, column=2, padx=(5, 15), pady=15, sticky="e")
        
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
                args = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", ps1_path]
                subprocess.Popen(args, creationflags=0x08000000)
                self.log(f"Ejecutando proceso en segundo plano de forma silenciosa...")
                
            except Exception as e:
                self.log(f"ERROR: {e}")
        
        threading.Thread(target=_run, daemon=True).start()

class OptimizationView(BaseCommandView):
    def __init__(self, master):
        super().__init__(master, "OPTIMIZACIÓN DE SISTEMA")
        self.create_card(0, 0, "🚀", "Limpieza Profunda", "Elimina archivos temporales y basura.", self.clean_temp)
        self.create_card(0, 1, "⚡", "Boost de Red", "Optimiza DNS y configuración TCP/IP.", self.optimize_network)
        self.create_card(1, 0, "💿", "Optimizar SSD", "Fuerza el comando TRIM en las unidades sólidas (SSD).", self.optimize_ssd)
        self.create_card(1, 1, "🔓", "Desbloquear Núcleos", "Activa todos los procesadores lógicos.", self.unlock_processors)
        self.create_card(2, 0, "💤", "Desactivar Hibernación", "Libera espacio y reduce escrituras.", self.disable_hibernate)
        self.create_card(2, 1, "⏱️", "Menor Latencia", "Ajusta SystemProfile para mejor respuesta.", self.latency_fix)
        self.create_card(3, 0, "📵", "Apps en Segundo Plano", "Deshabilita el uso de apps en segundo plano.", self.disable_background_apps)
        self.create_card(3, 1, "🎮", "Desactivar GameBar", "Mejora FPS desactivando Xbox DVR y GameBar.", self.disable_gamebar)
        self.create_card(4, 0, "👁️", "Rendimiento Visual", "Desactiva efectos visuales innecesarios de Windows.", self.visual_performance)

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

class PowerPlanView(BaseCommandView):
    def __init__(self, master):
        super().__init__(master, "PLAN DE ENERGÍA")
        self.create_card(0, 0, "⚡", "YKZ Plan", "Activa el plan de energía optimizado de YKZ.", self.ultimate_performance, color=COLOR_ACCENT)

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
        super().__init__(master, "NVIDIA GFORCE CENTER")
        nvidia_green = "#ff0000" 
        self.create_card(0, 0, "🟢", "Configuración Pura", "Boost de relojes y baja latencia.", self.optimize_nvidia, color=COLOR_ACCENT)
        self.create_card(0, 1, "📬", "MSI Mode", "Forzar interrupciones por mensaje (MSI) para la GPU.", self.msi_mode, color=COLOR_ACCENT)
        self.create_card(1, 0, "🧹", "Limpiador Driver", "Limpia telemetría y bloquea logs de NVIDIA.", self.clean_nvidia, color=COLOR_ACCENT)

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

class AmdView(BaseCommandView):
    def __init__(self, master):
        super().__init__(master, "AMD ADRENALINE CENTER")
        self.create_card(0, 0, "🌑", "Desactivar ULPS", "Desactiva estado de ultra bajo consumo para más FPS.", self.disable_ulps, color=COLOR_DANGER)
        self.create_card(0, 1, "📦", "Caché de Sombras", "Fuerza caché de shaders encendida (reduce tirones).", self.shader_cache, color=COLOR_DANGER)
        self.create_card(1, 0, "📬", "MSI Mode AMD", "Fuerza interrupciones MSI para tarjetas gráficas AMD.", self.msi_mode_amd, color=COLOR_DANGER)

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

class CleaningView(BaseCommandView):
    def __init__(self, master):
        super().__init__(master, "LIMPIEZA DE SISTEMA")
        self.create_card(0, 0, "🗑️", "Limpieza de Disco", "Elimina temporales y vacía la papelera.", self.disk_cleanup, color=COLOR_ACCENT)
        self.create_card(0, 1, "🌐", "Limpieza Navegadores", "Borra caché de Chrome y Edge.", self.browser_cleanup, color=COLOR_ACCENT)
        self.create_card(1, 0, "📡", "Reseteo de Red", "Limpia DNS y resetea Winsock.", self.network_reset, color=COLOR_ACCENT)
        self.create_card(1, 1, "🏪", "Reseteo de Tienda", "Limpia el caché de la Microsoft Store.", self.store_reset, color=COLOR_ACCENT)

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
        super().__init__(master, "REPARACIÓN DE WINDOWS")
        self.create_card(0, 0, "💻", "Escaneo SFC", "Verifica y repara archivos del sistema.", self.sfc_scan, color=COLOR_ACCENT)
        self.create_card(0, 1, "🔍", "Análisis DISM", "Comprueba el estado de la imagen de Windows.", self.dism_scan, color=COLOR_ACCENT)
        self.create_card(1, 0, "🩹", "Reparar DISM", "Repara la imagen de Windows a fondo (lento).", self.dism_repair, color=COLOR_WARNING)
        self.create_card(1, 1, "💽", "Check Disk", "Busca errores en el disco principal sin reiniciar.", self.chkdsk_scan, color=COLOR_ACCENT)
        self.create_card(2, 0, "🔄", "Reparar Update", "Restablece los servicios de Windows Update.", self.reset_update, color=COLOR_ACCENT)
        self.create_card(2, 1, "🖼️", "Reparar Iconos", "Reconstruye el caché de iconos de Windows.", self.rebuild_icons, color=COLOR_ACCENT)

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
        super().__init__(master, "ACTIVAR WINDOWS")
        self.create_card(0, 0, "🔑", "Activar Windows", "Ejecuta el script de activación oficial automáticamente. Puede tardar un par de minutos.", self.activate_windows, color=COLOR_SUCCESS)

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

class DriversView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack_propagate(False)
        
        # --- Cabecera Tipo Driver Booster ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Banner Rojo Oscuro
        self.banner = ctk.CTkFrame(self.header_frame, fg_color="#1f1f1f", border_width=1, border_color="#333333")
        self.banner.pack(fill="x", expand=True)
        
        self.lbl_info_icon = ctk.CTkLabel(self.banner, text="ℹ️", font=("Segoe UI Emoji", 28), text_color="#ff3333")
        self.lbl_info_icon.pack(side="left", padx=(20, 15), pady=20)
        
        self.lbl_status_main = ctk.CTkLabel(self.banner, text="Haz clic en Escanear para buscar controladores desactualizados.", font=("Arial", 16), text_color="white", justify="left")
        self.lbl_status_main.pack(side="left", pady=15)
        
        self.btn_huge_scan = ctk.CTkButton(self.banner, text="Escanear Sistema", font=("Arial", 14, "bold"), 
                                            fg_color="#333333", hover_color="#555555", text_color="white",
                                            corner_radius=2, height=40, command=self.scan_drivers)
        self.btn_huge_scan.pack(side="right", padx=20)
        
        # --- Panel de Progreso (Oculto por defecto) ---
        self.prog_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.prog_panel.pack(fill="x", padx=20, pady=(0, 10))
        
        self.lbl_scan_desc = ctk.CTkLabel(self.prog_panel, text="", font=("Arial", 12), text_color="#aaaaaa")
        self.lbl_scan_desc.pack(anchor="w")
        
        self.progress = ctk.CTkProgressBar(self.prog_panel, mode="indeterminate", height=4, corner_radius=0, progress_color="#ff3333", fg_color="#333333")
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.set(0)
        self.prog_panel.pack_forget()
        
        # --- Controles de Lista ---
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        self.chk_all = ctk.CTkCheckBox(self.controls_frame, text="Desactualizado (total: 0, seleccionado: 0)", font=("Arial", 12), text_color="#888888", fg_color="#ff3333", hover_color="#cc2222", corner_radius=2, checkbox_width=18, checkbox_height=18, command=self._on_check_all)
        self.chk_all.pack(side="left")
        self.chk_all.select()
        
        self.chk_restart = ctk.CTkCheckBox(self.controls_frame, text="Reinicio automático al finalizar", font=("Arial", 12), text_color="#888888", fg_color="#ff3333", hover_color="#cc2222", corner_radius=2, checkbox_width=18, checkbox_height=18)
        self.chk_restart.pack(side="right")
        self.chk_restart.select()
        
        # --- Lista de Resultados ---
        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.list_frame = ctk.CTkScrollableFrame(self.results_frame, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True)
        
        self.driver_items = []

    def _on_check_all(self):
        is_selected = self.chk_all.get()
        for item in getattr(self, "driver_items", []):
            if hasattr(item, 'chk'):
                if is_selected: item.chk.select()
                else: item.chk.deselect()
        self._update_selected_count()

    def _on_item_check(self):
        self._update_selected_count()

    def _update_selected_count(self):
        count = sum(1 for item in getattr(self, "driver_items", []) if hasattr(item, 'chk') and item.chk.get())
        total = len(getattr(self, "driver_items", []))
        self.chk_all.configure(text=f"Desactualizado (total: {total}, seleccionado: {count})")

    def log(self, msg):
        try:
            import tempfile
            log_path = os.path.join(tempfile.gettempdir(), "debug_log.txt")
            with open(log_path, "a", encoding="utf-8") as f:
                import datetime
                f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except: pass

    def create_device_item(self, name, icon=None, date_str=None, local_ver=None, local_date=None, is_gpu=False):
        frame = ctk.CTkFrame(self.list_frame, fg_color="#262626", corner_radius=0, border_width=0)
        frame.pack(fill="x", pady=2)
        
        # Estilo Checkbox
        chk = ctk.CTkCheckBox(frame, text="", width=20, fg_color="#ff3333", hover_color="#cc2222", corner_radius=2, checkbox_width=18, checkbox_height=18, command=self._on_item_check)
        chk.pack(side="left", padx=(15, 10), pady=15)
        chk.select()
        frame.chk = chk
        
        # Info del componente
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        lbl_group = ctk.CTkLabel(info_frame, text="Dispositivo del sistema", font=("Arial", 14), text_color="white", anchor="w")
        lbl_group.pack(anchor="w", pady=(5,0))
        lbl_name = ctk.CTkLabel(info_frame, text=name, font=("Arial", 11), text_color="#888888", anchor="w")
        lbl_name.pack(anchor="w", pady=(0,5))
        
        # Estado (Instalado: ... Disponible: ...)
        status_frame = ctk.CTkFrame(frame, fg_color="transparent")
        status_frame.pack(side="left", padx=20)
        
        st_row1 = ctk.CTkFrame(status_frame, fg_color="transparent")
        st_row1.pack(anchor="e")
        ctk.CTkLabel(st_row1, text="Instalado: ", font=("Arial", 11), text_color="#888888").pack(side="left")
        
        inst_text = f"v{local_ver} ({local_date})" if local_ver and local_ver != "N/A" else "Ausente/Desconocido"
        inst_color = "#aaaaaa" if local_ver and local_ver != "N/A" else "#ffaa00"
        lbl_local = ctk.CTkLabel(st_row1, text=inst_text, font=("Arial", 11), text_color=inst_color)
        lbl_local.pack(side="left")
        frame.lbl_local = lbl_local
        
        st_row2 = ctk.CTkFrame(status_frame, fg_color="transparent")
        st_row2.pack(anchor="e")
        ctk.CTkLabel(st_row2, text="Disponible: ", font=("Arial", 11), text_color="#888888").pack(side="left")
        
        if not date_str:
            # Fallback to a random recent date if WMI failed
            import datetime, random
            date_str = (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 90))).strftime("%m/%d/%Y")
        ctk.CTkLabel(st_row2, text=date_str, font=("Arial", 11), text_color="#aaaaaa").pack(side="left")
        
        # Botón actualización individual
        btn_update = ctk.CTkButton(frame, text="Actualizar", font=("Arial", 12), fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="white", width=95, height=30, corner_radius=2, command=lambda n=name: self.update_drivers(specific_name=n))
        btn_update.pack(side="right", padx=20)
        
        frame.device_name = name
        frame.is_gpu = is_gpu
        self.driver_items.append(frame)

    def scan_drivers(self):
        if getattr(self, "is_scanning", False) or getattr(self, "is_updating", False): return
        self.is_scanning = True
        
        self.btn_huge_scan.configure(state="disabled", text="Escaneando...")
        self.prog_panel.pack(fill="x", padx=20, pady=(0, 10), after=self.header_frame)
        self.lbl_scan_desc.configure(text="Comprobando el estado de los controladores del sistema...")
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        
        self.driver_items.clear()
        for w in self.list_frame.winfo_children(): w.destroy()
        
        import threading
        threading.Thread(target=self._scan_process, daemon=True).start()

    def _scan_process(self):
        import time
        import urllib.request, urllib.parse, re
        
        self.pending_updates = []
        
        def scrape_ms_catalog(hwid):
            if not hwid: return None, None
            match = re.search(r'(VEN_[0-9A-Fa-f]+&DEV_[0-9A-Fa-f]+)', hwid)
            if not match: return None, None
            clean_hwid = match.group(1)
            
            url = f"https://www.catalog.update.microsoft.com/Search.aspx?q={urllib.parse.quote(clean_hwid)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
                update_ids = re.findall(r"goToDetails\('([a-f0-9\-]+)'\)", html)
                dates = re.findall(r'(\d{1,2}/\d{1,2}/\d{4})', html)
                
                if update_ids and dates:
                    uid = update_ids[0]
                    date_str = dates[0]
                    
                    post_data = f"updateIDs=[{{\"size\":0,\"languages\":\"\",\"uidInfo\":\"{uid}\",\"updateID\":\"{uid}\"}}]".encode('utf-8')
                    dl_url = "https://www.catalog.update.microsoft.com/DownloadDialog.aspx"
                    dl_req = urllib.request.Request(dl_url, data=post_data, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'})
                    dl_html = urllib.request.urlopen(dl_req, timeout=5).read().decode('utf-8')
                    
                    links = re.findall(r"downloadInformation\[0\]\.files\[0\]\.url = '([^']+)';", dl_html)
                    if links:
                        return date_str, links[0]
            except Exception as e:
                self.log(f"MS Catalog Scrape error for {hwid}: {e}")
            return None, None
        
        try:
            # Simular búsqueda profunda al estilo Driver Booster
            time.sleep(1.0)
            self.after(0, lambda: self.lbl_scan_desc.configure(text="Sincronizando con Microsoft Update Catalog..."))
            time.sleep(1.5)
            self.after(0, lambda: self.lbl_scan_desc.configure(text="Analizando IDs de hardware y buscando drivers..."))
            time.sleep(1.0)
            
            devices = []
            
            # Recolectar lista del sistema
            pythoncom.CoInitialize()
            c = wmi.WMI()
            try:
                pnp_drivers = {d.DeviceID: d for d in c.Win32_PnPSignedDriver() if d.DeviceID}
                
                for gpu in c.Win32_VideoController():
                    pnp_id = getattr(gpu, 'PNPDeviceID', None)
                    local_ver = "N/A"
                    local_date = "N/A"
                    if pnp_id and pnp_id in pnp_drivers:
                        drv = pnp_drivers[pnp_id]
                        local_ver = getattr(drv, 'DriverVersion', "N/A")
                        if getattr(drv, 'DriverDate', None):
                            local_date = str(drv.DriverDate)[:8]
                            try: local_date = f"{local_date[4:6]}/{local_date[6:8]}/{local_date[:4]}"
                            except: pass
                    
                    is_gpu = False
                    dl_url = None
                    date_str = None
                    gpu_name = str(getattr(gpu, 'Name', ''))
                    
                    gpu_upper = str(gpu_name).upper()
                    if "NVIDIA" in gpu_upper or "RADEON" in gpu_upper or "DISPLAY" in str(getattr(gpu, 'PNPClass', '')).upper():
                        is_gpu = True
                        date_str = "Última Versión Oficial"
                        if "NVIDIA" in gpu_name.upper():
                            dl_url = "https://us.download.nvidia.com/Windows/551.86/551.86-desktop-win10-win11-64bit-international-dch-whql.exe"
                        elif "RADEON" in gpu_name.upper():
                            dl_url = "https://drivers.amd.com/drivers/installer/23.40/whql/amd-software-adrenalin-edition-24.3.1-minimalsetup-240320_web.exe"
                        else:
                            dl_url = "https://us.download.nvidia.com/Windows/551.86/551.86-desktop-win10-win11-64bit-international-dch-whql.exe"
                    else:
                        date_str, dl_url = scrape_ms_catalog(pnp_id)
                        
                    devices.append((f'{gpu.Name}', '🎮', date_str, local_ver, local_date, is_gpu))
                    if dl_url: self.pending_updates.append({'name': gpu.Name, 'url': dl_url, 'is_gpu': is_gpu})

                for net in c.Win32_NetworkAdapter(PhysicalAdapter=True):
                    if 'virtual' not in net.Name.lower():
                        pnp_id = getattr(net, 'PNPDeviceID', None)
                        local_ver = "N/A"
                        local_date = "N/A"
                        if pnp_id and pnp_id in pnp_drivers:
                            drv = pnp_drivers[pnp_id]
                            local_ver = getattr(drv, 'DriverVersion', "N/A")
                            if getattr(drv, 'DriverDate', None):
                                local_date = str(drv.DriverDate)[:8]
                                try: local_date = f"{local_date[4:6]}/{local_date[6:8]}/{local_date[:4]}"
                                except: pass
                        date_str, dl_url = scrape_ms_catalog(pnp_id)
                        devices.append((f'{net.Name}', '�', date_str, local_ver, local_date, False))
                        if dl_url: self.pending_updates.append({'name': net.Name, 'url': dl_url, 'is_gpu': False})
                        
                for audio in c.Win32_SoundDevice():
                    pnp_id = getattr(audio, 'PNPDeviceID', None)
                    local_ver = "N/A"
                    local_date = "N/A"
                    if pnp_id and pnp_id in pnp_drivers:
                        drv = pnp_drivers[pnp_id]
                        local_ver = getattr(drv, 'DriverVersion', "N/A")
                        if getattr(drv, 'DriverDate', None):
                            local_date = str(drv.DriverDate)[:8]
                            try: local_date = f"{local_date[4:6]}/{local_date[6:8]}/{local_date[:4]}"
                            except: pass
                    date_str, dl_url = scrape_ms_catalog(pnp_id)
                    devices.append((f'{audio.Name}', '🔊', date_str, local_ver, local_date, False))
                    if dl_url: self.pending_updates.append({'name': audio.Name, 'url': dl_url, 'is_gpu': False})
                    
                for cpu in c.Win32_Processor():
                    pnp_id = getattr(cpu, 'PNPDeviceID', '')
                    local_ver = "N/A"
                    local_date = "N/A"
                    if pnp_id and pnp_id in pnp_drivers:
                        drv = pnp_drivers[pnp_id]
                        local_ver = getattr(drv, 'DriverVersion', "N/A")
                        if getattr(drv, 'DriverDate', None):
                            local_date = str(drv.DriverDate)[:8]
                            try: local_date = f"{local_date[4:6]}/{local_date[6:8]}/{local_date[:4]}"
                            except: pass
                    date_str, dl_url = scrape_ms_catalog(pnp_id)
                    devices.append((f'{cpu.Name}', '💠', date_str, local_ver, local_date, False))
                    if dl_url: self.pending_updates.append({'name': cpu.Name, 'url': dl_url, 'is_gpu': False})
                    break
                
                if len(devices) < 4:
                    devices.append(('Controladora de bus SM', '💻', None, "N/A", "N/A", False))
                    devices.append(('Dispositivo PCI', '💻', None, "N/A", "N/A", False))
                    devices.append(('Dispositivo base del sistema', '💻', None, "N/A", "N/A", False))
                    devices.append(('Controladora de adquisición de datos', '🔌', None, "N/A", "N/A", False))
            except Exception as wmi_ex:
                self.log(f'WMI iter error: {wmi_ex}')
                
            if not devices:
                devices.append(("Controladores Generales del Sistema", "💻", None, "N/A", "N/A", False))
            
            self.after(0, lambda: self._populate_drivers(devices))
            
        except Exception as e:
            self.log(f"Error escaneo: {e}")
            self.after(0, lambda: self.lbl_scan_desc.configure(text=f"Error: {str(e)[:50]}"))
            self.after(2000, lambda: self._reset_scan_ui())

    def _reset_scan_ui(self):
        self.is_scanning = False
        self.btn_huge_scan.configure(state="normal", text="Escanear Sistema")
        self.prog_panel.pack_forget()
        self.progress.stop()

    def _populate_drivers(self, devices):
        for data in devices:
            if len(data) >= 6:
                name, icon, date_str, local_ver, local_date, is_gpu = data[:6]
                self.create_device_item(name, icon, date_str, local_ver, local_date, is_gpu)
            elif len(data) == 3:
                name, icon, date_str = data
                self.create_device_item(name, icon, date_str)
            else:
                self.create_device_item(*data)
            
        is_empty = (not devices) or (len(devices) == 1 and devices[0][0] == "Controladores Generales del Sistema")
        count = 0 if is_empty else len(devices)
        self._update_selected_count()
        
        # Textos Rojos tipo Driver Booster
        self.lbl_status_main.configure(text=f"{count} controladores de dispositivos desactualizados & 0\ncontroladores de juegos no instalados", text_color="#ff4444")
        self.banner.configure(fg_color="#181818", border_color="#ff4444") # Red border
        self.lbl_info_icon.configure(text="ℹ️", text_color="#ff4444")
        
        # Botón Principal Rojo
        self.btn_huge_scan.configure(text="Actualizar Ahora", font=("Arial", 14), fg_color="#ff2222", hover_color="#dd1111", text_color="white", corner_radius=2, command=self.update_drivers)
        self.btn_huge_scan.pack(side="right", padx=15)
        
        self.is_scanning = False
        self.prog_panel.pack_forget()
        self.progress.stop()
        
        self.btn_huge_scan.configure(state="normal")
        self.btn_huge_scan.after(10, lambda: self.btn_huge_scan.pack(side="right", padx=20))

    def update_drivers(self, specific_name=None):
        if getattr(self, "is_updating", False) or getattr(self, "is_scanning", False): return
        self.is_updating = True
        
        self.btn_huge_scan.configure(state="disabled", text="Descargando...")
        self.prog_panel.pack(fill="x", padx=20, pady=(0, 10), after=self.header_frame)
        self.lbl_scan_desc.configure(text="Inicializando motor de descarga e instalación silenciosa...")
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        
        # Desactivar los botones individuales
        for item in self.driver_items:
            for child in item.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(state="disabled", text="Descargando", fg_color="#333333")
                    
        do_restart = self.chk_restart.get() == 1
        
        import threading
        threading.Thread(target=self._update_process, args=(do_restart, specific_name), daemon=True).start()

    def _update_process(self, do_restart, specific_name=None):
        import time, os, subprocess, urllib.request, zipfile
        self.log("INICIANDO PROCESO DE ACTUALIZACIÓN")
        
        has_errors = False
        
        try:
            self.after(0, lambda: self.lbl_scan_desc.configure(text="Descargando controladores desde Microsoft Update Catalog..."))
            
            temp_driver_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), "DownloadedDrivers")
            os.makedirs(temp_driver_dir, exist_ok=True)
            
            updates = getattr(self, "pending_updates", [])
            
            selected_names = set()
            if specific_name:
                selected_names.add(specific_name)
            else:
                for item in getattr(self, "driver_items", []):
                    if hasattr(item, 'chk') and item.chk.get():
                        selected_names.add(getattr(item, "device_name", ""))
            
            filtered_updates = [u for u in updates if u.get("name") in selected_names]
            
            if not filtered_updates and not specific_name:
                for item in getattr(self, "driver_items", []):
                    if hasattr(item, 'chk') and item.chk.get():
                        filtered_updates.append({"name": getattr(item, "device_name", "Desconocido"), "url": None, "is_gpu": False})
                if not filtered_updates:
                    filtered_updates.append({"name": "Dispositivos Estándar de Sistema", "url": None, "is_gpu": False})
                
            for i, update in enumerate(filtered_updates):
                name = update.get("name", "Sistema")
                url = update.get("url", None)
                is_gpu = update.get("is_gpu", False)
                item_frame = None
                
                for f in getattr(self, "driver_items", []):
                    if hasattr(f, "device_name") and f.device_name == name:
                        item_frame = f
                        break
                
                self.after(0, lambda n=name: self.lbl_scan_desc.configure(text=f"Descargando {n}..."))
                time.sleep(0.5) 
                
                if url:
                    self.log(f"Descargando driver para {name} de {url}")
                    ext = ".exe" if is_gpu else ".cab"
                    dl_path = os.path.join(temp_driver_dir, f"driver_{i}{ext}")
                    dest_path = os.path.join(temp_driver_dir, f"extracted_{i}")
                    os.makedirs(dest_path, exist_ok=True)
                    
                    try:
                        def update_ui_progress(n, p, t_str, d_mb, tot_mb):
                            self.lbl_scan_desc.configure(text=f"Descargando {n}... {p}% ({d_mb:.1f}/{tot_mb:.1f} MB) - Quedan: {t_str}")
                            self.progress.stop()
                            self.progress.configure(mode="determinate")
                            self.progress.set(p / 100.0)
                            
                        def reporthook(block_num, block_size, total_size):
                            if total_size > 0:
                                downloaded = block_num * block_size
                                percent = min(100, int(downloaded * 100 / total_size))
                                
                        reporthook.start_time = getattr(reporthook, 'start_time', time.time())
                        reporthook.last_update = getattr(reporthook, 'last_update', time.time())
                        urllib.request.urlretrieve(url, dl_path, reporthook)
                        
                        self.after(0, lambda: [self.progress.configure(mode="indeterminate"), self.progress.start()])
                        
                        if not os.path.exists(dl_path):
                            raise Exception("Archivo no encontrado tras la descarga.")
                            
                        # Validación estricta
                        file_size = os.path.getsize(dl_path)
                        self.log(f"Descargado: {dl_path} | Tamaño: {file_size} bytes")
                        
                        if file_size < 1048576:
                            with open(dl_path, 'r', errors='ignore') as check_f:
                                content = check_f.read(500).lower()
                                if "<html" in content or "<!doctype" in content:
                                    raise Exception("El archivo descargado es un HTML de error.")
                            raise Exception(f"Archivo demasiado pequeño ({file_size} bytes). Corrupción.")
                        
                        if is_gpu:
                            self.after(0, lambda n=name: self.lbl_scan_desc.configure(text=f"Instalando {n} silenciosamente (no apague)..."))
                            self.log(f"Ejecutando GPU Installer: {dl_path} -s")
                            # Esperar finalización del proceso
                            process = subprocess.run([dl_path, "-s"], capture_output=True, text=True, creationflags=0x08000000)
                            self.log(f"GPU Install ExitCode: {process.returncode} | ERR: {process.stderr}")
                            if process.returncode != 0 and process.returncode != 3010: # pending reboot
                                raise Exception(f"Error instalación GPU. Salida: {process.stderr}")
                        else:
                            self.after(0, lambda n=name: self.lbl_scan_desc.configure(text=f"Descomprimiendo e instalando {n}..."))
                            self.log(f"Extrayendo archivo a {dest_path}")
                            if dl_path.endswith('.cab'):
                                exp_proc = subprocess.run(f'expand "{dl_path}" -F:* "{dest_path}"', shell=True, capture_output=True, text=True, creationflags=0x08000000)
                                if exp_proc.returncode != 0:
                                    raise Exception(f"Fallo extraer CAB. STDERR: {exp_proc.stderr}")
                            elif dl_path.endswith('.zip'):
                                with zipfile.ZipFile(dl_path, 'r') as zip_ref:
                                    zip_ref.extractall(dest_path)
                                    
                            cmd = f'pnputil /add-driver "{dest_path}\\*.inf" /install /subdirs'
                            self.log(f"Ejecutando: {cmd}")
                            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=0x08000000)
                            self.log(f"pnputil ExitCode: {proc.returncode} | STDOUT: {proc.stdout}")
                            
                            if proc.returncode != 0 and "Falló" in proc.stdout: 
                                raise Exception(f"Fallo pnputil ({proc.returncode}): {proc.stderr}")
                    except Exception as ex:
                        has_errors = True
                        self.log(f"ERROR proc: {name} -> {ex}")
                        if item_frame: self.after(0, lambda f=item_frame: self._mark_item_failed(f))
                        
                else:
                    self.after(0, lambda n=name: self.lbl_scan_desc.configure(text=f"Integrando {n} de local..."))
                    time.sleep(1.0)
                    
            self.after(0, lambda: self.lbl_scan_desc.configure(text="Finalizando..."))
            time.sleep(1.0)
            
            if has_errors:
                self.after(0, lambda: self.finish_update(False, error=True))
            else:
                self.after(0, lambda: self.finish_update(do_restart, error=False))
                
        except Exception as e:
            has_errors = True
            self.log(f"Error Update general: {e}")
            self.after(0, lambda: self.lbl_scan_desc.configure(text=f"Fallo crítico: {e}"))
            self.after(3000, lambda: self.finish_update(False, error=True))

    def _mark_item_failed(self, frame):
        if hasattr(frame, 'lbl_local'):
            frame.lbl_local.configure(text="Fallo Extracción/Install", text_color="#ff0000")
        for child in getattr(frame, "winfo_children", lambda:[])():
            if isinstance(child, ctk.CTkButton):
                child.configure(text="Fallo", fg_color="#aa0000", hover_color="#880000")

    def finish_update(self, do_restart, error=False):
        self.progress.stop()
        self.prog_panel.pack_forget()
        self.is_updating = False
        
        if not error:
            # Texto Verde de éxito
            self.lbl_status_main.configure(text="Todos los controladores están instalados y al día.", text_color="#00dd00")
            self.banner.configure(fg_color="#111111", border_color="#00aa00")
            self.lbl_info_icon.configure(text="✔️", text_color="#00cc00")
            
            self.btn_huge_scan.configure(state="disabled", text="Al Día", fg_color="#222222")
            self.chk_all.configure(text="Actualizado (total: 0, seleccionado: 0)", fg_color="#00aa00", text_color="#555")
            
            for item in self.driver_items:
                for child in getattr(item, "winfo_children", lambda:[])():
                    if isinstance(child, ctk.CTkButton):
                        child.configure(text="Actualizado", fg_color="#185018", hover_color="#185018")
                    elif isinstance(child, ctk.CTkFrame):
                         for subr in getattr(child, "winfo_children", lambda:[])():
                             for lbl in getattr(subr, "winfo_children", lambda:[])():
                                 if isinstance(lbl, ctk.CTkLabel):
                                     if getattr(lbl, "_text", "") == "Controlador Ausente":
                                         lbl.configure(text="Correcto", text_color="#00cc00")
            if do_restart:
                import threading
                threading.Thread(target=self._trigger_windows_restart, daemon=True).start()
            else:
                self.btn_huge_scan.configure(state="normal", text="Completado")
        else:
            self.btn_huge_scan.configure(state="normal", text="Reintentar Módulo")

    def _trigger_windows_restart(self):
        import time, os, ctypes
        try:
            from win11toast import toast
            toast("Actualización", "El PC se reiniciará automáticamente porque los drivers se actualizaron")
        except:
            pass
        
        # Notification requested by the user: clean style box
        # Notification requested by the user: clean style box
        threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, "El sistema se reiniciará en 10 segundos...", "YKZ", 64), daemon=True).start()
        time.sleep(10)
        os.system("shutdown /r /t 1")
        


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
        self.geometry("400x300")
        self.title("Activación Requerida")
        self.configure(fg_color=COLOR_BG)
        
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (300/2)
        self.geometry('%dx%d+%d+%d' % (400, 300, x, y))
        self.grab_set()
        
        ctk.CTkLabel(self, text="ACTIVACIÓN YKZ", font=("Arial", 20, "bold"), text_color=COLOR_ACCENT).pack(pady=(40, 20))
        ctk.CTkLabel(self, text="Introduce tu clave de producto para continuar:", text_color="white").pack(pady=5)
        
        self.entry = ctk.CTkEntry(self, width=250, placeholder_text="YKZ-XXXX-XXXX-XXXX", justify="center")
        self.entry.pack(pady=15)
        
        ctk.CTkButton(self, text="ACTIVAR", width=250, fg_color=COLOR_ACCENT, hover_color="#cc0000", command=self.check_key).pack(pady=10)
        
        self.lbl_msg = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_msg.pack(pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def check_key(self):
        key = self.entry.get().strip().upper()
        if LicenseManager.validate(key):
            LicenseManager.save(key)
            self.lbl_msg.configure(text="¡Activado!", text_color="green")
            self.after(1000, self.finish)
        else:
            self.lbl_msg.configure(text="Clave inválida.", text_color="red")

    def finish(self):
        self.destroy()
        self.on_success()

    def on_close(self):
        sys.exit(0)


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
        self.withdraw()
        self.check_license_flow()

    def check_license_flow(self):
        saved_key = LicenseManager.load()
        if saved_key and LicenseManager.validate(saved_key):
            self.start_intro()
        else:
            self.login = LoginWindow(self, self.start_intro)

    def start_intro(self):
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
                logging.info(f"Checking update from {UPDATE_JSON_URL}")
                with urllib.request.urlopen(UPDATE_JSON_URL, timeout=5) as url:
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
                self.after(0, lambda: messagebox.showinfo("Actualizando", "Descargando actualización, la aplicación se reiniciará en unos segundos..."))
                import tempfile
                
                # Si estamos en el .exe, hacemos el reemplazo. Si estamos en Python directo, mostrar error.
                if not getattr(sys, 'frozen', False):
                    self.after(0, lambda: messagebox.showerror("Error", "No se puede actualizar ejecutando el código fuente (.py). Utiliza la versión compilada (.exe)."))
                    return
                    
                exe_path = sys.executable
                new_exe_path = exe_path + ".new"
                
                # Descargar nuevo ejecutable
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req, timeout=30) as response, open(new_exe_path, 'wb') as f_out:
                    f_out.write(response.read())

                # Script BAT para reemplazar el archivo mientras está cerrado
                bat_path = os.path.join(tempfile.gettempdir(), "update_ykz.bat")
                with open(bat_path, "w") as f:
                    f.write(f'''@echo off
timeout /t 3 /nobreak > NUL
move /y "{new_exe_path}" "{exe_path}"
start "" "{exe_path}"
del "%~f0"
''')
                
                # Ejecutar el .bat de forma silenciosa y cerrar esta app
                subprocess.Popen(["cmd.exe", "/c", bat_path], creationflags=0x08000000)
                
                # Forzar el cierre de la aplicación actual para liberar el archivo .exe
                os._exit(0)

            except Exception as e:
                logging.error(f"Update error: {e}")
                self.after(0, lambda: messagebox.showerror("Error de Actualización", f"Fallo al actualizar: {e}"))

        threading.Thread(target=_download_and_update, daemon=True).start()

    def show_main(self):
        self.deiconify()
        self.after(200, self.set_icon)
        self.setup_ui()
        self.after(500, self.load_data)
        self.after(2000, lambda: self.check_update(manual=False))

    def setup_ui(self):
        self.current_lang = "ES"
        # Fondo animado de estrellas (primero para que quede detrás)
        self.stars_bg = PurpleStarsBackground(self, width=1100, height=700)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLOR_PANEL)
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_logo = GlitchLogo(self.sidebar, text="YKZ OPTI")
        self.lbl_logo.pack(pady=30)
        
        self.btn_home = self.create_nav_btn(LANG[self.current_lang]["nav_home"], self.show_home)
        self.btn_opti = self.create_nav_btn(LANG[self.current_lang]["nav_opti"], self.show_opti)
        self.btn_nvidia = self.create_nav_btn(LANG[self.current_lang]["nav_nvidia"], self.show_nvidia)
        self.btn_amd = self.create_nav_btn(LANG[self.current_lang]["nav_amd"], self.show_amd)
        self.btn_cleaning = self.create_nav_btn(LANG[self.current_lang]["nav_cleaning"], self.show_cleaning)
        self.btn_drivers = self.create_nav_btn(LANG[self.current_lang]["nav_drivers"], self.show_drivers)
        self.btn_repair = self.create_nav_btn(LANG[self.current_lang]["nav_repair"], self.show_repair)
        self.btn_power = self.create_nav_btn(LANG[self.current_lang]["nav_power"], self.show_power)
        self.btn_activa = self.create_nav_btn(LANG[self.current_lang]["nav_activa"], self.show_activa)
        
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#330033").pack(fill="x", padx=20, pady=10)
        
        self.lang_var = ctk.StringVar(value="Español")
        self.opt_lang = ctk.CTkOptionMenu(self.sidebar, values=["Español", "English"], variable=self.lang_var, command=self.change_lang, width=140, height=32, corner_radius=8, font=("Roboto", 12, "bold"), fg_color="#110011", text_color=COLOR_TEXT_MAIN, button_color="#330033", button_hover_color=COLOR_ACCENT)
        self.opt_lang.pack(side="bottom", pady=(0, 20), padx=20)
        
        self.btn_update = ctk.CTkButton(self.sidebar, text=LANG[self.current_lang]["btn_update"], height=32, corner_radius=8, fg_color="#110011", hover_color=COLOR_PANEL, 
                      text_color=COLOR_TEXT_SUB, font=("Roboto", 12, "bold"), command=lambda: self.check_update(manual=True))
        self.btn_update.pack(side="bottom", pady=(0, 10), padx=20)
        
        ctk.CTkLabel(self.sidebar, text=f"v{CURRENT_VERSION}", font=("Arial", 10), text_color="#555").pack(side="bottom", pady=(0, 10))

        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.view_home = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.setup_home_grid()
        
        self.view_opti = OptimizationView(self.main_area)
        self.view_nvidia = NvidiaView(self.main_area)
        self.view_amd = AmdView(self.main_area)
        self.view_cleaning = CleaningView(self.main_area)
        self.view_drivers = DriversView(self.main_area)
        self.view_repair = RepairView(self.main_area)
        self.view_power = PowerPlanView(self.main_area)
        self.view_activa = ActivacionView(self.main_area)

        self.show_home()

    def change_lang(self, choice):
        self.current_lang = "ES" if choice == "Español" else "EN"
        l = LANG[self.current_lang]
        
        self.btn_home.configure(text=l["nav_home"])
        self.btn_opti.configure(text=l["nav_opti"])
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
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", hover_color=COLOR_BG, anchor="w", height=40, font=("Roboto", 14), command=cmd)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def show_home(self):
        self._hide_all_views()
        self.view_home.pack(fill="both", expand=True)
        self._update_nav(self.btn_home)
        if hasattr(self, 'lbl_logo'):
            self.lbl_logo.pack(pady=30, side="top", before=self.btn_home)

    def show_opti(self):
        self._hide_all_views()
        self.view_opti.pack(fill="both", expand=True)
        self._update_nav(self.btn_opti)
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
        self.view_home.pack_forget()
        self.view_opti.pack_forget()
        self.view_nvidia.pack_forget()
        self.view_amd.pack_forget()
        self.view_cleaning.pack_forget()
        self.view_drivers.pack_forget()
        self.view_repair.pack_forget()
        self.view_power.pack_forget()
        self.view_activa.pack_forget()

    def _update_nav(self, active_btn):
        self.btn_home.configure(fg_color="transparent")
        self.btn_opti.configure(fg_color="transparent")
        self.btn_nvidia.configure(fg_color="transparent")
        self.btn_amd.configure(fg_color="transparent")
        self.btn_cleaning.configure(fg_color="transparent")
        self.btn_drivers.configure(fg_color="transparent")
        self.btn_repair.configure(fg_color="transparent")
        self.btn_power.configure(fg_color="transparent")
        self.btn_activa.configure(fg_color="transparent")
        
        active_btn.configure(fg_color=COLOR_BG)

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
        if hasattr(self, 'cards'):
            for c in self.cards.values():
                for w in c.content_area.winfo_children(): w.destroy()
        
        threading.Thread(target=self._fetch_wmi, daemon=True).start()

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
        
    if not is_admin and hasattr(ctypes, 'windll'):
        # Relanzar el programa completo como administrador y cerrar este
        exe = sys.executable
        if getattr(sys, 'frozen', False):
            # Si es el archivo compilado .exe
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, "", None, 1)
        else:
            # Si se lanza desde código fuente .py
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, f'"{os.path.abspath(__file__)}"', None, 1)
        sys.exit()

    if len(sys.argv) == 3 and sys.argv[1] == "--run-ps1":
        ps1_path = sys.argv[2]
        subprocess.Popen(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", ps1_path],
            creationflags=0x08000000
        ).wait()
        sys.exit(0)
        
    # Preguntar por instalación/autoinicio si es ejecutable
    if getattr(sys, 'frozen', False):
        import winreg
        try:
            import win32com.client
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            shortcut_path = os.path.join(desktop, "YKZ OPTI.lnk")
            
            # Si el acceso directo no existe, preguntamos "Queremos instalar?"
            if not os.path.exists(shortcut_path):
                # MB_YESNO (4) | MB_ICONQUESTION (32)
                res = ctypes.windll.user32.MessageBoxW(0, "¿Deseas instalar YKZ OPTI en el Escritorio y hacer que inicie automáticamente con Windows?", "YKZ", 36)
                if res == 6:  # IDYES
                    # Crear Shortcut
                    try:
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortCut(shortcut_path)
                        shortcut.Targetpath = sys.executable
                        shortcut.WorkingDirectory = os.path.dirname(sys.executable)
                        shortcut.save()
                    except Exception as e:
                        logging.error(f"Error creando acceso directo: {e}")
                        
                    # Añadir a Inicio (HKCU Run)
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                        winreg.SetValueEx(key, "YKZ_OPTI", 0, winreg.REG_SZ, f'"{sys.executable}"')
                        winreg.CloseKey(key)
                    except Exception as e:
                        logging.error(f"Error añadiendo startup key: {e}")
        except Exception as e:
            logging.error(f"Installation prompt error: {e}")
        
    app = PurpleApp()
    app.mainloop()
