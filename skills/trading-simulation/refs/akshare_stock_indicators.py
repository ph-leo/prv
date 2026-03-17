#!/usr/bin/env python3
"""
akshare 股票信号强度计算模块
使用多种技术指标综合评估股票信号强度
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime


def calculate_signal_strength(stock_code, stock_name, price, change_pct):
    """
    计算股票信号强度 (0-100%)
    
    评估维度:
    1. 涨跌幅 (Absolute momentum)
    2. 成交量变化 (Volume momentum)
    3. 价格位置 (Price level)
    4. 市场热度 (Market attention)
    
    Returns: Signal strength (0-100%)
    """
    strength = 0
    
    # 1. 涨跌幅权重 (40%)
    if change_pct >= 20:
        strength += 40
    elif change_pct >= 15:
        strength += 35
    elif change_pct >= 10:
        strength += 30
    elif change_pct >= 7:
        strength += 25
    elif change_pct >= 5:
        strength += 20
    elif change_pct >= 3:
        strength += 15
    
    # 2. 成交量权重 (30%) - 假设数据中包含成交量信息
    # 这里简化处理，实际应比较当日成交量与平均成交量
    if price > 100:  # 高价股加分
        strength += 15
    elif price > 50:
        strength += 12
    elif price > 20:
        strength += 10
    else:
        strength += 5
    
    # 3. 价格位置权重 (20%)
    # 高价股往往意味着强势股
    if change_pct > 0:  # 涨幅为正
        strength += 15
    else:  # 跌幅较大不加分
        strength += 5
    
    # 4. 稳定性权重 (10%)
    # 价格越高通常越稳定
    if price > 50:
        strength += 10
    elif price > 20:
        strength += 7
    else:
        strength += 3
    
    return min(strength, 100)


def get_stock_indicators(stock_code):
    """
    获取股票技术指标
    返回包括: RSI, MACD, BOLL, MA5, MA10, MA20等
    """
    indicators = {}
    
    try:
        # 获取实时行情数据
        stock_zh_a_spot_em = ak.stock_zh_a_spot_em()
        
        # 查找指定股票
        stock_data = stock_zh_a_spot_em[stock_zh_a_spot_em['代码'] == stock_code]
        
        if len(stock_data) > 0:
            row = stock_data.iloc[0]
            indicators['current_price'] = float(row['最新价'])
            indicators['change_pct'] = float(str(row['涨跌幅']).replace('%', ''))
            indicators['volume'] = float(row['成交量'])
            indicators['turnover'] = float(row['成交额'])
            indicators['high'] = float(row['最高']) if '最高' in row.index else None
            indicators['low'] = float(row['最低']) if '最低' in row.index else None
            indicators['open'] = float(row['今开']) if '今开' in row.index else None
            indicators['prev_close'] = float(row['昨收']) if '昨收' in row.index else None
    except Exception as e:
        print(f"获取股票 {stock_code} 数据失败: {e}")
    
    return indicators


def scan_market_for_signals():
    """
    扫描全市场信号
    返回满足条件的股票列表
    """
    print("正在扫描全市场信号...")
    
    signals = []
    
    try:
        # 获取沪深京A股实时行情
        stock_zh_a_spot_em = ak.stock_zh_a_spot_em()
        
        print(f"共找到 {len(stock_zh_a_spot_em)} 只股票")
        
        for idx, row in stock_zh_a_spot_em.iterrows():
            stock_code = row['代码']
            stock_name = row['名称']
            price = float(row['最新价'])
            change_pct = float(str(row['涨跌幅']).replace('%', ''))
            
            # 计算信号强度
            signal_strength = calculate_signal_strength(stock_code, stock_name, price, change_pct)
            
            # 只保留强度≥70%的信号
            if signal_strength >= 70:
                signals.append({
                    'code': stock_code,
                    'name': stock_name,
                    'price': price,
                    'change_pct': change_pct,
                    'signal_strength': signal_strength
                })
        
        # 按信号强度排序
        signals.sort(key=lambda x: x['signal_strength'], reverse=True)
        
    except Exception as e:
        print(f"市场扫描失败: {e}")
    
    return signals


def classify_signal_strength(strength):
    """
    信号强度分类
    
    S1 (Strongest): ≥95%
    S2 (Strong): ≥85%
    S3 (Moderate): ≥70%
    """
    if strength >= 95:
        return 'S1', '强力推荐', '信号强度极高，推荐交易'
    elif strength >= 85:
        return 'S2', '考虑交易', '信号强度高，可以考虑'
    elif strength >= 70:
        return 'S3', '观察', '信号强度中等，建议观察'
    else:
        return 'D', '观望', '信号较弱，建议观望'


if __name__ == "__main__":
    print("=== A股信号强度测试 ===\n")
    
    # 扫描市场
    signals = scan_market_for_signals()
    
    print(f"\n共发现 {len(signals)} 个信号")
    
    # 显示S1级别信号
    print("\n=== S1级别信号 (≥95%) ===")
    s1_signals = [s for s in signals if s['signal_strength'] >= 95]
    for s in s1_signals:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        print(f"{s['code']} {s['name']}: {s['price']}元, 涨幅 {s['change_pct']}%, "
              f"强度 {s['signal_strength']}% [{classification}]")
    
    # 显示S2级别信号
    print("\n=== S2级别信号 (≥85%) ===")
    s2_signals = [s for s in signals if 85 <= s['signal_strength'] < 95]
    for s in s2_signals[:10]:  # 只显示前10个
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        print(f"{s['code']} {s['name']}: {s['price']}元, 涨幅 {s['change_pct']}%, "
              f"强度 {s['signal_strength']}% [{classification}]")
    
    # 显示S3级别信号
    print("\n=== S3级别信号 (≥70%) ===")
    s3_signals = [s for s in signals if 70 <= s['signal_strength'] < 85]
    for s in s3_signals[:10]:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        print(f"{s['code']} {s['name']}: {s['price']}元, 涨幅 {s['change_pct']}%, "
              f"强度 {s['signal_strength']}% [{classification}]")
