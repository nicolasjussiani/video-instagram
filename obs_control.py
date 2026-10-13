import base64
import hashlib
import json
import os
import sys
import uuid
from pathlib import Path

import websocket

cfg = json.loads((Path(os.environ['APPDATA']) / 'obs-studio/plugin_config/obs-websocket/config.json').read_text(encoding='utf-8-sig'))
ws = websocket.create_connection(f"ws://127.0.0.1:{cfg['server_port']}", timeout=20)
hello = json.loads(ws.recv())['d']
identify = {'rpcVersion': 1, 'eventSubscriptions': 0}
if 'authentication' in hello:
    a = hello['authentication']
    secret = base64.b64encode(hashlib.sha256((cfg['server_password'] + a['salt']).encode()).digest()).decode()
    identify['authentication'] = base64.b64encode(hashlib.sha256((secret + a['challenge']).encode()).digest()).decode()
ws.send(json.dumps({'op': 1, 'd': identify}))
assert json.loads(ws.recv())['op'] == 2

def request(kind, data=None):
    rid = str(uuid.uuid4())
    ws.send(json.dumps({'op': 6, 'd': {'requestType': kind, 'requestId': rid, 'requestData': data or {}}}))
    while True:
        message = json.loads(ws.recv())
        if message['op'] == 7 and message['d']['requestId'] == rid:
            result = message['d']
            if not result['requestStatus']['result']:
                raise RuntimeError(f"{kind}: {result['requestStatus']}")
            return result.get('responseData', {})

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        commands = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
    else:
        commands = json.loads(sys.argv[1])
    for command in commands:
        result = request(command['type'], command.get('data'))
        if command.get('save_image'):
            Path(command['save_image']).write_bytes(base64.b64decode(result['imageData'].split(',', 1)[1]))
            result = {'image_saved': command['save_image']}
        print(json.dumps({'type': command['type'], 'result': result}, ensure_ascii=False))
    ws.close(timeout=1)
