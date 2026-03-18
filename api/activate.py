import json
import os
import urllib.request
import base64
from datetime import datetime

def handler(environ, start_response):
    # CORS headers (needed for browser fetch calls)
    cors_headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type'),
    ]

    # Handle preflight
    if environ.get('REQUEST_METHOD') == 'OPTIONS':
        start_response('200 OK', cors_headers)
        return [b'']

    if environ.get('REQUEST_METHOD') != 'POST':
        start_response('405 Method Not Allowed', cors_headers)
        return [json.dumps({"error": "Method not allowed"}).encode()]

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        body = json.loads(request_body.decode('utf-8'))

        key = body.get('key', '').strip().upper()
        hwid = body.get('hwid', '').strip()
        ip = body.get('ip', environ.get('REMOTE_ADDR', '0.0.0.0'))

        if not key or not hwid:
            start_response('400 Bad Request', cors_headers)
            return [json.dumps({"error": "Key y HWID son requeridos"}).encode()]

        GH_TOKEN = os.environ.get('GH_TOKEN')
        REPO = "weeesh23w/ykz-opti"
        FILE_PATH = "licencias.json"

        if not GH_TOKEN:
            start_response('500 Internal Server Error', cors_headers)
            return [json.dumps({"error": "GH_TOKEN no configurado en el servidor"}).encode()]

        # 1. Fetch current licencias.json from GitHub
        api_url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
        gh_headers = {
            "Authorization": f"token {GH_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Vercel-Serverless"
        }

        req = urllib.request.Request(api_url, headers=gh_headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode())
            content = base64.b64decode(res_data['content']).decode('utf-8')
            sha = res_data['sha']
            db = json.loads(content)

        # 2. Logic Check
        keys = db.get('keys', [])
        used_keys = db.get('used_keys', {})

        # Key must exist in the pool (or in issued_keys)
        issued_keys = db.get('issued_keys', {})
        all_valid_keys = set(keys) | set(issued_keys.keys())

        if key not in all_valid_keys:
            start_response('403 Forbidden', cors_headers)
            return [json.dumps({"success": False, "error": "Licencia inexistente o inválida"}).encode()]

        # Check if already activated
        if key in used_keys:
            if used_keys[key]['hwid'] == hwid:
                # Same hardware → allow re-activation
                start_response('200 OK', cors_headers)
                return [json.dumps({"success": True, "message": "Re-activación exitosa en tu dispositivo"}).encode()]
            else:
                start_response('403 Forbidden', cors_headers)
                return [json.dumps({"success": False, "error": "Esta licencia ya está activada en otro dispositivo"}).encode()]

        # 3. Register new activation
        used_keys[key] = {
            "hwid": hwid,
            "ip": ip,
            "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        db['used_keys'] = used_keys

        # 4. Push update to GitHub
        new_content = base64.b64encode(json.dumps(db, indent=4).encode()).decode()
        update_data = json.dumps({
            "message": f"Activate key {key[:12]}...",
            "content": new_content,
            "sha": sha
        }).encode()

        update_req = urllib.request.Request(api_url, data=update_data, headers=gh_headers, method='PUT')
        with urllib.request.urlopen(update_req, timeout=10):
            pass

        start_response('200 OK', cors_headers)
        return [json.dumps({"success": True, "message": "¡Activado correctamente! Bienvenido a YKZ Premium."}).encode()]

    except Exception as e:
        start_response('500 Internal Server Error', cors_headers)
        return [json.dumps({"error": f"Error del servidor: {str(e)}"}).encode()]
