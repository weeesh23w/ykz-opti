import json
import os
import urllib.request
import base64
from io import BytesIO

def handler(environ, start_response):
    # Solo permitir POST
    if environ.get('REQUEST_METHOD') != 'POST':
        start_response('405 Method Not Allowed', [('Content-Type', 'application/json')])
        return [json.dumps({"error": "Method not allowed"}).encode()]

    try:
        # Leer el cuerpo de la petición
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        body = json.loads(request_body.decode('utf-8'))
        
        key = body.get('key', '').upper()
        hwid = body.get('hwid', '')
        ip = body.get('ip', '0.0.0.0')

        if not key or not hwid:
            start_response('400 Bad Request', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "Key and HWID are required"}).encode()]

        # --- Configuration ---
        GH_TOKEN = os.environ.get('GH_TOKEN')
        REPO = "weeesh23w/ykz-opti"
        FILE_PATH = "licencias.json"
        
        if not GH_TOKEN:
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "GH_TOKEN no configurado en Vercel"}).encode()]

        # 1. Fetch current licencias.json from GitHub
        api_url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
        headers = {
            "Authorization": f"token {GH_TOKEN}", 
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Vercel-Serverless"
        }
        
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode())
            content = base64.b64decode(res_data['content']).decode('utf-8')
            sha = res_data['sha']
            db = json.loads(content)

        # 2. Logic Check
        keys = db.get('keys', [])
        used_keys = db.get('used_keys', {})

        if key not in keys:
            start_response('403 Forbidden', [('Content-Type', 'application/json')])
            return [json.dumps({"success": False, "error": "Licencia inexistente"}).encode()]

        if key in used_keys:
            if used_keys[key]['hwid'] == hwid:
                start_response('200 OK', [('Content-Type', 'application/json')])
                return [json.dumps({"success": True, "message": "Re-activación exitosa (mismo HWID)"}).encode()]
            else:
                start_response('403 Forbidden', [('Content-Type', 'application/json')])
                return [json.dumps({"success": False, "error": "Licencia ya usada en otro PC"}).encode()]

        # 3. Register New Usage
        used_keys[key] = {"hwid": hwid, "ip": ip, "date": "2026-03-17"}
        db['used_keys'] = used_keys
        
        # 4. Push update back to GitHub
        new_content = base64.b64encode(json.dumps(db, indent=4).encode()).decode()
        update_data = json.dumps({
            "message": f"Activate key {key} for HWID {hwid}",
            "content": new_content,
            "sha": sha
        }).encode()
        
        update_req = urllib.request.Request(api_url, data=update_data, headers=headers, method='PUT')
        with urllib.request.urlopen(update_req, timeout=10) as update_res:
             start_response('200 OK', [('Content-Type', 'application/json')])
             return [json.dumps({"success": True, "message": "Activado y vinculado a tu PC"}).encode()]

    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return [json.dumps({"error": f"Error del servidor: {str(e)}"}).encode()]
