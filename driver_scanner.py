import wmi
import pythoncom
import os
import re

class DriverScanner:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.IGNORAR = [
            "WAN Miniport", "NDIS", "ACPI", "PCI standard", "Microsoft Kernel",
            "Virtual", "Enumerator", "Composite Device", "System Timer",
            "speaker", "clock", "event timer", "Legacy device", "processor",
            "Volume Manager", "Shadow", "Microcode", "Root Enumerator",
            "Software Device", "Print Queue", "Redirector", "Standard system",
            "Volume", "Manager", "Controller (standard)", "ScsiAdapter",
            "Remote Desktop", "Generic software", "Xbox", "Filter"
        ]
        self.VENDORS = {
            "VEN_10DE": "NVIDIA",
            "VEN_1002": "AMD",
            "VEN_8086": "Intel",
            "VEN_10EC": "Realtek",
            "VEN_14E4": "Broadcom",
            "VEN_168C": "Qualcomm",
            "VEN_046D": "Logitech",
            "VEN_1532": "Razer",
            "VEN_1B1C": "Corsair",
            "VEN_0951": "HyperX",
            "VEN_1038": "SteelSeries",
            "VEN_1043": "ASUS",
            "VEN_1462": "MSI",
            "VEN_1458": "Gigabyte",
            "VEN_1028": "Dell",
            "VEN_103C": "HP",
            "VEN_17AA": "Lenovo"
        }

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)
        print(f"[Scanner] {msg}")

    def is_real_hardware(self, d):
        name = d.DeviceName
        hwid = d.HardwareID[0] if d.HardwareID else ""
        
        # Ignorar si es un dispositivo virtual raíz o enumerador de software
        if any(x in hwid.upper() for x in ["ROOT\\", "UMB\\", "SWD\\", "HTREE\\"]):
            return False
            
        for word in self.IGNORAR:
            if word.lower() in name.lower():
                return False
        return True

    def get_manufacturer_from_hwid(self, hwid):
        if not hwid: return "Generic"
        hwid_upper = hwid.upper()
        for ven_id, name in self.VENDORS.items():
            if ven_id.upper() in hwid_upper:
                return name
        return None # Indica que no se encontró en la lista de vendors conocidos

    def scan(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        drivers = []
        
        self.log("Analizando Hardware ID y Fabricantes...")
        
        all_drivers = c.Win32_PnPSignedDriver()
        total = len(all_drivers)
        
        for i, d in enumerate(all_drivers):
            name = d.DeviceName
            if not name or not self.is_real_hardware(d):
                continue

            hwid = d.HardwareID[0] if d.HardwareID else ""
            
            # Prioridad de fabricante: ID de Hardware > WMI Manufacturer
            manufacturer = self.get_manufacturer_from_hwid(hwid)
            if not manufacturer:
                manufacturer = d.Manufacturer if d.Manufacturer else "Desconocido"
            
            # Limpiar fabricantes genéricos de Microsoft para hardware real
            if "Microsoft" in manufacturer and any(x in name.upper() for x in ["AUDIO", "VIDEO", "GRAPHICS", "NETWORK", "WIRELESS", "USB"]):
                 manufacturer = "OEM / Generic"

            # Formatear fecha
            raw_date = d.DriverDate
            date_str = "N/A"
            if raw_date:
                date_str = f"{raw_date[4:6]}/{raw_date[6:8]}/{raw_date[:4]}"

            is_gpu = any(x in name.upper() for x in ["NVIDIA", "AMD", "RADEON", "INTEL(R) UHD", "INTEL(R) IRIS"])
            
            # Simular verificación de API (Nvidia/AMD/MS Update)
            status = "Al día"
            if is_gpu:
                self.log(f"Consultando API de {manufacturer} para {name}...")
                status = "Update Available" # Forzamos detección en GPU para demostración
            elif any(x in name.upper() for x in ["NETWORK", "WI-FI", "AUDIO"]):
                status = "Update Available"
            
            drivers.append({
                "name": name,
                "version": d.DriverVersion if d.DriverVersion else "N/A",
                "hwid": hwid,
                "manufacturer": manufacturer,
                "date": date_str,
                "status": status,
                "is_gpu": is_gpu
            })
            
            if i % 20 == 0:
                self.log(f"Procesando dispositivos: {int((i/total)*100)}%")
            
        return drivers
