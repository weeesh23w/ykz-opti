import json
import os
import urllib.request
import base64

def handler(request):
    if request.method != 'POST':
        return {"statusCode": 405, "body": json.dumps({"error": "Method not allowed"})}

    try:
        body = json.loads(request.body.decode('utf-8'))
        key = body.get('key', '').upper()
        hwid = body.get('hwid', '')
        ip = body.get('ip', '0.0.0.0')

        if not key or not hwid:
            return {"statusCode": 400, "body": json.dumps({"error": "Key and HWID are required"})}

        # --- Configuration ---
        GH_TOKEN = os.environ.get('GH_TOKEN') # Debe configurarse en Vercel
        REPO = "weeesh23w/ykz-opti"
        FILE_PATH = "licencias.json"
        
        if not GH_TOKEN:
            return {"statusCode": 500, "body": json.dumps({"error": "Server configuration error (GH_TOKEN missing)"})}

        # 1. Fetch current licencias.json from GitHub
        api_url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            content = base64.b64decode(res_data['content']).decode('utf-8')
            sha = res_data['sha']
            db = json.loads(content)

        # 2. Logic Check
        keys = db.get('keys', [])
        used_keys = db.get('used_keys', {})

        if key not in keys:
            return {"statusCode": 403, "body": json.dumps({"success": False, "error": "Esta licencia no existe."})}

        if key in used_keys:
            if used_keys[key]['hwid'] == hwid:
                return {"statusCode": 200, "body": json.dumps({"success": True, "message": "Licencia ya vinculada a este equipo."})}
            else:
                return {"statusCode": 403, "body": json.dumps({"success": False, "error": "Esta licencia ya está en uso en otro ordenador."})}

        # 3. Register New Usage
        used_keys[key] = {"hwid": hwid, "ip": ip, "date": "2026-03-17"} # Simple date for now
        db['used_keys'] = used_keys
        
        # 4. Push update back to GitHub
        new_content = base64.b64encode(json.dumps(db, indent=4).encode()).decode()
        update_data = json.dumps({
            "message": f"Activate key {key} for HWID {hwid}",
            "content": new_content,
            "sha": sha
        }).encode()
        
        update_req = urllib.request.Request(api_url, data=update_data, headers=headers, method='PUT')
        with urllib.request.urlopen(update_req) as update_res:
            return {"statusCode": 200, "body": json.dumps({"success": True, "message": "Licencia activada con éxito y vinculada a tu HWID."})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
