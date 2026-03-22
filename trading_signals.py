#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股盘前信号扫描脚本
执行时间：每天 08:30 (A股开盘前)
"""

import akshare as ak
from datetime import datetime
import pandas as pd

def get_us_market():
    """获取隔夜美股数据"""
    print("\n【1】隔夜美股市场表现：")
    try:
        # 美股指数
        indices = {
            'DJI': '道琼斯工业指数',
            'IXIC': '纳斯达克指数', 
            'SPX': '标普500指数'
        }
        
        for symbol, name in indices.items():
            try:
                data = ak.stock_us_daily(symbol=symbol)
                if len(data) >= 2:
                    last_close = data.iloc[-2]['close']
                    current = data.iloc[-1]['close']
                    change_pct = ((current - last_close) / last_close) * 100
                    print(f"  {name}: {current:.2f} ({change_pct:+.2f}%)")
            except:
                print(f"  {name}: 数据获取受限")
        
        # 热门中概股
        print("\n  热门中概股隔夜表现：")
        try:
            stock_zh_us_spot = ak.stock_zh_us_spot()
            if stock_zh_us_spot is not None and len(stock_zh_us_spot) > 0:
                common_china_stocks = ["阿里巴巴", "腾讯音乐", "拼多多", "京东", "百度", "蔚来", "理想汽车", "小鹏汽车"]
                for stock in common_china_stocks:
                    try:
                        stock_data = stock_zh_us_spot[stock_zh_us_spot['名称'].str.contains(stock)]
                        if len(stock_data) > 0:
                            row = stock_data.iloc[0]
                            print(f"    {row['名称']}: {row['最新价']:.2f} ({row['涨跌幅']:+.2f}%)")
                    except:
                        continue
        except:
            print("    (中概股数据获取受限)")
    except Exception as e:
        print(f"  美股数据获取失败: {e}")


def get_market_sentiment():
    """获取A股市场情绪指标"""
    print("\n【2】A股市场情绪指标：")
    try:
        # 沪深两市涨跌停家数
        stock_zt_pool = ak.stock_zt_pool()
        if stock_zt_pool is not None and len(stock_zt_pool) > 0:
            print(f"  昨日涨停家数: {len(stock_zt_pool)} 家")
    except:
        pass
    
    try:
        # 创业板指数
        cyq_index = ak.index_zh_a_daily(symbol="399006")
        if len(cyq_index) >= 2:
            last_close = cyq_index.iloc[-2]['close']
            current = cyq_index.iloc[-1]['close']
            change_pct = ((current - last_close) / last_close) * 100
            print(f"  创业板指数: {current:.2f} ({change_pct:+.2f}%)")
    except:
        pass


def get_hot_sectors():
    """预判热点板块"""
    print("\n【3】近期热点板块监测：")
    try:
        # 板块资金流向
        stock_sector_fund_flow = ak.stock_sector_fund_flow_sentiment(symbol="/all")
        if stock_sector_fund_flow is not None and len(stock_sector_fund_flow) > 0:
            print("  主力资金流入前5板块：")
            top_flow = stock_sector_fund_flow.nlargest(5, '今日')
            for idx, row in top_flow.iterrows():
                print(f"    {row['名称']}: {row['今日']:.2f} 亿元")
    except Exception as e:
        print(f"  板块数据获取失败: {e}")


def get_recommended_stocks():
    """筛选今日推荐股票"""
    print("\n【4】今日推荐股票（5只）：")
    print("-" * 60)
    
    recommended_stocks = []
    
    try:
        # 获取股票列表
        stock_zh_a_spot = ak.stock_zh_a_spot()
        
        if stock_zh_a_spot is not None and len(stock_zh_a_spot) > 0:
            # 从涨停池中筛选
            try:
                stock_zt_pool_current = ak.stock_zt_pool()
                if stock_zt_pool_current is not None and len(stock_zt_pool_current) > 0:
                    count = 0
                    for idx, row in stock_zt_pool_current.iterrows():
                        if count >= 5:
                            break
                        code = row['代码']
                        name = row['名称']
                        try:
                            stock_zh_a_daily = ak.stock_zh_a_daily(symbol=code)
                            if len(stock_zh_a_daily) >= 5:
                                recent_close = stock_zh_a_daily['close'].iloc[-5:]
                                if recent_close.iloc[-1] > recent_close.iloc[-2] > recent_close.iloc[-3]:
                                    recommended_stocks.append({
                                        'code': code,
                                        'name': name,
                                        'reason': '近期连续上涨，资金持续流入'
                                    })
                                    count += 1
                        except:
                            continue
                    print(f"\n  涨停池选股: {count} 只")
            except Exception as e:
                print(f"  涨停池扫描错误: {e}")
            
            # 如果涨停池不够，补充其他强势股
            if len(recommended_stocks) < 5:
                print(f"\n  补充筛选：寻找资金流入的股票")
                count = len(recommended_stocks)
                
                for idx, row in stock_zh_a_spot.iterrows():
                    if count >= 5:
                        break
                    try:
                        code = row['代码']
                        name = row['名称']
                        price = row['最新价']
                        change_pct = row['涨跌幅']
                        turnover = row['换手率']
                        
                        # 筛选条件：价格 > 5元，涨幅 > 2%，换手率 > 2%
                        if price and price > 5 and change_pct and change_pct > 2 and turnover and turnover > 2:
                            recommended_stocks.append({
                                'code': code,
                                'name': name,
                                'reason': f'价格{price:.2f}元，涨幅{change_pct:.2f}%，换手率{turnover:.2f}%'
                            })
                            count += 1
                    except:
                        continue
        
    except Exception as e:
        print(f"  股票筛选错误: {e}")
    
    # 输出推荐
    if len(recommended_stocks) == 0:
        print("\n  暂无符合推荐条件的股票")
    else:
        for i, stock in enumerate(recommended_stocks[:5], 1):
            print(f"{i}. {stock['code']} - {stock['name']} - {stock['reason']}")


def main():
    print("=" * 60)
    print("【A股盘前信号扫描 - 08:30】")
    print("执行时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    get_us_market()
    get_market_sentiment()
    get_hot_sectors()
    get_recommended_stocks()
    
    print("\n" + "=" * 60)
    print("数据来源：akshare (东方财富/同花顺)")
    print("声明：本信号仅供参考，不构成投资建议")
    print("=" * 60)


if __name__ == "__main__":
    main()
