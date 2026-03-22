#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股S1信号监控脚本 - 10:00盘中扫描
使用 akshare 获取A股实时数据（ fixes for network issues）
"""

import akshare as ak
import pandas as pd
import sys
import os
from datetime import datetime
import time
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

# 找到 SEND_DINGTALK_URL 环境变量
SEND_DINGTALK_URL = os.environ.get("SEND_DINGTALK_URL", "")

def get_stock_realtime_data():
    """
    使用 akshare 获取A股实时数据
    数据源：东方财富 - 基金持仓数据（备用）
    """
    try:
        print(">正在尝试获取A股实时数据...")
        
        # 方法1: 使用东方财富股票实时数据（带重试）
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # 设置超时
        timeout = (10, 30)  # 连接超时10秒，读取超时30秒
        
        # 尝试股票实时数据
        try:
            print("  [1/3] 尝试东方财富股票实时数据...")
            # 首先测试连接
            response = session.get("https://push2.eastmoney.com/api/qt/clist/get", 
                                 params={"pn": 1, "pz": 10, "po": 1, "np": 1, 
                                         "fltt": 2, "invt": 2, "fid": "f3", 
                                         "fs": "m:0 t:6,m:0 t:80,m:1 t:2", 
                                         "fields": "f12,f14,f2,f3,f124,f128,f136,f115,f152",
                                         "_": str(int(time.time() * 1000))},
                                 headers={"User-Agent": "Mozilla/5.0"},
                                 timeout=15)
            
            if response.status_code == 200 and "data" in response.text:
                data = ak.stock_zh_a_spot_em()
                if not data.empty:
                    print(f"✅ 成功获取 {len(data)} 只A股数据")
                    return data
        except Exception as e:
            print(f"  东方财富实时数据失败: {e}")
        
        # 方法2: 使用同花顺数据（备用）
        try:
            print("  [2/3] 尝试同花顺数据...")
            data = ak.stock_zh_a_spot()
            if not data.empty:
                print(f"✅ 成功获取 {len(data)} 只A股数据")
                return data
        except Exception as e:
            print(f"  同花顺数据失败: {e}")
        
        # 方法3: 使用历史数据作为替代
        print("  [3/3] 回退到历史数据模式...")
        try:
            # 获取近期涨幅靠前的股票作为代理
            stock_info = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                                           start_date="20260301", end_date="20260318")
            if not stock_info.empty:
                print(f"✅ 获取历史数据成功，共 {len(stock_info)} 条")
                # 从历史数据中提取最后几日的数据作为参考
                recent = stock_info.tail(10).copy()
                recent['股票代码'] = '000001'
                recent['股票名称'] = '平安银行'
                print(f"⚠️ 使用历史数据代替实时数据，数据时效性可能降低")
                return recent
        except Exception as e:
            print(f"  历史数据获取失败: {e}")
        
        print("❌ 所有数据源获取失败")
        return None
        
    except Exception as e:
        print(f"❌ 获取数据异常: {e}")
        return None

def calculate_s1_signal(row):
    """
    计算S1信号强度（简化版多因子模型）
    S1级别：≥95% 强信号
    """
    try:
        score = 0
        factors = []
        
        # 因子1：价格贴近最高价（25分）
        if '最新价' in row and '最高' in row:
            latest = float(row['最新价']) if pd.notna(row['最新价']) else 0
            high = float(row['最高']) if pd.notna(row['最高']) else 0
            if high > 0 and latest >= high * 0.98:
                score += 25
                factors.append(f"新高>98%({latest:.2f}/{high:.2f})")
        
        # 因子2：成交量/成交额放大（25分）
        if '成交额' in row:
            amount = float(row['成交额']) if pd.notna(row['成交额']) else 0
            if amount > 5000:  # 成交额>5000万
                score += 25
                factors.append(f"成交>{int(amount/10000)}万")
        
        # 因子3：涨幅排名（20分）
        if '涨跌幅' in row:
            change = float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0
            if change >= 9.5:  # 接近涨停
                score += 20
                factors.append(f"涨幅{change:.2f}%")
            elif change >= 5.0:
                score += 15
                factors.append(f"涨幅{change:.2f}%")
        
        # 因子4：主力资金（20分）
        if '主力净流' in row:
            net_flow = float(row['主力净流']) if pd.notna(row['主力净流']) else 0
            if net_flow > 1000:  # 主力净流入>1000万
                score += 20
                factors.append(f"主流入>1000万")
        
        # 因子5：基础分（10分）
        score += 10
        factors.append("基础形态")
        
        # 信号强度百分比
        signal_strength = min(score, 100)
        
        return signal_strength, factors
        
    except Exception as e:
        return 0, [f"计算错误:{e}"]

def scan_s1_signals(df):
    """
    扫描S1级别强信号（≥95%）
    """
    if df is None or df.empty:
        print("❌ 数据为空")
        return pd.DataFrame()
    
    print(f"📊 数据列: {df.columns.tolist()}")
    
    results = []
    
    for idx, row in df.iterrows():
        try:
            strength, factors = calculate_s1_signal(row)
            
            if strength >= 95:
                stock_info = {
                    '代码': row.get('代码', row.get('股票代码', row.get('f12', ''))),
                    '名称': row.get('名称', row.get('股票名称', row.get('f14', ''))),
                    '最新价': row.get('最新价', 0),
                    '涨跌幅': row.get('涨跌幅', 0),
                    '信号强度': strength,
                    '因素': ';'.join(factors)
                }
                results.append(stock_info)
                print(f"  👉 发现S1信号: {stock_info['名称']} 强度={strength}%")
                
        except Exception as e:
            continue
    
    if not results:
        print("⏳ 未发现S1级别信号（≥95%）")
        return pd.DataFrame()
    
    result_df = pd.DataFrame(results)
    # 按信号强度排序
    result_df = result_df.drop_duplicates()
    result_df = result_df.sort_values('信号强度', ascending=False)
    
    print(f"✅ 共发现 {len(results)} 只S1信号股票")
    return result_df

def format_signal_report(df):
    """
    格式化信号报告
    """
    if df.empty:
        return "📈【A股S1信号监控】\n\n⏳ 未发现S1级别强信号（≥95%）"
    
    report = []
    report.append("📈【A股S1信号监控】")
    report.append(f"⏰ 扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"📊 发现信号: {len(df)} 只")
    report.append("-" * 40)
    
    for idx, row in df.iterrows():
        report.append(f"\n🎯 {row['代码']} {row['名称']}")
        report.append(f"   💰 价格: {row['最新价']:.2f}  /  涨幅: {row['涨跌幅']:.2f}%")
        report.append(f"   📈 强度: {row['信号强度']}%")
        report.append(f"   💡 因素: {row['因素']}")
    
    report.append("\n" + "=" * 40)
    report.append("讯: 信号强度 ≥95% 为S1级别强信号")
    report.append("待: 等待用户确认...")
    
    return "\n".join(report)

def send_to_dingtalk(message):
    """
    发送到钉钉群
    """
    if not SEND_DINGTALK_URL:
        print("⚠️ 未配置 SEND_DINGTALK_URL，跳过发送")
        return False
    
    try:
        import requests
        headers = {'Content-Type': 'application/json'}
        data = {
            "msgtype": "text",
            "text": {"content": message}
        }
        response = requests.post(SEND_DINGTALK_URL, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ 钉钉消息发送成功")
            return True
        else:
            print(f"❌ 钉钉发送失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False

def main():
    print("=" * 50)
    print("🔍 A股S1信号监控 - 启动")
    print("=" * 50)
    
    # 1. 获取实时数据
    df = get_stock_realtime_data()
    if df is None:
        print("⚠️ 数据获取失败，退出")
        return
    
    # 2. 扫描S1信号
    print("\n🔍 正在扫描S1级别信号（≥95%）...")
    s1_signals = scan_s1_signals(df)
    
    # 3. 生成报告
    report = format_signal_report(s1_signals)
    print("\n" + report)
    
    # 4. 发送到钉钉
    print("\n📤 发送钉钉通知...")
    send_to_dingtalk(report)
    
    print("\n✅ 监控完成")

if __name__ == "__main__":
    main()
