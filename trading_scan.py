#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股盘前信号扫描脚本
执行时间：每天 08:30（A股开盘前）
"""

import akshare as ak
import sys
import time
from datetime import datetime

MAX_RETRIES = 3

def retry_fetch(func, max_retries=MAX_RETRIES):
    """重试机制获取数据"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ {func.__name__} 最终失败: {e}")
                return None
            print(f"⚠️  {func.__name__} 尝试 {attempt + 1}/{max_retries} 失败: {e}")
            time.sleep(2)
    return None

def get_us_market_data():
    """获取隔夜美股数据"""
    print("\n" + "="*60)
    print("📊 获取隔夜美股数据")
    print("="*60)
    
    data = {}
    
    # 纳斯达克指数
    def fetch_nasdaq():
        return ak.stock_us_daily(symbol="105.NASDAQ")
    
    df = retry_fetch(fetch_nasdaq)
    if df is not None and len(df) > 0:
        row = df.iloc[0]
        data['nasdaq'] = {
            'open': row['open'],
            'close': row['close'],
            'high': row['high'],
            'low': row['low'],
            'volume': row['volume'],
            'change_pct': (row['close'] - row['open']) / row['open'] * 100
        }
        print(f"纳斯达克: {row['close']:.2f} ({data['nasdaq']['change_pct']:+.2f}%)")
    
    # 道琼斯指数
    def fetch_dji():
        return ak.stock_us_daily(symbol="104.DJI")
    
    df = retry_fetch(fetch_dji)
    if df is not None and len(df) > 0:
        row = df.iloc[0]
        data['dji'] = {
            'open': row['open'],
            'close': row['close'],
            'high': row['high'],
            'low': row['low'],
            'volume': row['volume'],
            'change_pct': (row['close'] - row['open']) / row['open'] * 100
        }
        print(f"道指: {row['close']:.2f} ({data['dji']['change_pct']:+.2f}%)")
    
    # 费城半导体指数
    def fetch_sox():
        return ak.stock_us_daily(symbol="106.OSX")
    
    df = retry_fetch(fetch_sox)
    if df is not None and len(df) > 0:
        row = df.iloc[0]
        data['sox'] = {
            'close': row['close'],
            'change_pct': (row['close'] - row['open']) / row['open'] * 100
        }
        print(f"费城半导体: {row['close']:.2f} ({data['sox']['change_pct']:+.2f}%)")
    
    # 热门中概股
    print("\n热门中概股:")
    gONGs = {
        '103.BABA': '阿里巴巴',
        '103.NIO': '蔚来',
        '103.LK': '贝壳',
        '103.PDD': '拼多多',
        '103.IDXG': '理想汽车',
        '103.TM': '丰田',
        '103.TSLA': '特斯拉',
        '103.AMZN': '亚马逊',
        '103.MSFT': '微软',
        '103.GOOG': '谷歌',
    }
    
    for code, name in gONGs.items():
        def fetch_stock(code=code):
            return ak.stock_us_daily(symbol=code)
        
        df = retry_fetch(fetch_stock)
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            change_pct = (row['close'] - row['open']) / row['open'] * 100
            print(f"  {name}: {row['close']:.2f} ({change_pct:+.2f}%)")
    
    return data

def get_industry_ranking():
    """获取行业排名数据"""
    print("\n" + "="*60)
    print("📈 获取行业排名数据")
    print("="*60)
    
    try:
        # 行业资金流向
        df = ak.stock_fund_flow_industry()
        if len(df) > 0:
            print("\n行业资金流向Top10:")
            print(df[['行业', '最新价', '涨跌幅', '主力净额', '主力净占比']].head(10).to_string())
            return df
    except Exception as e:
        print(f"行业数据获取失败: {e}")
    
    return None

def select_stocks():
    """筛选今日推荐股票"""
    print("\n" + "="*60)
    print("选股筛选今日推荐股票")
    print("="*60)
    
    try:
        # 获取涨跌幅排名
        df = ak.stock_zh_a_spot_em()
        if df is None or len(df) == 0:
            print("无法获取股票行情数据")
            return []
        
        # 筛选条件：涨幅前5、成交额大、量比大
        df_sorted = df.sort_values(by='涨跌幅', ascending=False).head(20)
        
        print("\n涨幅前20的股票:")
        print(df_sorted[['代码', '名称', '最新价', '涨跌幅', '成交额', '量比']].to_string())
        
        # 选择5只股票
        selected = []
        for idx, row in df_sorted.head(5).iterrows():
            selected.append({
                'code': row['代码'],
                'name': row['名称'],
                'price': row['最新价'],
                'change_pct': row['涨跌幅'],
                'turnover': row['成交额'],
                'volume_ratio': row['量比'],
                'reason': f"涨幅{row['涨跌幅']:.2f}%，量比{row['量比']:.2f}"
            })
        
        return selected
        
    except Exception as e:
        print(f"选股失败: {e}")
        return []

def generate_report(us_data, industry_data, stocks):
    """生成扫描报告"""
    report = []
    report.append("="*60)
    report.append("🚀 A股盘前信号扫描报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*60)
    
    # 美股影响分析
    report.append("\n📊 隔夜美股表现:")
    if us_data.get('nasdaq'):
        report.append(f"  • 纳斯达克: {us_data['nasdaq']['close']:.2f} ({us_data['nasdaq']['change_pct']:+.2f}%)")
    if us_data.get('dji'):
        report.append(f"  • 道指: {us_data['dji']['close']:.2f} ({us_data['dji']['change_pct']:+.2f}%)")
    if us_data.get('sox'):
        report.append(f"  • 费城半导体: {us_data['sox']['close']:.2f} ({us_data['sox']['change_pct']:+.2f}%)")
    
    # 影响分析
    report.append("\n💡 对A股影响分析:")
    if us_data.get('nasdaq') and us_data['nasdaq']['change_pct'] > 0:
        report.append("  • 纳斯达克上涨，对A股科技板块有正面影响")
    else:
        report.append("  • 纳斯达克下跌，A股科技板块可能承压")
    
    if us_data.get('sox') and us_data['sox']['change_pct'] > 0:
        report.append("  • 费城半导体强势，半导体板块可能受益")
    
    # 热点板块预判
    report.append("\n🔮 今日热点板块预判:")
    report.append("  • 半导体/芯片（受益于费城半导体表现）")
    report.append("  • 新能源车（特斯拉等造车势力影响）")
    report.append("  • 科创板科技股（纳斯达克联动）")
    report.append("  • 人工智能（美股AI龙头带动）")
    
    # 今日推荐股票
    report.append("\n🎯 今日推荐】（5只）")
    for i, stock in enumerate(stocks, 1):
        report.append(f"{i}. {stock['code']} - {stock['name']} - {stock['reason']}")
    
    report.append("\n" + "="*60)
    report.append("数据来源: akshare (东方财富/同花顺)")
    report.append("注意: 本报告仅供参考，不构成投资建议")
    report.append("="*60)
    
    return "\n".join(report)

def main():
    print("🚀 开始A股盘前信号扫描...")
    
    # Step 1: 获取美股数据
    us_data = get_us_market_data()
    
    # Step 2: 获取行业数据
    industry_data = get_industry_ranking()
    
    # Step 3: 筛选股票
    stocks = select_stocks()
    
    # Step 4: 生成报告
    report = generate_report(us_data, industry_data, stocks)
    
    print("\n" + report)
    
    # Step 5: 发送到钉钉
    try:
        import dingtalk_tensor as dt
        # 使用钉钉机器人发送
        dt.send_to_dingtalk(report, target_cid="cidPRZXi2wt7jEmvEe4h6ye2w==")
        print("\n✅ 报告已发送到钉钉群")
    except Exception as e:
        print(f"\n⚠️  钉钉发送失败（仅影响推送，不影响报告生成）: {e}")
    
    return report

if __name__ == "__main__":
    main()
