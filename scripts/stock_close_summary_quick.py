#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股收盘总结生成器 - 快速版
- 跳过耗时接口（热点板块、北向资金）
- 只获取核心数据
- 容错处理
"""

import akshare as ak
import sys
import time
import traceback
from datetime import datetime
import pandas as pd

# ============== 配置 ==============
MAX_RETRIES = 3
RETRY_DELAY = 2

# ============== 工具函数 ==============
def retry_request(func, *args, **kwargs):
    """带重试机制的请求函数"""
    for attempt in range(MAX_RETRIES):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"重试 {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(RETRY_DELAY)
            else:
                print(f"所有重试失败: {e}")
                return None
    return None

# ============== 核心数据获取 ==============
def get_zh_a_spot():
    """获取A股实时行情"""
    print("正在获取A股实时行情...")
    try:
        df = ak.stock_zh_a_spot()
        return df
    except Exception as e:
        print(f"获取A股行情失败: {e}")
        return None

def get_board_concept_names():
    """获取概念板块名称"""
    print("正在获取板块数据...")
    try:
        df = ak.stock_board_concept_name_em()
        return df
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        return None

def get_fund_flow():
    """获取资金流向"""
    print("正在获取资金流向...")
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            return {
                "direction": "流入" if float(str(row.get('沪深港通资金流向', 0)).replace(',', '')) >= 0 else "流出",
                "amount": str(row.get('沪深港通资金流向', '0'))
            }
        return None
    except Exception as e:
        print(f"获取资金流向失败: {e}")
        return None

# ============== 报告生成 ==============
def generate_report():
    """生成收盘总结报告"""
    report = []
    report.append("【收盘总结】")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 1. 获取A股行情
    df_spot = retry_request(get_zh_a_spot)
    
    if df_spot is not None and len(df_spot) > 0:
        # 处理涨跌幅
        df_spot['涨跌幅'] = pd.to_numeric(df_spot['涨跌幅'], errors='coerce')
        df_spot = df_spot.dropna(subset=['涨跌幅'])
        
        up_count = len(df_spot[df_spot['涨跌幅'] > 0])
        down_count = len(df_spot[df_spot['涨跌幅'] < 0])
        flat_count = len(df_spot[df_spot['涨跌幅'] == 0])
        
        report.append("【大盘走势】")
        report.append(f"涨跌家数: 涨 {up_count} 家 / 跌 {down_count} 家 / 平 {flat_count} 家")
        report.append("")
        
        # 涨幅前5
        try:
            df_top = df_spot.nlargest(5, '涨跌幅')[['代码', '名称', '涨跌幅']]
            report.append("【涨幅前5】")
            for _, row in df_top.iterrows():
                report.append(f"  {row['代码']} - {row['名称']} - {row['涨跌幅']}%")
            report.append("")
        except Exception as e:
            print(f"涨幅前5获取失败: {e}")
        
        # 跌幅前5
        try:
            df_bottom = df_spot.nsmallest(5, '涨跌幅')[['代码', '名称', '涨跌幅']]
            report.append("【跌幅前5】")
            for _, row in df_bottom.iterrows():
                report.append(f"  {row['代码']} - {row['名称']} - {row['涨跌幅']}%")
            report.append("")
        except Exception as e:
            print(f"跌幅前5获取失败: {e}")
        
        # 成交量前5
        try:
            df_spot['成交量'] = pd.to_numeric(df_spot['成交量'], errors='coerce')
            df_spot = df_spot.dropna(subset=['成交量'])
            df_volume = df_spot.nlargest(5, '成交量')[['代码', '名称', '成交量']]
            report.append("【活跃股票(成交量)】")
            for _, row in df_volume.iterrows():
                report.append(f"  {row['代码']} - {row['名称']} - {row['成交量']}手")
            report.append("")
        except Exception as e:
            print(f"成交量前5获取失败: {e}")
    else:
        report.append("【大盘走势】")
        report.append("（实时数据获取失败）")
        report.append("")
        up_count = 0
        down_count = 0
    
    # 2. 板块数据（可选）
    board_df = retry_request(get_board_concept_names)
    if board_df is not None and len(board_df) > 0:
        report.append("【热点板块】")
        for _, row in board_df.head(5).iterrows():
            name = row.get('板块名称', row.get('name', '未知'))
            report.append(f"  {name}")
        report.append("")
    else:
        report.append("【热点板块】")
        report.append("（板块数据获取中）")
        report.append("")
    
    # 3. 资金流向（可选）
    funds = retry_request(get_fund_flow)
    if funds is not None:
        report.append(f"【北向资金】{funds['direction']} {funds['amount']}")
        report.append("")
    
    # 4. 明日展望
    report.append("【明日展望】")
    try:
        if up_count > down_count * 1.2:
            report.append("市场情绪积极，多数股票上涨，预计明日可能延续涨势。")
        elif down_count > up_count * 1.2:
            report.append("市场情绪低迷，多数股票下跌，预计明日可能继续调整。")
        else:
            report.append("市场涨跌平衡，预计明日维持震荡走势。")
    except:
        report.append("市场分析基于可用数据，预计明日维持震荡走势。")
    report.append("")
    
    report.append("---")
    report.append("数据源: akshare (东方财富)")
    
    return "\n".join(report)

# ============== 主程序 ==============
if __name__ == "__main__":
    print("开始生成A股收盘总结（快速版）...")
    
    try:
        report = generate_report()
        print("\n" + "=" * 60)
        print("报告生成成功！")
        print("=" * 60)
        print(report)
        print("=" * 60)
        
        # 保存报告
        today = datetime.now().strftime('%Y-%m-%d')
        report_file = f"/root/.openclaw/workspace/memory/{today}.md"
        with open(report_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n## A股收盘总结 {today}\n")
            f.write(report)
            f.write(f"\n\n_生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
        
        print(f"\n报告已保存到 {report_file}")
        
        # 同时保存到临时文件（供钉钉Bot使用）
        with open("/root/.openclaw/workspace/stock_summary.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("报告已保存到 /root/.openclaw/workspace/stock_summary.txt")
        
    except Exception as e:
        print(f"生成报告失败: {e}")
        traceback.print_exc()
        sys.exit(1)
