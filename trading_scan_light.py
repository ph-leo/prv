#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股盘前信号扫描脚本 - 轻量版
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
            result = func()
            if result is not None and len(result) > 0:
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ {func.__name__} 最终失败: {e}")
                return None
            print(f"⚠️  {func.__name__} 尝试 {attempt + 1}/{max_retries} 失败: {e}")
            time.sleep(2)
    return None

def main():
    print("🚀 A股盘前信号扫描 - 轻量版")
    print("="*60)
    
    # 存储数据
    us_data = {}
    stocks = []
    
    # Step 1: 获取美股指数（使用 sina index）
    print("\n📊 获取隔夜美股数据...")
    try:
        df = ak.index_us_sina()
        if df is not None and len(df) > 0:
            print(f"获取到 {len(df)} 个美股指数")
            print(df[['symbol', 'name', 'price', 'change', 'change_rate']].head(20))
            
            # 提取关键指数
            for idx, row in df.iterrows():
                symbol = row['symbol']
                if 'IXIC' in symbol:  # 纳斯达克
                    us_data['nasdaq'] = {
                        'price': row['price'],
                        'change': row['change'],
                        'change_rate': row['change_rate']
                    }
                    print(f"纳斯达克: {row['price']} ({row['change_rate']:+.2f}%)")
                elif 'DJI' in symbol:  # 道指
                    us_data['dji'] = {
                        'price': row['price'],
                        'change': row['change'],
                        'change_rate': row['change_rate']
                    }
                    print(f"道指: {row['price']} ({row['change_rate']:+.2f}%)")
                elif 'SOX' in symbol:  # 费城半导体
                    us_data['sox'] = {
                        'price': row['price'],
                        'change': row['change'],
                        'change_rate': row['change_rate']
                    }
                    print(f"费城半导体: {row['price']} ({row['change_rate']:+.2f}%)")
    except Exception as e:
        print(f"美股数据获取部分失败: {e}")
    
    # Step 2: 获取市场热度板块
    print("\n📈 获取行业资金流向...")
    try:
        df = ak.stock_fund_flow_industry()
        if df is not None and len(df) > 0:
            print("\n行业资金流向Top5:")
            print(df[['行业', '最新价', '涨跌幅', '流通市值', '涨跌家数']].head(10).to_string())
             # 提取前5个行业
            for idx, row in df.head(5).iterrows():
                print(f"  • {row['行业']}: 涨跌幅 {row['涨跌幅']:+.2f}%")
    except Exception as e:
        print(f"行业数据获取失败: {e}")
    
    # Step 3: 获取A股涨幅榜
    print("\n🎯 筛选今日强势股票...")
    try:
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            # 按涨跌幅排序
            df_sorted = df.sort_values(by='涨跌幅', ascending=False)
            
            print(f"\n涨幅前10的股票:")
            print(df_sorted[['代码', '名称', '最新价', '涨跌幅', '成交额', '量比']].head(10).to_string())
            
            # 选择5只股票
            for idx, row in df_sorted.head(5).iterrows():
                stocks.append({
                    'code': row['代码'],
                    'name': row['名称'],
                    'price': row['最新价'],
                    'change_pct': row['涨跌幅'],
                    'turnover': row['成交额'],
                    'volume_ratio': row['量比'],
                    'reason': f"今日涨幅{row['涨跌幅']:.2f}%，量比{row['量比']:.2f}，资金活跃"
                })
    except Exception as e:
        print(f"股票筛选失败: {e}")
    
    # Step 4: 生成报告
    print("\n" + "="*60)
    print("🚀 A股盘前信号扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\n📊 隔夜美股表现:")
    if us_data.get('nasdaq'):
        print(f"  • 纳斯达克: {us_data['nasdaq']['price']} ({us_data['nasdaq']['change_rate']:+.2f}%)")
    else:
        print("  • 纳斯达克: 数据获取失败")
    
    if us_data.get('dji'):
        print(f"  • 道指: {us_data['dji']['price']} ({us_data['dji']['change_rate']:+.2f}%)")
    else:
        print("  • 道指: 数据获取失败")
    
    if us_data.get('sox'):
        print(f"  • 费城半导体: {us_data['sox']['price']} ({us_data['sox']['change_rate']:+.2f}%)")
    else:
        print("  • 费城半导体: 数据获取失败")
    
    print("\n💡 对A股影响分析:")
    if us_data.get('nasdaq') and us_data['nasdaq']['change_rate'] > 0:
        print("  • 纳斯达克上涨，对A股科技板块有正面影响")
    elif us_data.get('nasdaq'):
        print("  • 纳斯达克下跌，A股科技板块可能承压")
    
    if us_data.get('sox') and us_data['sox']['change_rate'] > 0:
        print("  • 费城半导体强势，半导体板块可能受益")
    
    print("\n🔮 今日热点板块预判:")
    print("  • 半导体/芯片（受益于费城半导体表现）")
    print("  • 新能源车（特斯拉等造车势力影响）")
    print("  • 科创板科技股（纳斯达克联动）")
    print("  • 人工智能（美股AI龙头带动）")
    
    print("\n🎯 今日推荐】（5只）")
    if stocks:
        for i, stock in enumerate(stocks, 1):
            print(f"{i}. {stock['code']} - {stock['name']} - {stock['reason']}")
    else:
        print("  • 股票数据获取失败，无法推荐")
    
    print("\n" + "="*60)
    print("数据来源: akshare (东方财富/同花顺)")
    print("注意: 本报告仅供参考，不构成投资建议")
    print("="*60)
    
    # Step 5: 发送到钉钉（如果库可用）
    print("\n📩 尝试发送到钉钉...")
    try:
        import sys
        sys.path.insert(0, '/usr/lib/node_modules/openclaw')
        from openclaw.plugins import dingtalk
        print("钉钉模块加载成功")
    except Exception as e:
        print(f"钉钉模块不可用: {e}")
        print("提示: 请配置钉钉机器人 Webhook 地址")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
