import shutil
import os

src_dir = r"C:\Users\666\.gemini\antigravity\brain\4f4d0914-6500-4fe2-a016-500a13214a92"
dest_dir = r"c:\Users\666\Desktop\666\website\assets"

files = {
    "media__1773750480767.png": "user_ui_1.png",
    "media__1773750504806.png": "user_ui_2.png",
    "media__1773750524237.png": "user_ui_3.png"
}

for src_name, dest_name in files.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    print(f"Copying {src_path} to {dest_path}")
    shutil.copy2(src_path, dest_path)

print("Done.")
