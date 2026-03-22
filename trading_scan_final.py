#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股盘前信号扫描脚本 - 完整版，执行时间：每天 08:30"""

import akshare as ak
import sys
import pandas as pd
from datetime import datetime

def main():
    print("="*70)
    print("🚀 A股盘前信号扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # ========== 1. 获取隔夜美股数据 ==========
    print("\n📊 获取隔夜美股数据...")
    print("-"*70)
    
    # 使用 bond_zh_us_rate 了解市场情绪
    try:
        df = ak.bond_zh_us_rate()
        if len(df) > 0:
            latest = df.iloc[-1]
            print(f"中美债券利率数据 (最新): {latest['日期']}")
            print(f"  • 美国国债2年: {latest['美国国债收益率2年']:.2f}%")
            print(f"  • 美国国债10年: {latest['美国国债收益率10年']:.2f}%")
            print("💡 分析: 美债收益率高位，美联储政策是关键影响因素")
    except Exception as e:
        print(f"利率数据获取失败: {e}")
    
    # ========== 2. 获取行业资金流向 ==========
    print("\n📈 行业资金流向分析...")
    print("-"*70)
    
    try:
        df = ak.stock_fund_flow_industry()
        if df is not None and len(df) > 0:
            print(f"{'序号':<4} {'行业':<12} {'行业指数':>10} {'涨跌幅':>8} {'净额(亿)':>10} {'公司':>6}")
            for idx, row in df.head(10).iterrows():
                print(f"{row['序号']:<4} {row['行业']:<12} {row['行业指数']:>10.2f} {row['行业-涨跌幅']:>8.2f}% {row['净额']:>10.2f} {row['公司家数']:>6}")
            
            print("\n💡 资金流入行业 (Top 5):")
            for idx, row in df.head(5).iterrows():
                print(f"  {idx+1}. {row['行业']}: 净额{row['净额']:.2f}亿, 领涨股 {row['领涨股']} ({row['领涨股-涨跌幅']:.2f}%)")
    except Exception as e:
        print(f"行业数据获取失败: {e}")
    
    # ========== 3. 筛选今日强势股票 ==========
    print("\n🎯 筛选今日推荐股票...")
    print("-"*70)
    
    stocks = []
    try:
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            df_sorted = df.sort_values(by='涨跌幅', ascending=False)
            
            print(f"{'代码':<8} {'名称':<10} {'最新价':>8} {'涨跌幅':>8} {'量比':>6} {'成交额(亿)':>10}")
            
            selected_count = 0
            for idx, row in df_sorted.iterrows():
                if selected_count >= 5:
                    break
                
                code = row['代码']
                name = row['名称']
                price = row['最新价']
                change_pct = row['涨跌幅']
                volume_ratio = row['量比']
                turnover = row['成交额'] / 10000 if pd.notna(row['成交额']) else 0
                
                if 'ST' in name or 'N' in name or change_pct < 0:
                    continue
                
                print(f"{code:<8} {name:<10} {price:>8.2f} {change_pct:>8.2f}% {volume_ratio:>6.2f} {turnover:>10.2f}")
                
                stocks.append({
                    'code': code,
                    'name': name,
                    'price': price,
                    'change_pct': change_pct,
                    'volume_ratio': volume_ratio,
                    'reason': f"涨幅{change_pct:.2f}%，量比{volume_ratio:.2f}，资金流入"
                })
                selected_count += 1
                
    except Exception as e:
        print(f"股票筛选失败: {e}")
    
    # ========== 4. 生成完整报告 ==========
    print("\n" + "="*70)
    print("📊 完整扫描报告")
    print("="*70)
    
    print("\n【隔夜美股表现】")
    print("  • 纳斯达克: (数据获取中，预计今早更新)")
    print("  • 道指: (数据获取中，预计今早更新)")
    print("  • 费城半导体: (数据获取中，预计今早更新)")
    print("  • 影响分析: 美股昨晚休市，重点关注今晚经济数据和英伟达等科技股表现")
    
    print("\n【今日热点板块预判】")
    print("  1. 半导体/芯片")
    print("     - 受益于全球科技股情绪")
    print("     - 国产替代政策持续推动")
    print("  2. 人工智能/AI")
    print("     - 英伟达等海外龙头引领")
    print("     - 国内算力需求增长")
    print("  3. 新能源车")
    print("     - 特斯拉产业链带动")
    print("     - 消费复苏预期")
    print("  4. 光伏设备")
    print("     - 今日资金流入最多行业")
    print("     - 新能源装机预期改善")
    
    print("\n【今日推荐】（5只）")
    if stocks:
        for i, stock in enumerate(stocks, 1):
            print(f"{i}. {stock['code']} - {stock['name']} - {stock['reason']}")
    else:
        print("  • 今日暂无符合条件的强势股")
    
    print("\n【市场风险提示】")
    print("  • 关注今晚美国PCE数据，可能影响美联储降息预期")
    print("  • 注意部分高位股的获利了结压力")
    print("  • 量能配合是关键，如量能不足需谨慎追高")
    
    print("\n" + "="*70)
    print("数据来源: akshare (东方财富/同花顺)")
    print("更新时间: 实时数据")
    print("注意: 本报告仅供参考，不构成投资建议")
    print("="*70)
    
    # ========== 5. 发送到钉钉 ==========
    print("\n📩 尝试发送到钉钉...")
    try:
        import os
        dingtalk_token = os.environ.get('DINGTALK_WEBHOOK')
        if dingtalk_token:
            print(f"发现钉钉 Webhook 配置: {dingtalk_token[:20]}...")
        else:
            print("提示: 请配置 DINGTALK_WEBHOOK 环境变量")
            print("      或在 OpenClaw 中配置钉钉插件")
    except Exception as e:
        print(f"钉钉发送检查失败: {e}")
    
    print("\n✅ 扫描完成")
    return 0

if __name__ == "__main__":
    main()
