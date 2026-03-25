#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股模拟操盘系统 - 5万元模拟账户
任务：每天09:30开盘时执行，扫描S1强信号（≥95%）

注意：由于akshare实时数据接口不稳定，本脚本使用预设模拟数据演示流程
实际运行时需要替换为稳定的A股数据源
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

# 模拟账户配置
INITIAL_BALANCE = 50000.0  # 5万元
ACCOUNT_FILE = "/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/trading_account.json"
SIGNAL_HISTORY_FILE = "/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/signal_history.json"
CONFIRMED_TRADES_FILE = "/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/confirmed_trades.json"

# 预设股票池（模拟数据）- 包含S1级别强信号
# 实际使用时应替换为从数据源获取的实时数据
PRESET_STOCKS = [
    # 代码, 名称, 今开, 最高, 最低, 最新价, 涨跌幅, 成交额
    # S1强信号（涨跌幅≥5%，接近涨停）
    ("sh600000", "浦发银行", 12.50, 12.80, 12.40, 13.10, 5.12, "2.5亿"),  # 信号强度：100%
    ("sz000001", "平安银行", 15.20, 15.60, 15.10, 15.95, 5.08, "3.2亿"),  # 信号强度：100%
    # S2信号（涨跌幅3-5%）
    ("sh600036", "招商银行", 35.80, 36.50, 35.60, 36.85, 3.04, "5.8亿"),
    ("sz000651", "格力电器", 38.20, 39.00, 38.00, 38.90, 1.83, "4.1亿"),
    # 小幅上涨
    ("sh600519", "贵州茅台", 1750.00, 1780.00, 1740.00, 1762.00, 1.44, "8.5亿"),
    ("sz300750", "宁德时代", 185.00, 189.00, 184.00, 186.50, 1.90, "6.2亿"),
    ("sh601318", "中国平安", 48.50, 49.20, 48.30, 49.00, 1.03, "7.3亿"),
    ("sz002475", "立讯精密", 28.50, 29.20, 28.30, 29.10, 2.11, "3.8亿"),
]

class TradingAccount:
    """模拟交易账户管理"""
    
    def __init__(self, initial_balance: float = INITIAL_BALANCE):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.holdings = {}  # {stock_code: {"shares": int, "cost_price": float}}
        self.trades = []  # 交易记录
        self.portfolio_value = initial_balance
        self.daily_pnl = 0.0
        
    def load(self):
        """从文件加载账户状态"""
        if os.path.exists(ACCOUNT_FILE):
            with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.balance = data.get('balance', self.initial_balance)
                self.holdings = data.get('holdings', {})
                self.trades = data.get('trades', [])
                self.portfolio_value = data.get('portfolio_value', self.initial_balance)
                
    def save(self):
        """保存账户状态到文件"""
        data = {
            'balance': self.balance,
            'holdings': self.holdings,
            'trades': self.trades,
            'portfolio_value': self.portfolio_value,
            'updated_at': datetime.now().isoformat()
        }
        with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_portfolio(self):
        """更新投资组合价值"""
        # 模拟更新（使用预设价格）
        self.portfolio_value = self.balance
        for code, holding in self.holdings.items():
            # 从预设数据中查找当前价格
            for stock in PRESET_STOCKS:
                if stock[0] == code:
                    current_price = stock[5]  # 最新价
                    self.portfolio_value += holding['shares'] * current_price
                    break
    
    def buy(self, stock_code: str, stock_name: str, price: float, shares: int) -> bool:
        """买入股票"""
        cost = price * shares
        if cost > self.balance:
            return False
        
        self.balance -= cost
        if stock_code in self.holdings:
            # 加仓计算成本价
            oldholding = self.holdings[stock_code]
            total_shares = oldholding['shares'] + shares
            total_cost = oldholding['shares'] * oldholding['cost_price'] + cost
            new_cost_price = total_cost / total_shares if total_shares > 0 else price
            self.holdings[stock_code] = {
                'shares': total_shares,
                'cost_price': new_cost_price
            }
        else:
            self.holdings[stock_code] = {
                'shares': shares,
                'cost_price': price
            }
        
        trade_record = {
            'type': 'buy',
            'code': stock_code,
            'name': stock_name,
            'price': price,
            'shares': shares,
            'timestamp': datetime.now().isoformat()
        }
        self.trades.append(trade_record)
        self.save()
        return True
    
    def sell(self, stock_code: str, stock_name: str, price: float, shares: int) -> bool:
        """卖出股票"""
        if stock_code not in self.holdings or self.holdings[stock_code]['shares'] < shares:
            return False
        
        revenue = price * shares
        self.balance += revenue
        self.holdings[stock_code]['shares'] -= shares
        
        if self.holdings[stock_code]['shares'] == 0:
            del self.holdings[stock_code]
        
        trade_record = {
            'type': 'sell',
            'code': stock_code,
            'name': stock_name,
            'price': price,
            'shares': shares,
            'timestamp': datetime.now().isoformat()
        }
        self.trades.append(trade_record)
        self.save()
        return True
    
    def get_profit_loss(self) -> Dict:
        """计算盈亏"""
        self.update_portfolio()
        total_profit = self.portfolio_value - self.initial_balance
        profit_rate = (total_profit / self.initial_balance) * 100 if self.initial_balance > 0 else 0
        return {
            'initial_balance': self.initial_balance,
            'current_portfolio': round(self.portfolio_value, 2),
            'total_profit': round(total_profit, 2),
            'profit_rate': round(profit_rate, 2)
        }

def load_signal_history() -> Dict:
    """加载信号历史"""
    if os.path.exists(SIGNAL_HISTORY_FILE):
        with open(SIGNAL_HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_signal_history(history: Dict):
    """保存信号历史"""
    with open(SIGNAL_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_confirmed_trades() -> List[Dict]:
    """加载已确认交易"""
    if os.path.exists(CONFIRMED_TRADES_FILE):
        with open(CONFIRMED_TRADES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_confirmed_trades(trades: List[Dict]):
    """保存已确认交易"""
    with open(CONFIRMED_TRADES_FILE, 'w', encoding='utf-8') as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

def calculate_signal_strength(stock: tuple) -> float:
    """
    计算信号强度（0-100%）
    基于多种技术指标和市场情绪
    
    stock: (code, name, open, high, low, last, change_pct, amount)
    """
    strength = 0.0
    _, _, opn, high, low, price, change_pct, amount = stock
    
    # 1. 价格动量 (30%)
    if change_pct > 0:
        strength += 15
    if change_pct >= 3:
        strength += 20
    if change_pct >= 5:  # 涨停接近
        strength += 25
    
    # 2. 开盘价位置 (20%)
    if price > opn:
        strength += 10
    if price > high * 0.98:  # 接近当日高点
        strength += 15
    
    # 3. 成交额放大 (15%)
    # 简化处理，实际应计算成交量均线
    if '亿' in amount:
        num_amount = float(amount.replace('亿', ''))
        if num_amount > 1:
            strength += 10
        if num_amount > 3:
            strength += 15
    
    # 4. 价格位置 (20%)
    # 模拟计算近期位置
    if price > opn * 1.02:
        strength += 15
    
    # 5. 涨停状态 (15%)
    if change_pct >= 9.5:
        strength += 15
    
    return min(strength, 100.0)

def scan_s1_strong_signals() -> List[Dict]:
    """
    扫描S1级别强信号（≥95%）
    返回符合条件的股票列表
    """
    strong_signals = []
    
    for stock in PRESET_STOCKS:
        strength = calculate_signal_strength(stock)
        
        # 筛选S1级别强信号（≥95%）
        if strength >= 95:
            strong_signals.append({
                'code': stock[0],
                'name': stock[1],
                'price': stock[5],
                'change_pct': stock[6],
                'open': stock[2],
                'strength': round(strength, 2),
                'timestamp': datetime.now().isoformat()
            })
    
    return strong_signals

def format_signal_message(signals: List[Dict]) -> str:
    """格式化信号消息"""
    if not signals:
        return "【A股开盘扫描】\n今日本轮扫描无S1级别强信号。\n等待下一个交易日..."
    
    message = "【A股开盘扫描 - S1强信号】\n"
    message += f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"发现信号数量: {len(signals)}\n\n"
    
    for i, signal in enumerate(signals, 1):
        message += f"【{i}】{signal['code']} {signal['name']}\n"
        message += f"   当前价: {signal['price']}元\n"
        message += f"   涨跌幅: {signal['change_pct']}%\n"
        message += f"   开盘价: {signal['open']}元\n"
        message += f"   信号强度: {signal['strength']}%\n\n"
    
    message += "确认后可执行模拟交易"
    return message

def generate_daily_report(account: TradingAccount) -> str:
    """生成每日盈亏报告"""
    account.update_portfolio()
    pnl = account.get_profit_loss()
    
    report = f"【每日盈亏报告】{datetime.now().strftime('%Y-%m-%d')}\n"
    report += f"初始资金: ¥{pnl['initial_balance']:.2f}\n"
    report += f"当前市值: ¥{pnl['current_portfolio']:.2f}\n"
    report += f"盈亏金额: ¥{pnl['total_profit']:.2f}\n"
    report += f"收益率: {pnl['profit_rate']}%\n"
    
    # 持仓详情
    if account.holdings:
        report += "\n【持仓详情】\n"
        for code, holding in account.holdings.items():
            report += f"{code} {holding['shares']}股 (成本: ¥{holding['cost_price']:.2f})\n"
    
    return report

def main():
    """主函数"""
    print("=" * 50)
    print("A股模拟操盘系统 - 启动")
    print("=" * 50)
    
    # 初始化账户
    account = TradingAccount()
    account.load()
    print(f"账户资金: ¥{account.balance:.2f}")
    
    # 检查时间（09:30执行）
    current_time = datetime.now()
    print(f"当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 只在交易日执行（周一-周五）
    if current_time.weekday() >= 5:
        print("休息日，跳过执行")
        return
    
    # 获取今天日期用于检查
    today = current_time.strftime('%Y-%m-%d')
    
    # 扫描S1强信号
    print("开始扫描S1级别强信号...")
    signals = scan_s1_strong_signals()
    
    # 格式化消息
    message = format_signal_message(signals)
    print("\n" + message)
    
    # 将信号保存为待确认交易
    confirmed_trades = load_confirmed_trades()
    
    # 检查当日是否已有待确认交易（避免重复添加）
    today_pending = [t for t in confirmed_trades if t.get('date') == today and t.get('status') == 'pending']
    
    if signals and not today_pending:
        # 为每个信号创建待确认交易
        new_trades = []
        for signal in signals:
            trade = {
                'code': signal['code'],
                'name': signal['name'],
                'price': signal['price'],
                'strength': signal['strength'],
                'status': 'pending',  # pending, confirmed, skipped
                'date': today,
                'created_at': signal['timestamp']
            }
            new_trades.append(trade)
        
        # 保存待确认交易
        confirmed_trades.extend(new_trades)
        save_confirmed_trades(confirmed_trades)
        
        print(f"\n已保存 {len(new_trades)} 个S1强信号到待确认列表")
    elif today_pending:
        print(f"\n今日已有 {len(today_pending)} 个待确认信号，无需重复添加")
    
    # 保存信号历史
    signal_history = load_signal_history()
    if 'scanned_dates' not in signal_history:
        signal_history['scanned_dates'] = []
    signal_history['scanned_dates'].append(today)
    signal_history['last_scan'] = datetime.now().isoformat()
    save_signal_history(signal_history)
    
    # 检查是否需要生成10天报告
    # 这里简化处理，实际应记录开始日期并计算10天后
    confirmed_trades_this_period = [t for t in confirmed_trades if t.get('status') == 'confirmed']
    days_trading = len(set(t.get('date', today) for t in confirmed_trades_this_period))
    if days_trading == 10:
        report = generate_daily_report(account)
        print("\n" + report)
        print("10天周期结束，已生成盈亏报告")

if __name__ == "__main__":
    main()
