from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import base64
from datetime import datetime


class handler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(200, {})

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}

            key = body.get('key', '').strip().upper()
            hwid = body.get('hwid', '').strip()
            ip = body.get('ip', self.client_address[0] if self.client_address else '0.0.0.0')

            if not key or not hwid:
                self._send_json(400, {"error": "Key y HWID son requeridos"})
                return

            GH_TOKEN = os.environ.get('GH_TOKEN')
            REPO = "weeesh23w/ykz-opti"
            FILE_PATH = "licencias.json"

            if not GH_TOKEN:
                self._send_json(500, {"error": "GH_TOKEN no configurado en el servidor"})
                return

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
            issued_keys = db.get('issued_keys', {})

            # All valid keys = pool + issued
            all_valid_keys = set(keys) | set(issued_keys.keys())

            if key not in all_valid_keys:
                self._send_json(403, {"success": False, "error": "Licencia inexistente o inválida"})
                return

            # Check if already activated
            if key in used_keys:
                if used_keys[key]['hwid'] == hwid:
                    self._send_json(200, {"success": True, "message": "Re-activación exitosa en tu dispositivo"})
                    return
                else:
                    self._send_json(403, {"success": False, "error": "Esta licencia ya está activada en otro dispositivo"})
                    return

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

            self._send_json(200, {"success": True, "message": "¡Activado correctamente! Bienvenido a YKZ Premium."})

        except Exception as e:
            self._send_json(500, {"error": f"Error del servidor: {str(e)}"})
