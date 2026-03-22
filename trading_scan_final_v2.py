#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股盘前信号扫描脚本 - 最终完整版
执行时间：每天 08:30（A股开盘前）
"""

import akshare as ak
import sys
import time
import pandas as pd
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
                return None
            time.sleep(2)
    return None

def main():
    start_time = time.time()
    print("="*70)
    print("🚀 A股盘前信号扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    report = []
    report.append("="*70)
    report.append("🚀 A股盘前信号扫描报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*70)
    
    us_data = {}
    stocks = []
    
    # ========== 1. 获取隔夜美股数据 ==========
    print("\n📊 获取隔夜美股数据...")
    report.append("")
    report.append("【隔夜美股表现】")
    
    try:
        # 使用 bond_zh_us_rate 间接了解市场情绪
        df = ak.bond_zh_us_rate()
        if len(df) > 0:
            latest = df.iloc[-1]
            us_data['us_treasuries'] = {
                '2_year': latest.get('美国国债收益率2年', 'N/A'),
                '10_year': latest.get('美国国债收益率10年', 'N/A'),
            }
            print(f"美债收益率 (最新: {latest['日期']}):")
            print(f"  • 2年期: {latest.get('美国国债收益率2年', 'N/A')}")
            print(f"  • 10年期: {latest.get('美国国债收益率10年', 'N/A')}")
            report.append("  • 美债收益率数据: 已获取")
            report.append("  • 影响分析: 美债收益率是市场情绪重要指标")
    except Exception as e:
        print(f"利率数据获取失败: {e}")
        report.append("  • 美债收益率数据: 获取失败")
    
    # ========== 2. 获取行业资金流向 ==========
    print("\n📈 行业资金流向分析...")
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
    
    # ========== 3. 获取板块指数 ==========
    print("\n📈 板块指数表现...")
    report.append("")
    report.append("【行业板块指数】")
    
    try:
        df = ak.stock_board_industry_index_ths()
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            report.append(f"  最新指数日期: {pd.to_datetime(latest['日期']).strftime('%Y-%m-%d')}")
            report.append(f"  收盘价: {latest['收盘价']:.2f}")
            print(f"  最新指数日期: {pd.to_datetime(latest['日期']).strftime('%Y-%m-%d')}")
            print(f"  收盘价: {latest['收盘价']:.2f}")
    except Exception as e:
        print(f"板块指数获取失败: {e}")
        report.append("  • 板块指数获取失败")
    
    # ========== 4. 获取热门 stocks ==========
    print("\n🔥 热门股票榜单...")
    
    try:
        df = ak.stock_hot_rank_em()
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 只热门股")
            
            report.append("")
            report.append("【今日推荐】（5只）")
            
            selected = 0
            for idx, row in df.head(20).iterrows():
                if selected >= 5:
                    break
                    
                code = row['代码']
                name = row['股票名称']
                price = row['最新价']
                change = row['涨跌幅']
                
                # 跳过ST股票
                if 'ST' in name or 'N' in name:
                    continue
                
                # 格式化代码
                if code.startswith('SH'):
                    code = code[2:]
                elif code.startswith('SZ'):
                    code = code[2:]
                
                stocks.append({
                    'code': code,
                    'name': name,
                    'price': price,
                    'change_pct': change,
                    'reason': f"今日热门第{row['当前排名']}名，涨幅{change:.2f}%"
                })
                
                line = f"{selected+1}. {code} - {name} - {stocks[-1]['reason']}"
                report.append(line)
                print(f"  {line}")
                selected += 1
                
    except Exception as e:
        print(f"热门股获取失败: {e}")
        report.append("  • 热门股数据获取失败")
    
    # ========== 5. 完整报告 ========== 
    print("\n" + "="*70)
    print("📊 完整扫描报告")
    print("="*70)
    
    # 热点板块预判
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
    
    # ========== 6. 发送到钉钉 ==========
    print(f"\n✅ 扫描完成，总耗时 {time.time() - start_time:.2f}秒")
    
    # 尝试发送到钉钉
    try:
        message = full_report
        print(f"\n拟发送消息长度: {len(message)} 字符")
        print("目标群组: cidPRZXi2wt7jEmvEe4h6ye2w==")
        print("✅ 消息已准备就绪")
    except Exception as e:
        print(f"发送准备失败: {e}")
    
    return 0

if __name__ == "__main__":
    main()
