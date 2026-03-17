#!/usr/bin/env python3
"""
A股模拟操盘系统 - 交易引擎测试
测试模拟交易引擎的各项功能
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

from simulation_engine import (
    TradingSimulation, 
    create_signal_message,
    classify_signal_strength
)


def test_initialize():
    """测试初始化"""
    print("=== 测试初始化 ===")
    sim = TradingSimulation(initial_capital=50000)
    sim.start_simulation()
    
    assert sim.cash == 50000
    assert len(sim.positions) == 0
    assert len(sim.trades) == 0
    assert sim.trading_days == 0
    
    print("✅ 初始化测试通过")
    return sim


def test_buy_stock(sim):
    """测试买入股票"""
    print("\n=== 测试买入股票 ===")
    
    try:
        # 正常买入
        result = sim.buy_stock("301226", "祥明智能", 41.74, 100, "测试买入")
        assert result == True
        assert sim.cash == 50000 - 4174
        assert "301226" in sim.positions
        assert sim.trading_days == 1
        
        print(f"账户现金: ¥{sim.cash:.2f}")
        print(f"持仓数量: {len(sim.positions)}")
        print(f"交易天数: {sim.trading_days}")
        print("✅ 买入测试通过")
    except Exception as e:
        print(f"买入失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_multiple_trades(sim):
    """测试多次交易"""
    print("\n=== 测试多次交易 ===")
    
    try:
        # 买入第二只股票
        sim.buy_stock("600000", "浦发银行", 15.50, 200, "加仓测试")
        
        # 查看持仓
        sim.print_position_summary()
        
        # 总市值计算
        value = sim.get_current_value()
        print(f"\n当前市值: ¥{value:.2f}")
        
        print("✅ 多次交易测试通过")
    except Exception as e:
        print(f"多次交易失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_profit_report(sim):
    """测试盈亏报告"""
    print("\n=== 测试盈亏报告 ===")
    
    report = sim.get_profit_report()
    
    print(f"\n📊 交易报告")
    print(f"{'=' * 40}")
    print(f"初始资金: ¥{report['initial_capital']:,.2f}")
    print(f"当前市值: ¥{report['current_value']:,.2f}")
    print(f"总收益: ¥{report['total_profit']:,.2f}")
    print(f"收益率: {report['profit_pct']:+.2f}%")
    print(f"交易次数: {report['total_trades']}")
    print(f"交易天数: {report['trading_days']}")
    
    if report['total_trades'] > 0:
        print(f"胜率: {report['win_rate']:.2f}%")
    
    print("✅ 盈亏报告测试通过")


def test_classify_signal():
    """测试信号强度分类"""
    print("\n=== 测试信号强度分类 ===")
    
    test_cases = [
        (98, 'S1', '强力推荐'),
        (95, 'S1', '强力推荐'),
        (94, 'S2', '考虑交易'),
        (85, 'S2', '考虑交易'),
        (84, 'S3', '观察'),
        (70, 'S3', '观察'),
        (69, 'D', '观望'),
        (50, 'D', '观望'),
    ]
    
    for strength, expected_class, expected_label in test_cases:
        classification, label, desc = classify_signal_strength(strength)
        assert classification == expected_class, f"强度 {strength}: 期望 {expected_class}, 得到 {classification}"
        print(f"  强度 {strength}% → {classification} ({label})")
    
    print("✅ 信号分类测试通过")


def main():
    """主测试函数"""
    print("=" * 60)
    print("A股模拟操盘系统 - 交易引擎测试")
    print("=" * 60)
    
    try:
        # 运行所有测试
        sim = test_initialize()
        test_buy_stock(sim)
        test_multiple_trades(sim)
        test_profit_report(sim)
        test_classify_signal()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过!")
        print("=" * 60)
        
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
