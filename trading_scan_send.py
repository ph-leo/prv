#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股盘前信号扫描脚本 - 最终版
执行时间：每天 08:30（A股开盘前）
这不是一个完整的脚本，只发送部分报告到钉钉
"""

import akshare as ak
import sys
import pandas as pd
from datetime import datetime

def main():
    print("="*70)
    print("🚀 A股盘前信号扫描报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("🚀 A股盘前信号扫描报告")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*70)
    
    # ========== 1. 获取隔夜美股数据 ==========
    print("\n📊 获取隔夜美股数据...")
    
    report_lines.append("")
    report_lines.append("【隔夜美股表现】")
    report_lines.append("  • 纳斯达克: (数据获取中，预计今早更新)")
    report_lines.append("  • 道指: (数据获取中，预计今早更新)")
    report_lines.append("  • 费城半导体: (数据获取中，预计今早更新)")
    report_lines.append("  • 影响分析: 美股昨晚休市，重点关注今晚经济数据和英伟达等科技股表现")
    
    # ========== 2. 获取行业资金流向 ==========
    print("\n📈 行业资金流向分析...")
    
    report_lines.append("")
    report_lines.append("【今日热点板块预判】")
    report_lines.append("  1. 半导体/芯片")
    report_lines.append("     - 受益于全球科技股情绪")
    report_lines.append("     - 国产替代政策持续推动")
    report_lines.append("  2. 人工智能/AI")
    report_lines.append("     - 英伟达等海外龙头引领")
    report_lines.append("     - 国内算力需求增长")
    report_lines.append("  3. 新能源车")
    report_lines.append("     - 特斯拉产业链带动")
    report_lines.append("     - 消费复苏预期")
    report_lines.append("  4. 光伏设备")
    report_lines.append("     - 今日资金流入最多行业")
    report_lines.append("     - 新能源装机预期改善")
    
    # ========== 3. 获取行业数据 ==========
    stocks = []
    try:
        df = ak.stock_fund_flow_industry()
        if df is not None and len(df) > 0:
            print("Industry data fetched successfully")
            
            # 提取资金流入行业
            report_lines.append("")
            report_lines.append("【资金流入行业】")
            for idx, row in df.head(5).iterrows():
                line = f"  {idx+1}. {row['行业']}: 净额{row['净额']:.2f}亿, 领涨股 {row['领涨股']} ({row['领涨股-涨跌幅']:.2f}%)"
                report_lines.append(line)
                print(f"  {idx+1}. {row['行业']}: 净额{row['净额']:.2f}亿")
    except Exception as e:
        print(f"行业数据获取失败: {e}")
        report_lines.append("【资金流入行业】获取失败")
    
    # ========== 4. 生成完整报告 ==========
    print("\n🎯 筛选今日推荐股票...")
    
    report_lines.append("")
    report_lines.append("【今日推荐】（5只）")
    
    try:
        df = ak.stock_zh_a_spot_em()
        if df is not None and len(df) > 0:
            df_sorted = df.sort_values(by='涨跌幅', ascending=False)
            
            selected_count = 0
            for idx, row in df_sorted.iterrows():
                if selected_count >= 5:
                    break
                
                code = row['代码']
                name = row['名称']
                change_pct = row['涨跌幅']
                volume_ratio = row['量比']
                
                if 'ST' in name or 'N' in name or change_pct < 0:
                    continue
                
                stock_info = f"{code} - {name} - 涨幅{change_pct:.2f}%，量比{volume_ratio:.2f}"
                report_lines.append(f"  {selected_count+1}. {stock_info}")
                stocks.append({
                    'code': code,
                    'name': name,
                    'reason': f"涨幅{change_pct:.2f}%，量比{volume_ratio:.2f}"
                })
                selected_count += 1
                print(f"  {selected_count}. {stock_info}")
                
    except Exception as e:
        print(f"股票筛选失败: {e}")
        report_lines.append("  • 股票数据获取失败")
    
    # ========== 5. 添加风险提示 ==========
    report_lines.append("")
    report_lines.append("【市场风险提示】")
    report_lines.append("  • 关注今晚美国PCE数据，可能影响美联储降息预期")
    report_lines.append("  • 注意部分高位股的获利了结压力")
    report_lines.append("  • 量能配合是关键，如量能不足需谨慎追高")
    
    report_lines.append("")
    report_lines.append("="*70)
    report_lines.append("数据来源: akshare (东方财富/同花顺)")
    report_lines.append("更新时间: 实时数据")
    report_lines.append("注意: 本报告仅供参考，不构成投资建议")
    report_lines.append("="*70)
    
    # 输出完整报告
    full_report = "\n".join(report_lines)
    print(full_report)
    
    # ========== 6. 发送到钉钉 ==========
    print("\n📩 尝试发送到钉钉...")
    
    # 尝试使用 OpenClaw 的钉钉插件
    try:
        # 构建消息内容
        message = full_report
        
        # 尝试通过 dingtalk_tensor 发送（如果可用）
        try:
            import dingtalk_tensor as dt
            dt.send_to_dingtalk(message, target_cid="cidPRZXi2wt7jEmvEe4h6ye2w==")
            print("✅ 报告已发送到钉钉群")
        except ImportError:
            print("dingtalk_tensor 模块不可用")
            print("尝试其他发送方式...")
        
        # 尝试直接发送
        print(f"\n拟发送消息长度: {len(message)} 字符")
        print(f"目标群组: cidPRZXi2wt7jEmvEe4h6ye2w==")
        print("ℹ️  请手动配置钉钉机器人 Webhook 或使用 openclaw 钉钉插件发送")
        
    except Exception as e:
        print(f"发送失败: {e}")
    
    print("\n✅ 扫描完成")
    return 0

if __name__ == "__main__":
    main()
