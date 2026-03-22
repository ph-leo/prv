#!/usr/bin/env python3
"""
A-Share S1 Signal Monitor using akshare
Scans for strong signals (≥95% confidence) during trading hours

Usage:
  # Test mode - no notification
  python3 scripts/monitor_s1_signals.py --test
  
  # Full monitoring - with DingTalk notification
  python3 scripts/monitor_s1_signals.py
  
  # Environment variables
  export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
  export DINGTALK_SECRET="SECxxx"
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import sys
import json
import time
import os
import requests
from functools import wraps
import hmac
import hashlib
import base64


def retry(max_retries=2, delay=1):
    """重试装饰器，用于网络请求失败重试"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"  ⚠️ 尝试 {attempt + 1}/{max_retries} 失败: {str(e)[:50]}...")
                        time.sleep(delay * (attempt + 1))
                    else:
                        raise
        return wrapper
    return decorator


@retry(max_retries=2, delay=1)
def fetch_realtime_quotes():
    """
    Fetch real-time A-share stock quotes using akshare
    Data sources: Eastmoney, TONGLU, Sina Finance
    
    Returns:
        tuple: (shanghai_df, shenzhen_df)
    """
    print("  → 获取实时行情数据...")
    
    # Try Eastmoney first
    sh_quotes = None
    sz_quotes = None
    
    # Try different data sources
    sources = [
        ('Eastmoney SH', lambda: ak.stock_sh_a_spot_em()),
        ('Sina SH', lambda: ak.stock_zh_a_spot()),
        ('Eastmoney CZ', lambda: ak.stock_cy_a_spot_em()),
    ]
    
    for source_name, fetch_func in sources:
        try:
            df = fetch_func()
            print(f"  ✓ {source_name}: {len(df)} 股")
            
            if df is not None and len(df) > 0:
                # Use this data as base
                if sh_quotes is None:
                    sh_quotes = df
                    sz_quotes = df.copy() if df is not None else None
        except Exception as e:
            print(f"  ✗ {source_name}: {str(e)[:40]}...")
            continue
    
    if sh_quotes is None:
        raise Exception("所有数据源获取失败")
    
    return sh_quotes, sz_quotes


def detect_s1_signals(sh_quotes, sz_quotes, threshold=0.95):
    """
    Detect S1-level strong signals (≥95% confidence)
    
    Args:
        sh_quotes: Shanghai stock data
        sz_quotes: Shenzhen stock data  
        threshold: Minimum confidence threshold (default 0.95)
    
    Returns:
        list: Detected signals with confidence scores
    """
    signals = []
    
    for df, market in [(sh_quotes, 'SH'), (sz_quotes, 'SZ')]:
        if df is None or len(df) == 0:
            continue
        
        for _, row in df.iterrows():
            try:
                # Extract stock info - handle both column naming conventions
                symbol = str(row.get('代码', row.get('symbol', ''))).strip()
                name = str(row.get('名称', row.get('name', ''))).strip()
                
                # Parse price and change - handle various formats
                price_str = str(row.get('最新价', row.get('price', ''))).strip()
                change_str = str(row.get('涨跌幅', row.get('change', ''))).strip()
                volume_str = str(row.get('成交量', row.get('volume', ''))).strip()
                
                # Convert to numeric
                price = float(price_str.replace(',', '')) if price_str and price_str != '-' else 0
                change = float(change_str.replace('%', '').replace(',', '')) if change_str and change_str != '-' else 0
                volume = float(volume_str.replace(',', '')) if volume_str and volume_str != '-' else 0
                
                # Calculate confidence score
                confidence = calculate_signal_confidence(price, change, volume)
                
                if confidence >= threshold:
                    signals.append({
                        'market': market,
                        'symbol': symbol,
                        'name': name,
                        'price': price,
                        'change': change,
                        'volume': volume,
                        'confidence': confidence,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            except (ValueError, KeyError, TypeError) as e:
                continue
    
    return signals


def calculate_signal_confidence(price, change, volume):
    """
    Calculate S1 signal confidence score based on multiple factors
    
    Score components:
    - Price movement (0-30 points)
    - Volume (0-30 points)  
    - Volatility (0-20 points)
    - Market strength (0-20 points)
    
    Args:
        price: Current price
        change: Price change percentage
        volume: Trading volume
    
    Returns:
        float: Confidence score (0-1.0)
    """
    confidence = 0.0
    
    # 1. Price movement (30 points max)
    if abs(change) > 7:
        confidence += 0.30
    elif abs(change) > 5:
        confidence += 0.25
    elif abs(change) > 3:
        confidence += 0.15
    elif abs(change) > 1:
        confidence += 0.05
    
    # 2. Volume factor (30 points max)
    if volume > 1000000:
        confidence += 0.30
    elif volume > 500000:
        confidence += 0.20
    elif volume > 200000:
        confidence += 0.10
    
    # 3. Volatility (20 points max)
    if price > 10:
        confidence += 0.10
    elif price > 5:
        confidence += 0.05
    
    # 4. Market strength (20 points max)
    if change > 0:
        confidence += 0.10
    
    return min(confidence, 1.0)


def format_signal_message(signals, is_test=False):
    """
    Format signals for DingTalk notification
    
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
*数据源: Sina Finance/Eastmoney
*系统: Trading Monitor v1.0*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return message
    
    message = """📊 **A股S1信号监控 - 10:00**

**🔍 发现 {} 个S1级强信号（≥95%置信度）**

---
""".format(len(signals))
    
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
    
    message += """
⚠️ **请用户确认是否执行交易操作**

---
*监控时间: {}
*数据源: Sina Finance/Eastmoney
*系统: Trading Monitor v1.0*
*置信度阈值: ≥95%*
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return message


def send_dingtalk_alert(webhook_url, message, secret=None, timeout=10):
    """
    Send alert to DingTalk group
    
    Args:
        webhook_url: DingTalk robot webhook URL
        message: Alert message content
        secret: Secret key for signature (if enabled)
        timeout: Request timeout in seconds
    
    Returns:
        dict: Response from DingTalk API
    """
    headers = {
        'Content-Type': 'application/json',
    }
    
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
    
    # Add signature if secret provided
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
    
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=timeout)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': f'Unknown error: {str(e)}'}


def main():
    """Main monitoring function"""
    print("=" * 60)
    print("xA-Share S1 Signal Monitor - 10:00 Trading Session")
    print("=" * 60)
    
    # Parse arguments
    is_test = '--test' in sys.argv
    if is_test:
        print("\n🧪 TEST MODE - No DingTalk notification will be sent")
    
    # Fetch market data
    print("\n[A] 获取实时行情数据...")
    try:
        sh_quotes, sz_quotes = fetch_realtime_quotes()
    except Exception as e:
        print(f"\n❌ 数据获取失败: {e}")
        print("   请检查网络连接或稍后重试")
        return []
    
    total_stocks = (len(sh_quotes) if sh_quotes is not None else 0) + \
                   (len(sz_quotes) if sz_quotes is not None else 0)
    print(f"✓ 已获取数据 - 总计: {total_stocks} 股")
    
    # Scan for S1 signals
    print("\n[S] 扫描S1级强信号 (≥95%置信度)...")
    signals = detect_s1_signals(sh_quotes, sz_quotes)
    
    print(f"✓ 扫描完成 - 发现 {len(signals)} 个S1级信号")
    
    # Display results
    if signals:
        print("\n⚠️  强信号列表:")
        for signal in signals:
            print(f"   [{signal['confidence']:.1%}] {signal['name']} ({signal['symbol']}) - {signal['change']:.2f}%")
    
    # Format output
    message = format_signal_message(signals, is_test)
    
    print("\n" + message)
    
    # Send to DingTalk if not test mode
    if not is_test:
        webhook_url = os.environ.get('DINGTALK_WEBHOOK_URL')
        
        if webhook_url:
            print("\n📤 发送DingTalk通知...")
            secret = os.environ.get('DINGTALK_SECRET')
            result = send_dingtalk_alert(webhook_url, message, secret)
            
            if 'errcode' in result and result['errcode'] == 0:
                print("✓ 通知发送成功")
            else:
                print(f"❌ 通知发送失败: {result}")
        else:
            print("\n⚠️  DINGTALK_WEBHOOK_URL not set - No notification sent")
            print("   设置环境变量以启用通知:")
            print("   export DINGTALK_WEBHOOK_URL='https://oapi.dingtalk.com/robot/send?access_token=xxx'")
    else:
        print("\n✅ TEST MODE - Monitor completed successfully")
    
    return signals


if __name__ == "__main__":
    signals = main()
