from flask import Flask, request, jsonify
import subprocess
import os
import json
import ssl

app = Flask(__name__)

@app.route('/dingtalk', methods=['POST'])
def handle_message():
    # 简化版：直接处理明文消息（需在钉钉关闭加密）
    data = request.json
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
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=8443, ssl_context=context)