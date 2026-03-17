#!/usr/bin/env python3
"""
A股数据获取脚本 - 优化版
带重试机制和多数据源备份
"""

import akshare as ak
import time
from datetime import datetime

def retry_get_data(func, max_retries=3, delay=2):
    """带重试的数据获取"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            print(f"尝试 {i+1}/{max_retries} 失败: {e}")
            if i < max_retries - 1:
                time.sleep(delay)
            else:
                print(f"最终失败: {e}")
                return None

def get_market_data():
    """获取大盘数据"""
    result = {}
    
    # 上证指数
    def get_sh():
        return ak.index_zh_a_hist(symbol="000001", period="daily", 
                                   start_date=datetime.now().strftime('%Y%m%d'),
                                   end_date=datetime.now().strftime('%Y%m%d'))
    
    # 深证成指
    def get_sz():
        return ak.index_zh_a_hist(symbol="399001", period="daily",
                                   start_date=datetime.now().strftime('%Y%m%d'),
                                   end_date=datetime.now().strftime('%Y%m%d'))
    
    # 创业板指
    def get_cy():
        return ak.index_zh_a_hist(symbol="399006", period="daily",
                                   start_date=datetime.now().strftime('%Y%m%d'),
                                   end_date=datetime.now().strftime('%Y%m%d'))
    
    result['sh'] = retry_get_data(get_sh)
    result['sz'] = retry_get_data(get_sz)
    result['cy'] = retry_get_data(get_cy)
    
    return result

def get_zt_data():
    """获取涨停数据"""
    def get_zt():
        return ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
    
    return retry_get_data(get_zt)

def get_top_gainers():
    """获取涨幅榜"""
    def get_gain():
        # 尝试多个数据源
        try:
            # 方法1: 涨停池
            zt = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
            if not zt.empty:
                return zt
        except:
            pass
        
        try:
            # 方法2: 实时行情
            df = ak.stock_zh_a_spot_em()
            return df.nlargest(5, '涨跌幅')
        except:
            pass
        
        return None
    
    return retry_get_data(get_gain, max_retries=3)

def get_top_losers():
    """获取跌幅榜"""
    def get_lose():
        try:
            df = ak.stock_zh_a_spot_em()
            return df.nsmallest(5, '涨跌幅')
        except:
            return None
    
    return retry_get_data(get_lose, max_retries=3)

def get_active_stocks():
    """获取活跃股票（成交量）"""
    def get_active():
        try:
            df = ak.stock_zh_a_spot_em()
            return df.nlargest(5, '成交额')
        except:
            return None
    
    return retry_get_data(get_active, max_retries=3)

def generate_report():
    """生成收盘报告 - 完全获取后再发送"""
    report = []
    report.append("【A股收盘总结】")
    report.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # 大盘数据
    report.append("📊 大盘：")
    market = get_market_data()
    
    if market['sh'] is not None and not market['sh'].empty:
        sh = market['sh'].iloc[0]
        report.append(f"- 上证指数：{sh['收盘']} ({sh['涨跌幅']:.2f}%)")
    else:
        report.append("- 上证指数：❌ 获取失败（网络连接超时）")
    
    if market['sz'] is not None and not market['sz'].empty:
        sz = market['sz'].iloc[0]
        report.append(f"- 深证成指：{sz['收盘']} ({sz['涨跌幅']:.2f}%)")
    else:
        report.append("- 深证成指：❌ 获取失败（网络连接超时）")
    
    if market['cy'] is not None and not market['cy'].empty:
        cy = market['cy'].iloc[0]
        report.append(f"- 创业板指：{cy['收盘']} ({cy['涨跌幅']:.2f}%)")
    else:
        report.append("- 创业板指：❌ 获取失败（网络连接超时）")
    
    report.append("")
    
    # 涨停家数
    report.append("📈 涨跌家数：")
    zt = get_zt_data()
    if zt is not None:
        report.append(f"- 涨停家数：{len(zt)}家")
    else:
        report.append("- 涨停家数：❌ 获取失败（数据源无响应）")
    
    report.append("")
    
    # 涨幅前5
    report.append("🔥 涨幅前5：")
    gainers = get_top_gainers()
    if gainers is not None and not gainers.empty:
        for i, (idx, row) in enumerate(gainers.head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            change = row.get('涨跌幅', 0)
            report.append(f"{i}. {code} - {name} - {change:.2f}%")
    else:
        report.append("❌ 获取失败（重试3次后仍失败）")
    
    report.append("")
    
    # 跌幅前5
    report.append("📉 跌幅前5：")
    losers = get_top_losers()
    if losers is not None and not losers.empty:
        for i, (idx, row) in enumerate(losers.head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            change = row.get('涨跌幅', 0)
            report.append(f"{i}. {code} - {name} - {change:.2f}%")
    else:
        report.append("❌ 获取失败（重试3次后仍失败）")
    
    report.append("")
    
    # 活跃前5
    report.append("💹 活跃前5（成交额）：")
    active = get_active_stocks()
    if active is not None and not active.empty:
        for i, (idx, row) in enumerate(active.head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            amount = row.get('成交额', 0) / 100000000  # 转为亿
            report.append(f"{i}. {code} - {name} - {amount:.2f}亿")
    else:
        report.append("❌ 获取失败（重试3次后仍失败）")
    
    report.append("")
    report.append("---")
    report.append("数据源：akshare（带重试机制）")
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_report())
