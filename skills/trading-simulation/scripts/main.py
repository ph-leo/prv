#!/usr/bin/env python3
"""
A股模拟操盘系统 - 主程序
集成信号扫描、模拟交易、盈亏报告
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加引用目录
script_dir = os.path.dirname(os.path.abspath(__file__))
refs_dir = os.path.join(script_dir, '..', 'refs')
sys.path.insert(0, refs_dir)

from akshare_stock_indicators import (
    calculate_signal_strength,
    scan_market_for_signals,
    classify_signal_strength
)
from simulation_engine import (
    TradingSimulation,
    create_signal_message
)


def initialize_simulation():
    """初始化模拟交易"""
    sim = TradingSimulation(initial_capital=50000)
    sim.start_simulation()
    return sim


def scan_and_display_signals():
    """扫描并展示信号"""
    print("\n=== 正在扫描A股信号 ===")
    signals = scan_market_for_signals()
    
    if not signals:
        print("未发现任何信号")
        return []
    
    print(f"\n共发现 {len(signals)} 个信号")
    
    # 分类显示
    s1_signals = [s for s in signals if s['signal_strength'] >= 95]
    s2_signals = [s for s in signals if 85 <= s['signal_strength'] < 95]
    s3_signals = [s for s in signals if 70 <= s['signal_strength'] < 85]
    
    print(f"\nS1级别信号 (≥95%): {len(s1_signals)} 个")
    for s in s1_signals:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        msg = create_signal_message(s)
        print(f"\n{msg}")
    
    if not s1_signals:
        print("未发现S1级别信号")
    
    return s1_signals


def execute_simulation():
    """执行完整的模拟交易流程"""
    print("=" * 60)
    print("🌟 A股模拟操盘系统 (5万元) 🌟")
    print("=" * 60)
    
    try:
        # 初始化
        sim = initialize_simulation()
        
        # 扫描信号
        s1_signals = scan_and_display_signals()
        
        # 模拟交易执行
        if s1_signals:
            print("\n=== 模拟交易执行 ===")
            # 取最强的一个信号执行
            best_signal = s1_signals[0]
            price = best_signal['price']
            shares = int(50000 / price / 100) * 100  # 买100的整数倍
            
            if shares > 0 and price * shares <= 50000:
                sim.buy_stock(
                    best_signal['code'],
                    best_signal['name'],
                    price,
                    shares,
                    "S1信号自动执行"
                )
            else:
                print("无法执行交易（资金不足或股数不足）")
        else:
            print("\n无S1信号，不执行交易")
        
        # 模拟10天后的情况（简化模拟）
        print("\n=== 模拟10天后盈亏报告 ===")
        report = sim.get_profit_report()
        
        print(f"\n📊 模拟交易报告")
        print(f"{'=' * 40}")
        print(f"初始资金: ¥{report['initial_capital']:,.2f}")
        print(f"当前市值: ¥{report['current_value']:,.2f}")
        print(f"总收益: ¥{report['total_profit']:,.2f} ({report['profit_pct']:+.2f}%)")
        print(f"交易次数: {report['total_trades']}")
        if report['total_trades'] > 0:
            print(f"胜率: {report['win_rate']:.2f}%")
        print(f"交易天数: {report['trading_days']}")
        
        # 打印持仓
        sim.print_position_summary()
        
        print("\n" + "=" * 60)
        print("模拟交易结束")
        print("=" * 60)
        
        return report
    except Exception as e:
        print(f"模拟执行失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("A股模拟操盘 - 启动")
    print("=" * 60)
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"模拟资金: 50,000元")
    print(f"信号频率: 每日开盘扫描")
    print("=" * 60)
    
    # 执行模拟
    report = execute_simulation()
    
    if report:
        # 返回状态码
        return 0
    else:
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户取消")
        sys.exit(1)
