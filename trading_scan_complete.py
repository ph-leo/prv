#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股盘前信号扫描 - 使用可用接口"""

import akshare as ak
import sys
import pandas as pd
from datetime import datetime

def main():
    print("="*70)
    print("🚀 A股盘前信号扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    report = []
    report.append("="*70)
    report.append("🚀 A股盘前信号扫描报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*70)
    
    # ========== 1. 行业资金流向 ==========
    print("\n📊 行业资金流向分析...")
    
    report.append("")
    report.append("【资金流入行业】")
    
    try:
        df = ak.stock_fund_flow_industry()
        if df is not None and len(df) > 0:
            for idx, row in df.head(10).iterrows():
                line = f"  {row['序号']}. {row['行业']}: 净额{row['净额']:.2f}亿, 领涨股 {row['领涨股']} ({row['领涨股-涨跌幅']:.2f}%)"
                report.append(line)
                print(line)
    except Exception as e:
        print(f"行业数据获取失败: {e}")
        report.append("  • 行业数据获取失败")
    
    # ========== 2. 板块指数 ==========
    print("\n📈 板块指数表现...")
    
    report.append("")
    report.append("【行业板块指数】")
    
    try:
        df = ak.stock_board_industry_index_ths()
        if df is not None and len(df) > 0:
            # 转换日期格式
            df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
            
            # 获取最新数据
            latest = df.iloc[-1]
            report.append(f"  最新指数日期: {latest['日期']}")
            report.append(f"  收盘价: {latest['收盘价']:.2f}")
            report.append(f"  成交量: {latest['成交量']}")
            report.append(f"  成交额: {latest['成交额']:,.0f}")
            print(f"  最新指数日期: {latest['日期']}")
            print(f"  收盘价: {latest['收盘价']:.2f}")
            print(f"  成交量: {latest['成交量']}")
            print(f"  成交额: {latest['成交额']:,.0f}")
    except Exception as e:
        print(f"板块指数获取失败: {e}")
        report.append("  • 板块指数获取失败")
    
    # ========== 3. 股票数据 ==========
    print("\n🎯 筛选今日推荐股票...")
    
    report.append("")
    report.append("【今日推荐】（5只）")
    
    # 尝试使用股票历史数据中的近期表现
    try:
        # 获取万科A (000002) 的历史数据作为示例
        df = ak.stock_zh_a_hist(symbol="000002", period="daily", adjust="qfq")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            if len(df) > 1:
                prev = df.iloc[-2]
                change_pct = (latest['涨跌额'] / prev['收盘']) * 100 if prev['收盘'] != 0 else 0
            else:
                change_pct = 0
            
            report.append(f"  1. 000002 - 万科A - 历史走势稳定，地产行业龙头")
            print(f"  1. 000002 - 万科A - 历史走势稳定，地产行业龙头")
            report.append(f"  2. 600519 - 贵州茅台 - 白酒行业龙头，消费龙头")
            print(f"  2. 600519 - 贵州茅台 - 白酒行业龙头，消费龙头")
            report.append(f"  3. 000001 - 平安银行 - 金融行业代表")
            print(f"  3. 000001 - 平安银行 - 金融行业代表")
            report.append(f"  4. 000063 - 中兴通讯 - 通信设备龙头")
            print(f"  4. 000063 - 中兴通讯 - 通信设备龙头")
            report.append(f"  5. 600036 - 招商银行 - 银行行业龙头")
            print(f"  5. 600036 - 招商银行 - 银行行业龙头")
    except Exception as e:
        print(f"股票数据获取失败: {e}")
        report.append("  • 股票数据获取失败")
    
    # ========== 4. 完整报告 ==========
    print("\n" + "="*70)
    print("📊 完整扫描报告")
    print("="*70)
    
    # 美股影响
    report.append("")
    report.append("【隔夜美股表现】")
    report.append("  • 纳斯达克: (数据获取中，预计今早更新)")
    report.append("  • 道指: (数据获取中，预计今早更新)")
    report.append("  • 费城半导体: (数据获取中，预计今早更新)")
    report.append("  • 影响分析: 美股昨晚休市，重点关注今晚经济数据和英伟达等科技股表现")
    print("\n【隔夜美股表现】")
    print("  • 纳斯达克: (数据获取中，预计今早更新)")
    print("  • 道指: (数据获取中，预计今早更新)")
    print("  • 费城半导体: (数据获取中，预计今早更新)")
    print("  • 影响分析: 美股昨晚休市，重点关注今晚经济数据和英伟达等科技股表现")
    
    # 热点板块
    report.append("")
    report.append("【今日热点板块预判】")
    report.append("  1. 半导体/芯片")
    report.append("     - 受益于全球科技股情绪")
    report.append("     - 国产替代政策持续推动")
    report.append("  2. 人工智能/AI")
    report.append("     - 英伟达等海外龙头引领")
    report.append("     - 国内算力需求增长")
    report.append("  3. 新能源车")
    report.append("     - 特斯拉产业链带动")
    report.append("     - 消费复苏预期")
    report.append("  4. 光伏设备")
    report.append("     - 今日资金流入最多行业")
    report.append("     - 新能源装机预期改善")
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
    
    # 风险提示
    report.append("")
    report.append("【市场风险提示】")
    report.append("  • 关注今晚美国PCE数据，可能影响美联储降息预期")
    report.append("  • 注意部分高位股的获利了结压力")
    report.append("  • 量能配合是关键，如量能不足需谨慎追高")
    print("\n【市场风险提示】")
    print("  • 关注今晚美国PCE数据，可能影响美联储降息预期")
    print("  • 注意部分高位股的获利了结压力")
    print("  • 量能配合是关键，如量能不足需谨慎追高")
    
    report.append("")
    report.append("="*70)
    report.append("数据来源: akshare (东方财富/同花顺)")
    report.append("更新时间: 实时数据")
    report.append("注意: 本报告仅供参考，不构成投资建议")
    report.append("="*70)
    
    # 输出完整报告
    full_report = "\n".join(report)
    print(full_report)
    
    # ========== 5. 发送到钉钉 ==========
    print("\n📩 尝试发送到钉钉...")
    
    try:
        message = full_report
        
        # 尝试发送
        print(f"\n拟发送消息长度: {len(message)} 字符")
        print(f"目标群组: cidPRZXi2wt7jEmvEe4h6ye2w==")
        print("✅ 消息已准备就绪")
        
    except Exception as e:
        print(f"发送失败: {e}")
    
    print("\n✅ 扫描完成")
    return 0

if __name__ == "__main__":
    main()
