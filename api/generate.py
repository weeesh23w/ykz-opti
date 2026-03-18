import json
import os
import urllib.request
import base64
from datetime import datetime

def handler(environ, start_response):
    # Allow CORS
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type'),
    ]

    if environ.get('REQUEST_METHOD') == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']

    if environ.get('REQUEST_METHOD') != 'POST':
        start_response('405 Method Not Allowed', headers)
        return [json.dumps({"error": "Method not allowed"}).encode()]

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        body = json.loads(request_body.decode('utf-8')) if request_body_size > 0 else {}

        # Optional: stripe session_id or order reference
        session_id = body.get('session_id', 'direct')

        GH_TOKEN = os.environ.get('GH_TOKEN')
        REPO = "weeesh23w/ykz-opti"
        FILE_PATH = "licencias.json"

        if not GH_TOKEN:
            start_response('500 Internal Server Error', headers)
            return [json.dumps({"error": "GH_TOKEN no configurado en el servidor"}).encode()]

        # 1. Fetch licencias.json from GitHub
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

        keys = db.get('keys', [])
        used_keys = db.get('used_keys', {})
        issued_keys = db.get('issued_keys', {})  # keys delivered but not yet activated

        # 2. Find an available key (not used, not already issued)
        already_taken = set(used_keys.keys()) | set(issued_keys.keys())
        available = [k for k in keys if k not in already_taken]

        if not available:
            start_response('503 Service Unavailable', headers)
            return [json.dumps({"error": "No hay licencias disponibles. Contacta soporte."}).encode()]

        # 3. Pick the first available key
        assigned_key = available[0]

        # 4. Mark it as issued
        issued_keys[assigned_key] = {
            "session_id": session_id,
            "issued_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        db['issued_keys'] = issued_keys

        # 5. Push update to GitHub
        new_content = base64.b64encode(json.dumps(db, indent=4).encode()).decode()
        update_data = json.dumps({
            "message": f"Issue key {assigned_key} for session {session_id}",
            "content": new_content,
            "sha": sha
        }).encode()

        update_req = urllib.request.Request(api_url, data=update_data, headers=gh_headers, method='PUT')
        with urllib.request.urlopen(update_req, timeout=10):
            pass

        start_response('200 OK', headers)
        return [json.dumps({
            "success": True,
            "key": assigned_key
        }).encode()]

    except Exception as e:
        start_response('500 Internal Server Error', headers)
        return [json.dumps({"error": str(e)}).encode()]
