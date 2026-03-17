from flask import Flask, request, jsonify
import subprocess
import os
import json
import hashlib
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

TOKEN = "openclaw_secure_token_2026"
AES_KEY = "NRridbO2lNZ0fzJxn7aplYW1VbmW3uhX3CHtYa5IdvI"

def decrypt(encrypted_data):
    key = base64.b64decode(AES_KEY + "=")
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
    pad = decrypted[-1]
    return decrypted[:-pad].decode('utf-8')

def verify_signature(timestamp, nonce, msg_encrypt):
    raw = f"{TOKEN}{timestamp}{nonce}{msg_encrypt}"
    sign = hashlib.sha256(raw.encode()).hexdigest()
    return sign == request.args.get('signature')

@app.route('/dingtalk', methods=['POST'])
def handle_message():
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    msg_encrypt = request.json.get('encrypt')
    
    if not verify_signature(timestamp, nonce, msg_encrypt):
        return "Forbidden", 403

    try:
        decrypted_json = decrypt(msg_encrypt)
        data = json.loads(decrypted_json)
    except Exception as e:
        return f"Decrypt error: {str(e)}", 400

    if 'text' in data:
        user_input = data['text']['content'].strip()
        result = subprocess.run(
            ['timeout', '30', 'openclaw', 'ask', user_input],
            capture_output=True,
            text=True,
            cwd='/root/.openclaw/workspace'
        )
        response = (result.stdout or result.stderr)[:2000]
        return jsonify({"msgtype": "text", "text": {"content": response}})
    
    return jsonify({"status": "ignored"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)  # 明确指定8080端口