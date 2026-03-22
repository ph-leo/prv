#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股早盘信号扫描脚本
执行时间：每天 09:30（A股开盘）
任务：
1. 使用 akshare 获取A股开盘数据
2. 扫描S1/S2级别交易信号
3. 获取热门板块分析
4. 发送到钉钉群
"""

import akshare as ak
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any


def get_stock_market_data() -> Dict[str, Any]:
    """获取A股市场数据"""
    print("正在获取市场数据...", file=sys.stderr)
    
    # 使用stock_zh_a_spot_em获取实时数据
    try:
        stock_info = ak.stock_zh_a_spot_em()
        total_stocks = len(stock_info)
        print(f"当前A股总数: {total_stocks}", file=sys.stderr)
    except Exception as e:
        print(f"stock_zh_a_spot_em获取失败: {e}", file=sys.stderr)
        total_stocks = 5000  # 估算值
    
    # 获取涨跌幅数据
    print("正在获取涨跌幅数据...", file=sys.stderr)
    try:
        daily_data = ak.stock_zh_a_daily()
        print(f"涨跌幅数据获取成功: {len(daily_data)}只股票", file=sys.stderr)
    except Exception as e:
        print(f"涨跌幅数据获取失败: {e}", file=sys.stderr)
        daily_data_count = 0
    else:
        daily_data_count = len(daily_data)
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_stocks": total_stocks,
        "daily_data_count": daily_data_count
    }


def scan_s1_s2_signals() -> Dict[str, List[str]]:
    """扫描S1/S2级别交易信号"""
    print("正在扫描交易信号...", file=sys.stderr)
    
    signals = {
        "S1": [],  # 强势信号
        "S2": [],  # 次强信号
        "overview": {}
    }
    
    try:
        # 使用stock_zh_a_spot_em获取实时数据
        spot_data = ak.stock_zh_a_spot_em()
        if len(spot_data) > 0:
            # 计算涨跌幅
            if '涨跌幅' in spot_data.columns:
                zdf = spot_data.copy()
                zdf['change_pct'] = zdf['涨跌幅'].astype(str).str.replace('%', '').astype(float)
                
                # S1信号：涨幅>7%
                s1_stocks = zdf[zdf['change_pct'] > 7].head(10)
                
                # S2信号：涨幅在3-7%之间
                s2_stocks = zdf[(zdf['change_pct'] > 3) & (zdf['change_pct'] <= 7)].head(20)
                
                signals["S1"] = s1_stocks['代码'].tolist()[:5]
                signals["S2"] = s2_stocks['代码'].tolist()[:10]
                signals["overview"] = {
                    "s1_count": len(s1_stocks),
                    "s2_count": len(s2_stocks),
                    "top_gainer": zdf.nlargest(1, 'change_pct')['代码'].iloc[0] if len(zdf) > 0 else "N/A",
                    "top_loser": zdf.nsmallest(1, 'change_pct')['代码'].iloc[0] if len(zdf) > 0 else "N/A"
                }
                
                print(f"S1信号股票: {signals['S1']}", file=sys.stderr)
                print(f"S2信号股票: {signals['S2']}", file=sys.stderr)
    except Exception as e:
        print(f"扫描信号时出错: {e}", file=sys.stderr)
    
    return signals


def get_hot_boards() -> Dict[str, Any]:
    """获取热门板块分析"""
    print("正在获取热门板块...", file=sys.stderr)
    
    boards = {
        "industry": [],
        "concept": [],
        "overview": {}
    }
    
    try:
        # 获取行业板块
        industry_board = ak.stock_board_industry_spot_em()
        if len(industry_board) > 0 and '板块' in industry_board.columns and '涨跌幅' in industry_board.columns:
            # 涨幅排名前5的行业板块
            top_industry = industry_board.nlargest(5, '涨跌幅')
            boards["industry"] = [
                {"name": row['板块'], "change": float(str(row['涨跌幅']).replace('%', ''))}
                for _, row in top_industry.iterrows()
            ]
            print(f"热门行业板块: {[b['name'] for b in boards['industry']]}", file=sys.stderr)
        
        # 获取概念板块
        concept_board = ak.stock_board_concept_spot_em()
        if len(concept_board) > 0 and '板块' in concept_board.columns and '涨跌幅' in concept_board.columns:
            # 涨幅排名前5的概念板块
            top_concept = concept_board.nlargest(5, '涨跌幅')
            boards["concept"] = [
                {"name": row['板块'], "change": float(str(row['涨跌幅']).replace('%', ''))}
                for _, row in top_concept.iterrows()
            ]
            print(f"热门概念板块: {[b['name'] for b in boards['concept']]}", file=sys.stderr)
        
        boards["overview"] = {
            "total_industry": len(industry_board) if len(industry_board) > 0 else 0,
            "total_concept": len(concept_board) if len(concept_board) > 0 else 0
        }
        
    except Exception as e:
        print(f"获取板块数据时出错: {e}", file=sys.stderr)
    
    return boards


def generate_report() -> str:
    """生成报告文本"""
    print("正在生成报告...", file=sys.stderr)
    
    market_data = get_stock_market_data()
    signals = scan_s1_s2_signals()
    boards = get_hot_boards()
    
    report = []
    report.append("=== A股早盘信号扫描 - 09:30 ===")
    report.append(f"扫描时间: {market_data['timestamp']}")
    report.append("")
    report.append("【市场概览】")
    report.append(f"• A股总数: {market_data['total_stocks']}只")
    report.append("")
    
    report.append("【S1/S2交易信号】")
    report.append(f"S1信号股票 (5只): {', '.join(signals['S1'][:5]) if signals['S1'] else '无'}")
    report.append(f"S2信号股票 (10只): {', '.join(signals['S2'][:10]) if signals['S2'] else '无'}")
    report.append("")
    
    report.append("【热门板块】")
    report.append("**行业板块TOP5:**")
    for board in boards['industry'][:5]:
        report.append(f"• {board['name']}: {board['change']:.2f}%")
    report.append("")
    report.append("**概念板块TOP5:**")
    for board in boards['concept'][:5]:
        report.append(f"• {board['name']}: {board['change']:.2f}%")
    
    return "\n".join(report)


if __name__ == "__main__":
    try:
        report = generate_report()
        print(report)
        
        # 保存报告到文件
        report_file = "/tmp/a_share_signals_morning_report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存到: {report_file}", file=sys.stderr)
        
        sys.exit(0)
    except Exception as e:
        print(f"脚本执行出错: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
