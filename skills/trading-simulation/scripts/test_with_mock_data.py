#!/usr/bin/env python3
"""
A股模拟操盘系统 - 使用模拟数据测试版本
在无法连接数据源时使用模拟数据演示系统功能
"""

import sys
import os

# 添加引用目录
script_dir = os.path.dirname(os.path.abspath(__file__))
refs_dir = os.path.join(script_dir, '..', 'refs')
sys.path.insert(0, refs_dir)

from simulation_engine import TradingSimulation, create_signal_message
from akshare_stock_indicators import classify_signal_strength


def scan_market_for_signals_mock():
    """
    使用模拟数据扫描A股信号
    基于2026-03-18的典型市场数据
    """
    print("正在扫描全市场信号（模拟数据）...")
    
    # 使用模拟数据
    mock_stocks = [
        # S1级别信号（高强度）- 涨幅超20%
        {'code': '301226', 'name': '祥明智能', 'price': 41.74, 'change_pct': 20.01},
        {'code': '300632', 'name': '(pk)', 'price': 28.50, 'change_pct': 19.98},
        {'code': '688018', 'name': '乐鑫科技', 'price': 92.30, 'change_pct': 15.20},
        # S1信号 - 新能源车龙头 (50元附近，20%涨幅)
        {'code': '300750', 'name': '宁德时代', 'price': 52.00, 'change_pct': 20.00},
        # S1信号 - 阿尔梅达 (55元，20%涨幅)
        {'code': '301519', 'name': '阿尔梅达', 'price': 55.00, 'change_pct': 20.00},
        
        # S2级别信号
        {'code': '002475', 'name': '立讯精密', 'price': 45.20, 'change_pct': 9.85},
        {'code': '600519', 'name': '贵州茅台', 'price': 1850.00, 'change_pct': 8.50},
        
        # S3级别信号
        {'code': '000001', 'name': '平安银行', 'price': 12.30, 'change_pct': 6.50},
        {'code': '601318', 'name': '中国平安', 'price': 52.80, 'change_pct': 5.20},
        
        # 普通波动
        {'code': '000002', 'name': '万科A', 'price': 18.50, 'change_pct': 3.20},
        {'code': '600036', 'name': '招商银行', 'price': 35.60, 'change_pct': -1.50},
        {'code': '002236', 'name': '大华股份', 'price': 15.80, 'change_pct': -2.30},
    ]
    
    signals = []
    for stock in mock_stocks:
        strength = 0
        
        # 1. 涨跌幅权重 (40%)
        if stock['change_pct'] >= 20:
            strength += 40
        elif stock['change_pct'] >= 18:
            strength += 38
        elif stock['change_pct'] >= 16:
            strength += 36
        elif stock['change_pct'] >= 15:
            strength += 35
        elif stock['change_pct'] >= 10:
            strength += 30
        elif stock['change_pct'] >= 7:
            strength += 25
        elif stock['change_pct'] >= 5:
            strength += 20
        elif stock['change_pct'] >= 3:
            strength += 15
        
        # 2. 价格位置权重 (20%)
        if stock['price'] > 100:
            strength += 15
        elif stock['price'] > 50:
            strength += 12
        elif stock['price'] > 20:
            strength += 10
        else:
            strength += 5
        
        # 3. 成交量权重 (30%) - 简化处理
        if stock['change_pct'] >= 15:
            strength += 30
        elif stock['change_pct'] > 10:
            strength += 25
        elif stock['change_pct'] > 0:
            strength += 20
        else:
            strength += 5
        
        # 4. 稳定性权重 (10%)
        if stock['price'] > 50:
            strength += 10
        elif stock['price'] > 20:
            strength += 7
        else:
            strength += 3
        
        signal_strength = min(strength, 100)
        
        if signal_strength >= 70:
            signals.append({
                'code': stock['code'],
                'name': stock['name'],
                'price': stock['price'],
                'change_pct': stock['change_pct'],
                'signal_strength': signal_strength
            })
    
    # 按信号强度排序
    signals.sort(key=lambda x: x['signal_strength'], reverse=True)
    
    print(f"模拟数据共找到 {len(signals)} 个信号")
    return signals


def calculate_signal_strength_mock(stock_code, stock_name, price, change_pct):
    """
    使用简化算法计算信号强度（基于原算法）
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
    
    # 2. 价格位置权重 (20%)
    if price > 100:
        strength += 15
    elif price > 50:
        strength += 12
    elif price > 20:
        strength += 10
    else:
        strength += 5
    
    # 3. 成交量权重 (30%) - 简化处理
    if change_pct > 0:
        strength += 15
    else:
        strength += 5
    
    # 4. 稳定性权重 (10%)
    if price > 50:
        strength += 10
    elif price > 20:
        strength += 7
    else:
        strength += 3
    
    return min(strength, 100)


def display_signals(signals):
    """显示信号摘要"""
    print("\n=== 信号强度分类 ===")
    
    s1_signals = [s for s in signals if s['signal_strength'] >= 95]
    s2_signals = [s for s in signals if 85 <= s['signal_strength'] < 95]
    s3_signals = [s for s in signals if 70 <= s['signal_strength'] < 85]
    
    print(f"\nS1级别信号 (≥95%): {len(s1_signals)} 个")
    for s in s1_signals:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        msg = create_signal_message(s)
        print(f"\n{msg}")
    
    print(f"\nS2级别信号 (85-95%): {len(s2_signals)} 个")
    for s in s2_signals[:5]:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        print(f"{s['code']} {s['name']}: {s['price']}元, 涨幅 {s['change_pct']}%, "
              f"强度 {s['signal_strength']}% [{classification}]")
    
    print(f"\nS3级别信号 (70-85%): {len(s3_signals)} 个")
    for s in s3_signals[:5]:
        classification, label, desc = classify_signal_strength(s['signal_strength'])
        print(f"{s['code']} {s['name']}: {s['price']}元, 涨幅 {s['change_pct']}%, "
              f"强度 {s['signal_strength']}% [{classification}]")
    
    return s1_signals


def execute_trading_simulation(s1_signals):
    """执行模拟交易"""
    print("\n=== 模拟交易执行流程 ===")
    
    # 初始化模拟账户
    sim = TradingSimulation(initial_capital=50000)
    sim.start_simulation()
    
    # 执行交易（如果发现S1信号）
    if s1_signals:
        # 取最强的一个信号执行
        best_signal = s1_signals[0]
        price = best_signal['price']
        shares = int(50000 / price / 100) * 100  # 买100的整数倍
        
        print(f"\n发现S1信号，准备执行交易:")
        print(f"股票: {best_signal['name']} ({best_signal['code']})")
        print(f"当前价: ¥{price:.2f}")
        print(f"建议买入股数: {shares}股")
        print(f"预计花费: ¥{price * shares:.2f}")
        print(f"剩余资金: ¥{50000 - price * shares:.2f}")
        
        if shares > 0 and price * shares <= 50000:
            success = sim.buy_stock(
                best_signal['code'],
                best_signal['name'],
                price,
                shares,
                "S1信号自动执行"
            )
            
            if success:
                print("\n✅ 交易执行成功！")
            else:
                print("\n❌ 交易执行失败")
        else:
            print("\n⚠️ 无法执行交易（资金不足或股数不足）")
    else:
        print("\n未发现S1级别信号，不执行交易")
    
    return sim


def generate_profit_report(sim):
    """生成盈亏报告"""
    print("\n=== 生成10天后盈亏报告 ===")
    
    # 获取实时报告
    report = sim.get_profit_report()
    
    print(f"\n📊 模拟交易报告")
    print(f"{'=' * 50}")
    print(f"初始资金: ¥{report['initial_capital']:,.2f}")
    print(f"当前市值: ¥{report['current_value']:,.2f}")
    print(f"总收益: ¥{report['total_profit']:,.2f} ({report['profit_pct']:+.2f}%)")
    print(f"交易次数: {report['total_trades']}")
    if report['total_trades'] > 0:
        print(f"胜率: {report['win_rate']:.2f}%")
    print(f"交易天数: {report['trading_days']}")
    
    # 打印持仓
    sim.print_position_summary()
    
    return report


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🌟 A股模拟操盘系统 - 模拟数据测试版 🌟")
    print("=" * 60)
    print(f"当前时间: 2026-03-18 09:30")
    print(f"模拟资金: 50,000元")
    print(f"信号频率: 每日开盘扫描")
    print(f"数据源: 模拟数据（用于演示）")
    print("=" * 60)
    
    # 扫描信号
    signals = scan_market_for_signals_mock()
    
    # 显示信号
    s1_signals = display_signals(signals)
    
    # 执行交易
    sim = execute_trading_simulation(s1_signals)
    
    # 生成报告
    report = generate_profit_report(sim)
    
    # 返回状态
    print("\n" + "=" * 60)
    print("✅ 模拟操盘完成")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户取消")
        sys.exit(1)
