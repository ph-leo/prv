#!/usr/bin/env python3
"""
A股模拟交易引擎
管理模拟账户、交易执行、盈亏计算
"""

import pandas as pd
from datetime import datetime, timedelta


class TradingSimulation:
    """A股模拟交易引擎"""
    
    def __init__(self, initial_capital=50000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}  # {stock_code: {'shares': int, 'cost': float}}
        self.trades = []     # 交易记录
        self.start_date = None
        self.current_date = None
        self.trading_days = 0
        self.signal_count = 0
        
    def start_simulation(self):
        """开始模拟交易"""
        self.start_date = datetime.now()
        self.current_date = self.start_date
        self.trading_days = 0
        self.trades = []
        self.positions = {}
        self.cash = self.initial_capital
        print(f"模拟交易开始: {self.start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"初始资金: ¥{self.initial_capital:,.2f}")
        
    def buy_stock(self, stock_code, stock_name, price, shares, reason=""):
        """买入股票"""
        cost = price * shares
        
        if cost > self.cash:
            print(f"资金不足，无法买入 {stock_name}")
            return False
        
        self.cash -= cost
        self.trading_days += 1
        
        if stock_code in self.positions:
            # 加仓计算
            old_pos = self.positions[stock_code]
            total_cost = old_pos['cost'] * old_pos['shares'] + cost
            total_shares = old_pos['shares'] + shares
            old_pos['cost'] = total_cost / total_shares
            old_pos['shares'] = total_shares
        else:
            self.positions[stock_code] = {
                'shares': shares,
                'cost': price,
                'name': stock_name
            }
        
        trade_record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'BUY',
            'code': stock_code,
            'name': stock_name,
            'price': price,
            'shares': shares,
            'total': cost,
            'reason': reason
        }
        self.trades.append(trade_record)
        
        print(f"买入: {stock_name} ({stock_code}) {shares}股 @ ¥{price:.2f} = ¥{cost:.2f}")
        return True
    
    def sell_stock(self, stock_code, price, reason=""):
        """卖出股票"""
        if stock_code not in self.positions:
            print(f"未持有 {stock_code}")
            return False
        
        pos = self.positions[stock_code]
        shares = pos['shares']
        revenue = price * shares
        profit = revenue - (pos['cost'] * shares)
        
        self.cash += revenue
        del self.positions[stock_code]
        
        trade_record = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'SELL',
            'code': stock_code,
            'name': pos['name'],
            'price': price,
            'shares': shares,
            'total': revenue,
            'profit': profit,
            'reason': reason
        }
        self.trades.append(trade_record)
        
        print(f"卖出: {pos['name']} ({stock_code}) {shares}股 @ ¥{price:.2f} = ¥{revenue:.2f}")
        print(f"  盈亏: ¥{profit:.2f} ({profit / (pos['cost'] * shares) * 100:.2f}%)")
        return True
    
    def get_current_value(self):
        """获取当前市值"""
        position_value = sum(
            pos['shares'] * pos['cost']  # 使用成本价作为当前价（简化版）
            for pos in self.positions.values()
        )
        return self.cash + position_value
    
    def get_current_price(self, stock_code):
        """获取股票当前价格（简化版，实际应从行情数据获取）"""
        # 这里简化处理，实际应用中需要从实时行情数据获取
        if stock_code in self.positions:
            return self.positions[stock_code]['cost']  # 暂时使用成本价
        return 0
    
    def get_profit_report(self):
        """获取盈亏报告"""
        current_value = self.get_current_value()
        total_profit = current_value - self.initial_capital
        profit_pct = (total_profit / self.initial_capital) * 100
        
        # 统计胜率
        winning_trades = sum(1 for t in self.trades if t.get('profit', 0) > 0)
        total_trades = len(self.trades)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        report = {
            'initial_capital': self.initial_capital,
            'current_value': current_value,
            'total_profit': total_profit,
            'profit_pct': profit_pct,
            'trading_days': self.trading_days,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'cash': self.cash,
            'positions': self.positions
        }
        
        return report
    
    def print_position_summary(self):
        """打印持仓摘要"""
        if not self.positions:
            print("当前无持仓")
            return
        
        print("\n=== 持仓摘要 ===")
        for code, pos in self.positions.items():
            current_price = self.get_current_price(code)
            position_value = pos['shares'] * current_price
            profit = position_value - (pos['cost'] * pos['shares'])
            profit_pct = (profit / (pos['cost'] * pos['shares'])) * 100
            
            print(f"{pos['name']} ({code}):")
            print(f"  持仓: {pos['shares']}股")
            print(f"  成本: ¥{pos['cost']:.2f}")
            print(f"  现价: ¥{current_price:.2f}")
            print(f"  市值: ¥{position_value:.2f}")
            print(f"  盈亏: ¥{profit:.2f} ({profit_pct:.2f}%)")


def create_signal_message(signal):
    """创建信号通知消息"""
    s = signal
    classification, label, desc = classify_signal_strength(s['signal_strength'])
    
    msg = (
        f"【{classification}信号 - {label}】\n"
        f"股票: {s['name']} ({s['code']})\n"
        f"当前价: ¥{s['price']:.2f}\n"
        f"涨跌幅: {s['change_pct']:+.2f}%\n"
        f"信号强度: {s['signal_strength']}%\n"
        f"推荐理由: {desc}\n"
        f"操作建议: {'逢低建仓' if s['change_pct'] > 0 else '观察等待'}"
    )
    return msg


def classify_signal_strength(strength):
    """信号强度分类"""
    if strength >= 95:
        return 'S1', '强力推荐', '信号强度极高，推荐交易'
    elif strength >= 85:
        return 'S2', '考虑交易', '信号强度高，可以考虑'
    elif strength >= 70:
        return 'S3', '观察', '信号强度中等，建议观察'
    else:
        return 'D', '观望', '信号较弱，建议观望'


if __name__ == "__main__":
    # 测试模拟交易引擎
    sim = TradingSimulation(initial_capital=50000)
    sim.start_simulation()
    
    # 模拟一次买入
    sim.buy_stock("301226", "祥明智能", 41.74, 100, "S1信号测试")
    
    # 打印摘要
    sim.print_position_summary()
    
    # 获取报告
    report = sim.get_profit_report()
    print(f"\n=== 初始盈亏报告 ===")
    print(f"初始资金: ¥{report['initial_capital']:,.2f}")
    print(f"当前市值: ¥{report['current_value']:,.2f}")
    print(f"总收益: ¥{report['total_profit']:,.2f} ({report['profit_pct']:.2f}%)")
    print(f"交易次数: {report['total_trades']}")
