from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
            key = body.get('key', '').upper()
            hwid = body.get('hwid', '')
            ip = body.get('ip', '0.0.0.0')

            if not key or not hwid:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Key and HWID are required"}).encode())
                return

            GH_TOKEN = os.environ.get('GH_TOKEN')
            REPO = "weeesh23w/ykz-opti"
            FILE_PATH = "licencias.json"
            
            if not GH_TOKEN:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "GH_TOKEN no configurado"}).encode())
                return

            # 1. Fetch current licencias.json
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
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Licencia inexistente"}).encode())
                return

            if key in used_keys:
                if used_keys[key]['hwid'] == hwid:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "message": "Re-activación exitosa"}).encode())
                    return
                else:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Licencia ya usada"}).encode())
                    return

            # 3. Register New Usage
            used_keys[key] = {"hwid": hwid, "ip": ip, "date": "2026-03-18"}
            db['used_keys'] = used_keys
            
            # 4. Push update
            new_content = base64.b64encode(json.dumps(db, indent=4).encode()).decode()
            update_data = json.dumps({
                "message": f"Activate key {key}",
                "content": new_content,
                "sha": sha
            }).encode()
            
            update_req = urllib.request.Request(api_url, data=update_data, headers=headers, method='PUT')
            with urllib.request.urlopen(update_req, timeout=10) as update_res:
                 self.send_response(200)
                 self.send_header('Content-type', 'application/json')
                 self.end_headers()
                 self.wfile.write(json.dumps({"success": True, "message": "Activado correctamente"}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
