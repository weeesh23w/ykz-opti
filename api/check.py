import json
def handler(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [json.dumps({"status": "ok", "service": "YKZ API"}).encode()]
