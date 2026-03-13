import os
import glob
from PIL import Image

workspace = r"c:\Users\666\Desktop\Nueva carpeta"
resources = os.path.join(workspace, "resources")
os.makedirs(resources, exist_ok=True)

home = os.environ.get('USERPROFILE') or os.path.expanduser('~')
search_dirs = [os.path.join(home, 'Downloads'), os.path.join(home, 'Desktop'), os.path.join(home, 'Pictures')]

candidates = []
for d in search_dirs:
    if not os.path.isdir(d):
        continue
    for ext in ('*.png','*.jpg','*.jpeg'):
        candidates.extend(glob.glob(os.path.join(d, '**', ext), recursive=True))

if not candidates:
    print('NO_IMAGES')
    raise SystemExit(1)

candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
src = candidates[0]

# Load and save
try:
    img = Image.open(src)
    splash_dst = os.path.join(resources, 'splash_start.jpg')
    exe_dst = os.path.join(resources, 'exe_icon.png')
    # Save splash as JPEG
    rgb = img.convert('RGB')
    rgb.save(splash_dst, format='JPEG', quality=90)
    # Save exe icon as PNG
    img.save(exe_dst, format='PNG')
    print('OK')
    print(src)
    print(splash_dst)
    print(exe_dst)
except Exception as e:
    print('ERROR', e)
    raise
