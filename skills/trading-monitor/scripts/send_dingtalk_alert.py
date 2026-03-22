#!/usr/bin/env python3
"""
DingTalk Alert Sender
Sends trading signals to DingTalk groups

Usage:
    python send_dingtalk_alert.py "<message>"
    
Environment variables:
    DINGTALK_WEBHOOK_URL - DingTalk webhook URL
    DINGTALK_SECRET      - Secret key (optional, for signature)
"""

import os
import sys
import json
import time
import requests
import hmac
import hashlib
import base64
from datetime import datetime


def build_dingtalk_payload(message, secret=None):
    """Build DingTalk webhook payload"""
    timestamp = str(round(time.time() * 1000))
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "xA股S1信号监控",
            "text": message
        },
        "at": {
            "isAtAll": False
        }
    }
    
    # Add timestamp and signature if secret provided
    if secret:
        string_to_sign = f"{timestamp}\n{secret}"
        signature = base64.b64encode(
            hmac.new(
                secret.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        payload['timestamp'] = timestamp
        payload['sign'] = signature
    
    return payload, timestamp


def send_dingtalk_alert(webhook_url, message, secret=None, timeout=10):
    """
    Send alert to DingTalk group
    
    Args:
        webhook_url: DingTalk robot webhook URL
        message: Alert message content (markdown format)
        secret: Secret key for signature (if enabled)
        timeout: Request timeout in seconds
    
    Returns:
        dict: Response from DingTalk API
    """
    headers = {
        'Content-Type': 'application/json',
    }
    
    payload, timestamp = build_dingtalk_payload(message, secret)
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=timeout)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'timestamp': timestamp}
    except Exception as e:
        return {'error': f'Unknown error: {str(e)}', 'timestamp': timestamp}


def format_message(signals, is_test=False):
    """
    Format signals into DingTalk markdown message
    
    Args:
        signals: List of detected signals
        is_test: Whether this is a test run
    
    Returns:
        str: Formatted markdown message
    """
    if not signals:
        message = """📊 **A股S1信号监控 - 10:00**

**当前时段无S1级别强信号（≥95%置信度）**

---
*监控时间: {}
*数据源: 东方财富*
*系统: Trading Monitor v1.0*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return message
    
    # Build message
    message = """📊 **A股S1信号监控 - 10:00**

**🔍 发现 {} 个S1级强信号（≥95%置信度）**

---
""".format(len(signals))
    
    # Add each signal
    for i, signal in enumerate(signals, 1):
        signal_msg = """
### {i}. {name} ({market}{symbol})
- **💰 价格**: {price}元
- **📈 涨幅**: {change:+.2f}%
- **📊 成交量**: {volume:,.0f}手
- **🎯 置信度**: {confidence:.1%}
- **🕒 时间**: {timestamp}

---
""".format(
            i=i,
            name=signal['name'],
            market=signal['market'],
            symbol=signal['symbol'],
            price=signal['price'],
            change=signal['change'],
            volume=signal['volume'],
            confidence=signal['confidence'],
            timestamp=signal['timestamp']
        )
        message += signal_msg
    
    # Add footer
    message += """
⚠️ **请用户确认是否执行交易操作**

---
*监控时间: {}
*数据源: 东方财富*
*系统: Trading Monitor v1.0*
*置信度阈值: ≥95%*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return message


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_dingtalk_alert.py <message>")
        print("\nEnvironment variables:")
        print("  DINGTALK_WEBHOOK_URL - DingTalk webhook URL")
        print("  DINGTALK_SECRET      - Secret key (optional)")
        sys.exit(1)
    
    message = sys.argv[1]
    webhook_url = os.environ.get('DINGTALK_WEBHOOK_URL')
    secret = os.environ.get('DINGTALK_SECRET')
    
    if not webhook_url:
        print("❌ Error: DingTalk webhook URL not provided")
        print("   Set DINGTALK_WEBHOOK_URL environment variable")
        sys.exit(1)
    
    print(f"📤 Sending alert to DingTalk...")
    print(f"   Webhook: {webhook_url[:30]}...")
    
    result = send_dingtalk_alert(webhook_url, message, secret)
    
    # Print result
    if 'errcode' in result and result['errcode'] == 0:
        print("✓ Alert sent successfully")
        print(f"   Message ID: {result.get('msgId', 'N/A')}")
    else:
        print(f"❌ Failed to send alert")
        print(f"   Response: {result}")


if __name__ == "__main__":
    main()
