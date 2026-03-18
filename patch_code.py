import re
import os

def patch():
    file_path = r"c:\Users\666\Desktop\666\codigo_completo.py"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the check_key method body
    pattern = re.compile(
        r'(def check_key\(self\):.*?key = self\.entry\.get\(\)\.strip\(\)\.upper\(\)\n)(        if LicenseManager\.validate\(key\):.*?else:.*?self\.lbl_msg\.configure\(text=l\["login_fail"\], text_color="red"\)\n)',
        re.DOTALL
    )

    replacement = r'''\1        if not key: return
        self.lbl_msg.configure(text="Validando...", text_color="white")
        self.update()
        success, msg = LicenseManager.validate(key)
        if success:
            LicenseManager.save(key)
            self.lbl_msg.configure(text=l["login_success"], text_color="green")
            messagebox.showinfo("YKZ OPTI", f"¡Activado!\\n{msg}")
            self.after(500, self.finish)
        else:
            self.lbl_msg.configure(text=msg, text_color="red")
'''
    
    new_content = pattern.sub(replacement, content)
    
    if new_content == content:
        print("No se encontró el patrón para parchear.")
        # Intento 2 con patrón más simple
        pattern2 = re.compile(r'if LicenseManager\.validate\(key\):.*?self\.lbl_msg\.configure\(text=l\["login_fail"\], text_color="red"\)', re.DOTALL)
        new_content = pattern2.sub(r'success, msg = LicenseManager.validate(key)\n        if success:\n            LicenseManager.save(key)\n            self.lbl_msg.configure(text=l["login_success"], text_color="green")\n            messagebox.showinfo("YKZ OPTI", f"¡Activado!\\n{msg}")\n            self.after(500, self.finish)\n        else:\n            self.lbl_msg.configure(text=msg, text_color="red")', content)
        if new_content == content:
            print("Intento 2 fallido.")
            return

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Parche aplicado con éxito.")

if __name__ == "__main__":
    patch()
