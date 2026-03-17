from flask import Flask, request, jsonify
import subprocess
import os
import json
import hashlib
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

# 加载安全凭证
TOKEN = os.getenv('DINGTALK_TOKEN', '')
AES_KEY = os.getenv('DINGTALK_AES_KEY', '')

def decrypt(encrypted_data):
    """钉钉消息解密"""
    key = base64.b64decode(AES_KEY + "=")
    cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])
    decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
    # 移除 PKCS7 填充
    pad = decrypted[-1]
    return decrypted[:-pad].decode('utf-8')

def verify_signature(timestamp, nonce, msg_encrypt):
    """验证钉钉签名（正确方式）"""
    # 计算签名: sha256(TOKEN + timestamp + nonce + encrypt)
    raw = f"{TOKEN}{timestamp}{nonce}{msg_encrypt}"
    sign = hashlib.sha256(raw.encode()).hexdigest()
    return sign == request.args.get('signature')

@app.route('/dingtalk', methods=['POST'])
def handle_message():
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    msg_encrypt = request.json.get('encrypt')
    
    # 验证签名
    if not verify_signature(timestamp, nonce, msg_encrypt):
        return "Forbidden", 403

    # 解密消息
    try:
        decrypted_json = decrypt(msg_encrypt)
        data = json.loads(decrypted_json)
    except Exception as e:
        return f"Decrypt error: {str(e)}", 400

    # 处理消息
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
    app.run(host='0.0.0.0', port=8081)