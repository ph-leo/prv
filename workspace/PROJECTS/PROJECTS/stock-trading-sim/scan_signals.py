#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股模拟操盘脚本 - S1强信号扫描
"""

import akshare as ak
import pandas as pd
import sys
import time

def fetch_stock_data():
    """获取A股实时行情数据"""
    try:
        print("正在获取A股实时行情数据...")
        stock_zh_a_spot_em = ak.stock_zh_a_spot_em()
        return stock_zh_a_spot_em
    except Exception as e:
        print(f"❌ 数据获取失败: {e}")
        return None

def scan_strong_signals(df):
    """扫描S1级别强信号 (涨幅 ≥ 9.5%)"""
    if df is None or df.empty:
        return pd.DataFrame()
    
    # 筛选条件
    # 主板: 涨幅 >= 9.5%
    # 创业板/科创板: 涨幅 >= 15%
    strong_signals = df[
        (df['涨跌幅'] >= 9.5) | 
        (df['代码'].str.startswith('30') & (df['涨跌幅'] >= 15)) |
        (df['代码'].str.startswith('68') & (df['涨跌幅'] >= 15))
    ]
    
    return strong_signals

def display_signals(signals):
    """显示强信号股票"""
    if signals.empty:
        print("\n⚠️ 当前无S1级别强信号股票")
        return
    
    print(f"\n✅ 发现 {len(signals)} 只强信号股票:")
    print("-" * 80)
    
    for _, stock in signals.iterrows():
        code = stock['代码']
        name = stock['名称']
        price = stock['最新价']
        change = stock['涨跌幅']
        volume = stock['成交量']
        amount = stock['成交额']
        
        print(f"  {code} {name}")
        print(f"    涨幅: {change:.2f}% | 价格: {price:.2f}元")
        print(f"    成交量: {volume} | 成交额: {amount}")
        print("-" * 80)

def main():
    print("=" * 80)
    print("🚀 A股模拟操盘 - S1强信号扫描")
    print("⏰ 时间: 2026-03-26 09:30")
    print("💰 模拟资金: 50,000 元")
    print("=" * 80)
    
    # 获取数据
    df = fetch_stock_data()
    
    if df is not None:
        # 扫描强信号
        signals = scan_strong_signals(df)
        
        # 显示结果
        display_signals(signals)
        
        # 保存到CSV
        if not signals.empty:
            signals.to_csv('/root/.openclaw/workspace/PROJECTS/stock-trading-sim/strong_signals_20260326.csv', index=False, encoding='utf-8-sig')
            print("\n✅ 信号数据已保存到: PROJECTS/stock-trading-sim/strong_signals_20260326.csv")
    else:
        print("\n⚠️ 数据获取失败，跳过今日扫描")
        sys.exit(1)

if __name__ == "__main__":
    main()
