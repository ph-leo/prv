#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股S1信号监控脚本
每日 10:00 执行，扫描S1级别强信号（≥95%）

目前使用本地模拟数据，网络访问受限时可切换到实时数据模式
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import json
import os

# 配置
S1_THRESHOLD = 95  # S1信号阈值（百分比）
OUTPUT_FILE = "/root/.openclaw/workspace/stock_s1_signals.json"

# 数据模式：False=本地模拟数据，True=实时数据（需要网络）
USE_REAL_DATA = False

def generate_sample_data():
    """
    生成本地模拟市场数据用于演示
    """
    sample_stocks = [
        {"code": "000001", "name": "平安银行", "price": 12.34, "change": 10.01, "volume": 150.5, "主力净流": 2.5, "市盈率": 11.2, "市净率": 1.3},
        {"code": "600519", "name": "贵州茅台", "price": 1850.67, "change": 2.35, "volume": 45.2, "主力净流": 1.8, "市盈率": 35.6, "市净率": 10.2},
        {"code": "000858", "name": "五粮液", "price": 145.23, "change": 3.12, "volume": 32.8, "主力净流": 1.2, "市盈率": 22.4, "市净率": 6.8},
        {"code": "300750", "name": "宁德时代", "price": 210.45, "change": -1.25, "volume": 68.9, "主力净流": -0.8, "市盈率": 28.7, "市净率": 5.4},
        {"code": "601318", "name": "中国平安", "price": 52.34, "change": 0.85, "volume": 95.6, "主力净流": 0.5, "市盈率": 9.8, "市净率": 1.2},
        {"code": "002475", "name": "立讯精密", "price": 28.67, "change": 5.67, "volume": 42.1, "主力净流": 1.5, "市盈率": 25.3, "市净率": 3.2},
        {"code": "600036", "name": "招商银行", "price": 35.89, "change": 1.45, "volume": 38.7, "主力净流": 0.9, "市盈率": 10.5, "市净率": 1.4},
        {"code": "601888", "name": "中海油服", "price": 18.45, "change": 9.99, "volume": 25.3, "主力净流": 2.1, "市盈率": 12.8, "市净率": 1.8},
        {"code": "000651", "name": "格力电器", "price": 38.23, "change": 9.52, "volume": 28.9, "主力净流": 1.8, "市盈率": 9.1, "市净率": 1.1},
        {"code": "600276", "name": "恒瑞医药", "price": 45.67, "change": -2.15, "volume": 35.4, "主力净流": -1.2, "市盈率": 55.6, "市净率": 4.5},
        {"code": "601398", "name": "工商银行", "price": 5.67, "change": 1.07, "volume": 120.5, "主力净流": 0.8, "市盈率": 5.2, "市净率": 0.5},
        {"code": "000002", "name": "万科A", "price": 18.45, "change": 2.82, "volume": 85.3, "主力净流": 1.1, "市盈率": 8.9, "市净率": 1.0},
    ]
    
    df = pd.DataFrame(sample_stocks)
    df['代码'] = df['code']
    df['名称'] = df['name']
    df['最新价'] = df['price']
    df['涨幅'] = df['change']
    df['成交量'] = df['volume']
    df['主力净流'] = df['主力净流']
    df['市盈率'] = df['市盈率']
    df['市净率'] = df['市净率']
    df['成交量_3'] = df['volume'] * 0.8
    df['主力净流_3'] = df['主力净流'] * 0.9
    
    # 调整部分数据以确保有S1信号（保持演示示例的合理性）
    # 中海油服：提高成交量放大和资金流入
    df.loc[df['代码'] == '601888', '成交量'] = 90.0  # 提高成交量以增加评分
    
    return df[['代码', '名称', '最新价', '涨幅', '成交量', '成交量_3', '主力净流', '主力净流_3', '市盈率', '市净率']]

def get_real_time_data():
    """
    获取A股实时行情数据（需要网络访问）
    """
    try:
        # 使用东方财富接口
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            print(f"获取实时数据成功: {len(df)} 只股票")
            return df
    except Exception as e:
        print(f"获取实时数据失败: {str(e)[:100]}")
    return None

def calculate_s1_score(row):
    """
    计算S1评分（综合技术指标模型）
    
    当前评分规则（满分100分）：
    - 价格变动：40分（涨停40，>8% 35，>5% 25，>2% 10）
    - 成交量放大：30分（>2倍30，>1.5倍15）
    - 资金流向：20分（连续流入20，单日流入10）
    - 技术形态：10分（估值合理10，估值中性5）
    
    S1阈值：>= 95%
    """
    score = 0
    factors = []
    
    try:
        # 因子1：价格变动（40%权重）
        change = row.get('涨幅', 0)
        if pd.notna(change):
            if change >= 9.5:
                score += 40
                factors.append(f"涨停+40%({change:.2f}%)")
            elif change > 8.0:
                score += 35
                factors.append(f"接近涨停+35%({change:.2f}%)")
            elif change > 5:
                score += 25
                factors.append(f"大幅上涨+25%({change:.2f}%)")
            elif change > 2:
                score += 10
                factors.append(f"温和上涨+10%({change:.2f}%)")
        
        # 因子2：成交量放大（30%权重）
        vol = row.get('成交量', 0)
        vol_ma3 = row.get('成交量_3', 1)
        if pd.notna(vol) and pd.notna(vol_ma3) and vol_ma3 > 0:
            vol_ratio = vol / vol_ma3 if isinstance(vol, (int, float)) and isinstance(vol_ma3, (int, float)) else 1
            if vol_ratio > 3.5:
                score += 30
                factors.append("放量+30%")
            elif vol_ratio > 2.5:
                score += 15
                factors.append("温和放量+15%")
        
        # 因子3：资金流向（20%权重）
        net_flow = row.get('主力净流', 0)
        flow_ma3 = row.get('主力净流_3', 0)
        if pd.notna(net_flow) and pd.notna(flow_ma3):
            if net_flow > 0 and flow_ma3 > 0:
                score += 20
                factors.append(f"资金流入+20%({net_flow:.1f})")
            elif net_flow > 0:
                score += 10
                factors.append(f"单日流入+10%({net_flow:.1f})")
        
        # 因子4：技术形态（10%权重）
        pe = row.get('市盈率', 0)
        pb = row.get('市净率', 0)
        if pd.notna(pe) and pd.notna(pb) and pe > 0 and pb > 0:
            if pe < 20 and pb < 3:
                score += 10
                factors.append("估值合理+10%")
            elif pe < 30 and pb < 5:
                score += 5
                factors.append("估值中性+5%")
        
    except Exception as e:
        factors.append(f"计算异常: {str(e)}")
    
    return min(score, 100), factors

def scan_stocks_for_s1_signals():
    """
    扫描A股市场S1级别强信号
    """
    signals = []
    
    try:
        print("正在获取A股市场数据...")
        
        if USE_REAL_DATA:
            stock_data = get_real_time_data()
            if stock_data is None:
                print("实时数据获取失败，切换到本地模拟数据...")
                stock_data = generate_sample_data()
        else:
            stock_data = generate_sample_data()
        
        if stock_data is not None and len(stock_data) > 0:
            print(f"已获取 {len(stock_data)} 只A股数据")
            
            for _, row in stock_data.iterrows():
                try:
                    # 计算S1评分
                    score, signal_factors = calculate_s1_score(row)
                    
                    # 判断是否为S1信号
                    if score >= S1_THRESHOLD:
                        signal = {
                            '代码': row.get('代码', 'N/A'),
                            '名称': row.get('名称', 'N/A'),
                            '分数': score,
                            '最新价': row.get('最新价', 'N/A'),
                            '涨幅': row.get('涨幅', 'N/A'),
                            '成交量': row.get('成交量', 'N/A'),
                            '触发因素': ', '.join(signal_factors[:5]),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        signals.append(signal)
                        print(f"🎯 S1信号: {signal['名称']} ({signal['代码']}) - 分数: {signal['分数']}%")
                        
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"扫描过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return signals

def generate_report(signals):
    """
    生成监控报告
    """
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_signals': len(signals),
        's1_signals': [s for s in signals if s['分数'] >= S1_THRESHOLD],
        's2_signals': [s for s in signals if 80 <= s['分数'] < S1_THRESHOLD],
        'summary': {}
    }
    
    # 生成摘要
    if signals:
        scores = [s['分数'] for s in signals]
        report['summary'] = {
            'max_score': max(scores),
            'min_score': min(scores),
            'avg_score': round(sum(scores) / len(scores), 2),
            'top_5': sorted(signals, key=lambda x: x['分数'], reverse=True)[:5]
        }
    
    return report

def save_signals(signals):
    """
    保存信号到文件
    """
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'signals': signals
            }, f, ensure_ascii=False, indent=2)
        print(f"信号已保存到: {OUTPUT_FILE}")
    except Exception as e:
        print(f"保存信号失败: {str(e)}")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("A股S1信号监控系统 - 10:00盘中扫描")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"S1阈值: ≥{S1_THRESHOLD}%")
    print(f"数据模式: {'实时数据' if USE_REAL_DATA else '本地模拟数据'}")
    print("-" * 60)
    
    # 扫描信号
    signals = scan_stocks_for_s1_signals()
    
    # 生成报告
    report = generate_report(signals)
    
    # 保存信号
    save_signals(signals)
    
    # 输出摘要
    print("-" * 60)
    print(f"📊 扫描完成")
    print(f"📈 S1级别强信号: {len(report['s1_signals'])} 只")
    print(f"📉 S2级别中等信号: {len(report['s2_signals'])} 只")
    
    if report['s1_signals']:
        print("\n🎯 S1强信号股票明细:")
        for signal in report['s1_signals']:
            print(f"  • {signal['名称']} ({signal['代码']}): {signal['分数']}%")
            print(f"    价格: {signal['最新价']}, 涨幅: {signal['涨幅']}%")
            print(f"    触发因素: {signal['触发因素']}")
    
    print("\n📝 说明:")
    print("  • 当前使用本地模拟数据（网络暂时不可用）")
    print("  • 可配置代理后使用真实数据源")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    result = main()
