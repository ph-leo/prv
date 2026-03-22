#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股收盘总结生成器
每天15:05执行，生成当日收盘总结报告
"""

import akshare as ak
import pandas as pd
import time
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 配置
MAX_RETRY = 3
RETRY_DELAY = 5  # 秒

def retry_request(func, max_retry=MAX_RETRY, **kwargs):
    """带重试机制的请求函数"""
    for attempt in range(max_retry):
        try:
            result = func(**kwargs)
            if result is not None and len(result) > 0:
                return result
            else:
                print(f"尝试 {attempt + 1}/{max_retry}: 返回空结果")
        except Exception as e:
            print(f"尝试 {attempt + 1}/{max_retry}: 失败 - {e}")
            if attempt < max_retry - 1:
                print(f"等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
    return None


def get_stock_spot_data():
    """获取A股实时行情数据（老版本）"""
    print("正在获取A股实时行情数据...")
    try:
        df = ak.stock_zh_a_spot()
        print(f"成功获取 {len(df)} 只股票数据")
        return df
    except Exception as e:
        print(f"获取A股行情数据失败: {e}")
        return None


def get_board_concept_data():
    """获取概念板块数据"""
    print("正在获取概念板块数据...")
    try:
        df = ak.stock_board_concept_name_em()
        print(f"成功获取 {len(df)} 个概念板块")
        return df
    except Exception as e:
        print(f"获取概念板块数据失败: {e}")
        return None


def get_money_flow_data():
    """获取行业资金流向数据"""
    print("正在获取行业资金流向数据...")
    try:
        df = ak.stock_money_flow_industry_cn()
        print(f"成功获取 {len(df)} 个行业资金流向")
        return df
    except Exception as e:
        print(f"获取行业资金流向失败: {e}")
        return None


def get_stock_top_bottom(df, n=5):
    """获取涨跌幅居前/后的股票"""
    if df is None or len(df) == 0:
        return pd.DataFrame(), pd.DataFrame()
    
    # 转换涨跌幅列为数值类型
    try:
        df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
        df['最新价'] = pd.to_numeric(df['最新价'], errors='coerce')
    except:
        return pd.DataFrame(), pd.DataFrame()
    
    # 过滤有效数据
    valid_df = df.dropna(subset=['涨跌幅', '最新价']).copy()
    
    if len(valid_df) == 0:
        return pd.DataFrame(), pd.DataFrame()
    
    # 涨幅前N
    top_gainers = valid_df.nlargest(n, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
    
    # 跌幅前N
    top_losers = valid_df.nsmallest(n, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
    
    return top_gainers, top_losers


def get_active_stocks(df, n=5):
    """获取活跃股票（按成交量/成交额）"""
    if df is None or len(df) == 0:
        return pd.DataFrame()
    
    # 尝试获取成交额或成交量列
    columns = df.columns.str.lower()
    
    # 查找成交额列
    turnover_col = None
    volume_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if '成交额' in col_lower or 'amount' in col_lower:
            turnover_col = col
        if '成交量' in col_lower or 'volume' in col_lower:
            volume_col = col
    
    # 转换数值类型
    try:
        df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
        if turnover_col:
            df[turnover_col] = pd.to_numeric(df[turnover_col], errors='coerce')
    except:
        pass
    
    # 按成交额或成交量排序
    if turnover_col:
        active = df.dropna(subset=[turnover_col, '涨跌幅']).nlargest(n, turnover_col)
        return active[['代码', '名称', turnover_col, '涨跌幅']]
    elif volume_col:
        active = df.dropna(subset=[volume_col, '涨跌幅']).nlargest(n, volume_col)
        return active[['代码', '名称', volume_col, '涨跌幅']]
    else:
        # 如果没有成交数据，返回任意N只
        return df.head(n)[['代码', '名称', '涨跌幅']]


def format_price(price):
    """格式化价格"""
    if pd.isna(price) or price is None:
        return "NaN"
    return f"{price:.2f}"


def format_percent(percent):
    """格式化百分比"""
    if pd.isna(percent) or percent is None:
        return "NaN"
    return f"{percent:.2f}%" if percent >= 0 else f"{percent:.2f}%"


def format_amount(amount):
    """格式化成交额"""
    if pd.isna(amount) or amount is None:
        return "NaN"
    if amount >= 1e8:
        return f"{amount/1e8:.2f}亿"
    elif amount >= 1e4:
        return f"{amount/1e4:.2f}万"
    return f"{amount:.0f}"


def generate_report():
    """生成收盘总结报告"""
    print("=" * 50)
    print("开始生成A股收盘总结报告")
    print("=" * 50)
    
    report_lines = []
    report_lines.append("【收盘总结】")
    
    # 1. 获取A股行情数据
    stock_df = retry_request(get_stock_spot_data)
    
    if stock_df is None or len(stock_df) == 0:
        report_lines.append("❌ 无法获取A股行情数据")
        return "\n".join(report_lines)
    
    # 2. 分析大盘走势
    try:
        stock_df['涨跌幅'] = pd.to_numeric(stock_df['涨跌幅'], errors='coerce')
        stock_df['最新价'] = pd.to_numeric(stock_df['最新价'], errors='coerce')
    except:
        pass
    
    valid_df = stock_df.dropna(subset=['涨跌幅'])
    
    if len(valid_df) > 0:
        up_count = len(valid_df[valid_df['涨跌幅'] > 0])
        down_count = len(valid_df[valid_df['涨跌幅'] < 0])
        flat_count = len(valid_df[valid_df['涨跌幅'] == 0])
        total_count = len(valid_df)
        
        avg_change = valid_df['涨跌幅'].mean()
        
        report_lines.append(f"大盘：{up_count}涨/{down_count}跌/{flat_count}平，共{total_count}只股票")
        report_lines.append(f"平均涨跌幅：{avg_change:+.2f}%")
    else:
        report_lines.append("❌ 无法计算涨跌情况")
    
    report_lines.append("")
    
    # 3. 涨跌家数
    report_lines.append(f"涨跌家数：涨 {up_count} 家 / 跌 {down_count} 家")
    report_lines.append("")
    
    # 4. 获取板块数据
    board_df = retry_request(get_board_concept_data)
    
    if board_df is not None and len(board_df) > 0:
        try:
            board_df['涨跌幅'] = pd.to_numeric(board_df['涨跌幅'], errors='coerce')
            top_boards = board_df.dropna(subset=['涨跌幅']).nlargest(5, '涨跌幅')
            
            if len(top_boards) > 0:
                report_lines.append("板块：热点板块回顾")
                for _, row in top_boards.iterrows():
                    board_name = row['板块']
                    board_change = row['涨跌幅']
                    report_lines.append(f"  • {board_name}: {format_percent(board_change)}")
        except Exception as e:
            print(f"板块分析失败: {e}")
    
    report_lines.append("")
    
    # 5. 北向资金流向
    money_df = retry_request(get_money_flow_data)
    
    if money_df is not None and len(money_df) > 0:
        try:
            money_df['今日净流量'] = pd.to_numeric(money_df['今日净流量'], errors='coerce')
            north_money = money_df['今日净流量'].sum()
            
            if north_money >= 0:
                report_lines.append(f"北向资金：流入 {format_amount(north_money)}")
            else:
                report_lines.append(f"北向资金：流出 {format_amount(abs(north_money))}")
        except Exception as e:
            print(f"北向资金分析失败: {e}")
    else:
        report_lines.append("北向资金：数据获取失败")
    
    report_lines.append("")
    
    # 6. 涨幅前5
    report_lines.append("涨幅前5：")
    top_gainers, top_losers = get_stock_top_bottom(stock_df, n=5)
    
    if len(top_gainers) > 0:
        for _, row in top_gainers.iterrows():
            code = row['代码']
            name = row['名称']
            change = row['涨跌幅']
            price = row['最新价']
            report_lines.append(f"  • {code} {name}: {format_percent(change)} ({format_price(price)}元)")
    else:
        report_lines.append("  • 暂无数据")
    
    report_lines.append("")
    
    # 7. 跌幅前5
    report_lines.append("跌幅前5：")
    if len(top_losers) > 0:
        for _, row in top_losers.iterrows():
            code = row['代码']
            name = row['名称']
            change = row['涨跌幅']
            price = row['最新价']
            report_lines.append(f"  • {code} {name}: {format_percent(change)} ({format_price(price)}元)")
    else:
        report_lines.append("  • 暂无数据")
    
    report_lines.append("")
    
    # 8. 活跃前5
    report_lines.append("活跃前5：")
    active_stocks = get_active_stocks(stock_df, n=5)
    
    if len(active_stocks) > 0:
        for _, row in active_stocks.iterrows():
            code = row['代码']
            name = row['名称']
            change = row.get('涨跌幅', 0)
            turnover = None
            for col in row.index:
                if '成交' in col or 'amount' in col.lower():
                    turnover = row[col]
                    break
            
            if turnover:
                report_lines.append(f"  • {code} {name}: 成交额 {format_amount(turnover)} ({format_percent(change)})")
            else:
                report_lines.append(f"  • {code} {name}: {format_percent(change)}")
    else:
        report_lines.append("  • 暂无数据")
    
    report_lines.append("")
    
    # 9. 明日展望
    report_lines.append("明日展望：")
    
    if len(valid_df) > 0:
        if avg_change > 0:
            report_lines.append("  • 大盘上涨，市场情绪乐观，关注成交量变化")
        elif avg_change < 0:
            report_lines.append("  • 大盘下跌，市场情绪谨慎，注意风险控制")
        else:
            report_lines.append("  • 大盘震荡，市场观望情绪浓厚")
    
    report_lines.append("  • 建议关注：热点板块轮动、成交量变化、北向资金流向")
    report_lines.append("  • 风险提示：股市有风险，投资需谨慎")
    
    report_lines.append("")
    report_lines.append("数据源：akshare（东方财富/同花顺）")
    
    return "\n".join(report_lines)


def main():
    """主函数"""
    start_time = time.time()
    
    # 生成报告
    report = generate_report()
    
    elapsed_time = time.time() - start_time
    print(f"\n报告生成完成，耗时: {elapsed_time:.2f}秒")
    print("=" * 50)
    print(report)
    print("=" * 50)
    
    # 保存报告到文件
    report_file = f"/root/.openclaw/workspace/skills/trading-simulation/reports/收盘总结_{datetime.now().strftime('%Y%m%d')}.md"
    try:
        import os
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {report_file}")
    except Exception as e:
        print(f"保存报告失败: {e}")
    
    return report


if __name__ == "__main__":
    main()
