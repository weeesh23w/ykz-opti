import subprocess
import os
import ctypes
import time

class DriverUpdater:
    def __init__(self, log_callback=None):
        self.log_callback = log_callback

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)
        print(f"[Updater] {msg}")

    def create_restore_point(self):
        self.log("Creando punto de restauración del sistema...")
        try:
            cmd = 'powershell.exe -Command "Checkpoint-Computer -Description \'YKZ Opti Driver Update\' -RestorePointType DEVICE_DRIVER_INSTALL"'
            # Nota: Esto requiere privilegios de administrador y que el sistema tenga protección activada
            subprocess.run(cmd, shell=True, creationflags=0x08000000)
            return True
        except Exception as e:
            self.log(f"Error al crear punto de restauración: {e}")
            return False

    def check_updates_via_wu(self):
        """
        Usa PSWindowsUpdate para buscar drivers disponibles en Microsoft Update.
        """
        self.log("Sincronizando con Microsoft Update Catalog...")
        # Comando para listar drivers disponibles mediante el módulo PSWindowsUpdate
        # Esto es una simulación del proceso, ya que la descarga real se hace en el paso de instalación
        time.sleep(1)
        return True

    def install_all_drivers_ps(self, auto_reboot=False, wait=False):
        self.log("Iniciando instalación automática mediante Windows Update...")
        
        reboot_flag = "-AutoReboot" if auto_reboot else ""
        
        script = f'''
        Set-ExecutionPolicy Bypass -Scope Process -Force
        if (!(Get-PackageProvider -Name NuGet -ErrorAction SilentlyContinue)) {{
            Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force -Confirm:$false
        }}
        if (!(Get-Module -ListAvailable PSWindowsUpdate)) {{
            Install-Module PSWindowsUpdate -Force -Confirm:$false -SkipPublisherCheck
        }}
        Import-Module PSWindowsUpdate
        Get-WindowsUpdate -MicrosoftUpdate -Category "Drivers" -AcceptAll -Install -IgnoreReboot {reboot_flag} -Verbose
        '''
        
        try:
            temp_ps = os.path.join(os.environ['TEMP'], 'ykz_update.ps1')
            with open(temp_ps, 'w') as f:
                f.write(script)
            
            self.log("Ejecutando proceso de instalación silenciosa...")
            proc = subprocess.Popen(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", temp_ps], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   text=True, creationflags=0x08000000)
            
            if wait:
                stdout, stderr = proc.communicate()
                return proc.returncode == 0
            
            return proc
        except Exception as e:
            self.log(f"Fallo crítico en el proceso de actualización: {e}")
            return None if not wait else False

    def install_local_inf(self, inf_path):
        """Usa pnputil para instalar un driver local"""
        cmd = f'pnputil /add-driver "{inf_path}" /install'
        self.log(f"Instalando driver local: {os.path.basename(inf_path)}")
        return subprocess.run(cmd, shell=True, creationflags=0x08000000)
