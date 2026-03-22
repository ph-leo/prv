#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股收盘总结 - 带钉钉发送功能
每天15:05执行，生成当日收盘总结报告并发送到钉钉群
"""

import akshare as ak
import pandas as pd
import time
import sys
import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# 配置
MAX_RETRY = 3
RETRY_DELAY = 3  # 秒

# 钉钉配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send"
DINGTALK_ACCESS_TOKEN = "openclaw_secure_token_2026"
DINGTALK_CHAT_ID = None  # 1458302740827526 (钉钉群ID)

def retry_request(func, max_retry=MAX_RETRY, **kwargs):
    """带重试机制的请求函数"""
    for attempt in range(max_retry):
        try:
            result = func(**kwargs)
            if result is not None and len(result) > 0:
                return result
            else:
                print(f"[重试 {attempt + 1}/{max_retry}] 返回空结果")
        except Exception as e:
            print(f"[重试 {attempt + 1}/{max_retry}] 失败 - {e}")
            if attempt < max_retry - 1:
                print(f"等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
    return None


def get_stock_spot_old():
    """获取A股实时行情数据（老版本，stock_zh_a_spot）"""
    print("正在获取A股实时行情数据（老版本）...")
    try:
        df = ak.stock_zh_a_spot()
        print(f"成功获取 {len(df)} 只股票数据")
        return df
    except Exception as e:
        print(f"获取A股行情数据失败: {e}")
        return None


def get_board_concept():
    """获取概念板块数据"""
    print("正在获取概念板块数据...")
    try:
        df = ak.stock_board_concept_name_em()
        print(f"成功获取 {len(df)} 个概念板块")
        return df
    except Exception as e:
        print(f"获取概念板块失败: {e}")
        return None


def get_board_industry():
    """获取行业板块数据"""
    print("正在获取行业板块数据...")
    try:
        df = ak.stock_board_industry_name_em()
        print(f"成功获取 {len(df)} 个行业板块")
        return df
    except Exception as e:
        print(f"获取行业板块失败: {e}")
        return None


def get_money_flow_industry():
    """获取行业资金流向"""
    print("正在获取行业资金流向...")
    try:
        df = ak.stock_money_flow_industry_cn()
        print(f"成功获取 {len(df)} 个行业资金流向")
        return df
    except Exception as e:
        print(f"获取行业资金流向失败: {e}")
        return None


def parse_stock_spot_data(df):
    """解析股票行情数据"""
    if df is None or len(df) == 0:
        return None
    
    # 转换关键列
    try:
        df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
        df['最新价'] = pd.to_numeric(df['最新价'], errors='coerce')
        df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
        df['成交额'] = pd.to_numeric(df['成交额'], errors='coerce')
    except:
        pass
    
    return df


def analyze_market(df):
    """分析市场情况"""
    if df is None or len(df) == 0:
        return None
    
    valid_df = df.dropna(subset=['涨跌幅'])
    if len(valid_df) == 0:
        return None
    
    up_count = len(valid_df[valid_df['涨跌幅'] > 0])
    down_count = len(valid_df[valid_df['涨跌幅'] < 0])
    flat_count = len(valid_df[valid_df['涨跌幅'] == 0])
    total_count = len(valid_df)
    
    avg_change = valid_df['涨跌幅'].mean() if len(valid_df) > 0 else 0
    
    return {
        'up_count': up_count,
        'down_count': down_count,
        'flat_count': flat_count,
        'total_count': total_count,
        'avg_change': avg_change
    }


def get_top_stocks(df, n=5, ascending=False):
    """获取涨跌幅居前的股票"""
    if df is None or len(df) == 0:
        return pd.DataFrame()
    
    try:
        df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    except:
        return pd.DataFrame()
    
    valid_df = df.dropna(subset=['涨跌幅', '代码', '名称'])
    if len(valid_df) == 0:
        return pd.DataFrame()
    
    if ascending:
        result = valid_df.nsmallest(n, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
    else:
        result = valid_df.nlargest(n, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
    
    return result


def get_active_stocks(df, n=5):
    """获取活跃股票"""
    if df is None or len(df) == 0:
        return pd.DataFrame()
    
    # 查找成交额或成交量列
    turnover_col = None
    for col in df.columns:
        if '成交' in col and '额' in col:
            turnover_col = col
            break
        elif 'amount' in col.lower() or 'turnover' in col.lower():
            turnover_col = col
            break
    
    if turnover_col:
        try:
            df[turnover_col] = pd.to_numeric(df[turnover_col], errors='coerce')
        except:
            return pd.DataFrame()
        
        valid_df = df.dropna(subset=[turnover_col, '代码', '名称'])
        if len(valid_df) == 0:
            return pd.DataFrame()
        
        result = valid_df.nlargest(n, turnover_col)[['代码', '名称', turnover_col, '涨跌幅']]
        return result
    
    return pd.DataFrame()


def format_value(value, decimals=2):
    """格式化数值"""
    if pd.isna(value) or value is None:
        return "NaN"
    if isinstance(value, str):
        return value
    return f"{value:.{decimals}f}"


def format_amount(amount):
    """格式化金额"""
    if pd.isna(amount) or amount is None:
        return "NaN"
    try:
        amount = float(amount)
        if amount >= 1e8:
            return f"{amount/1e8:.2f}亿"
        elif amount >= 1e4:
            return f"{amount/1e4:.2f}万"
        return f"{amount:.0f}"
    except:
        return str(amount)


def send_to_dingtalk(message, chat_id=None):
    """发送消息到钉钉群"""
    try:
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "msgtype": "text",
            "text": {"content": message},
            "at": {"isAtAll": False}
        }
        
        url = f"{DINGTALK_WEBHOOK}?access_token={DINGTALK_ACCESS_TOKEN}"
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        print(f"发送结果: {result}")
        return result
    except Exception as e:
        print(f"发送失败: {e}")
        return {"error": str(e)}


def generate_report():
    """生成收盘总结报告"""
    print("=" * 60)
    print("开始生成A股收盘总结报告")
    print("=" * 60)
    
    report_lines = []
    report_lines.append("【收盘总结】")
    
    has_data = False
    stock_df = None
    board_df = None
    money_df = None
    
    # 1. 尝试获取多个数据源
    print("\n--- 数据获取阶段 ---")
    
    stock_df = retry_request(get_stock_spot_old)
    
    for func in [get_board_concept, get_board_industry]:
        board_df = retry_request(func)
        if board_df is not None and len(board_df) > 0:
            print(f"成功获取板块数据")
            break
    
    money_df = retry_request(get_money_flow_industry)
    
    # 2. 分析市场
    print("\n--- 市场分析阶段 ---")
    market_info = analyze_market(stock_df)
    
    if market_info:
        has_data = True
        up = market_info['up_count']
        down = market_info['down_count']
        flat = market_info['flat_count']
        total = market_info['total_count']
        avg = market_info['avg_change']
        
        report_lines.append(f"大盘：{up}涨/{down}跌/{flat}平，共{total}只股票")
        report_lines.append(f"平均涨跌幅：{avg:+.2f}%")
    else:
        report_lines.append("❌ 无法获取A股行情数据")
        report_lines.append("说明：当前可能无法访问东方财富等数据源")
        report_lines.append("建议：稍后重试或使用其他数据源")
    
    report_lines.append("")
    
    if market_info:
        up = market_info['up_count']
        down = market_info['down_count']
        report_lines.append(f"涨跌家数：涨 {up} 家 / 跌 {down} 家")
    report_lines.append("")
    
    # 3. 板块分析
    if board_df is not None and len(board_df) > 0:
        try:
            board_df['涨跌幅'] = pd.to_numeric(board_df['涨跌幅'], errors='coerce')
            top_boards = board_df.dropna(subset=['涨跌幅']).nlargest(5, '涨跌幅')
            
            if len(top_boards) > 0:
                report_lines.append("板块：热点板块回顾")
                for _, row in top_boards.iterrows():
                    name = row.get('板块', row.get('板块名称', ''))
                    change = row.get('涨跌幅', 0)
                    report_lines.append(f"  • {name}: {format_value(change)}%")
        except Exception as e:
            print(f"板块分析失败: {e}")
    else:
        report_lines.append("板块：数据获取失败")
    report_lines.append("")
    
    # 4. 北向资金
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
            report_lines.append("北向资金：数据获取失败")
    else:
        report_lines.append("北向资金：数据获取失败")
    report_lines.append("")
    
    # 5. 涨幅前5
    report_lines.append("涨幅前5：")
    if stock_df is not None and len(stock_df) > 0:
        try:
            stock_df['涨跌幅'] = pd.to_numeric(stock_df['涨跌幅'], errors='coerce')
            stock_df['最新价'] = pd.to_numeric(stock_df['最新价'], errors='coerce')
        except:
            pass
        
        valid_df = stock_df.dropna(subset=['涨跌幅', '代码', '名称'])
        if len(valid_df) > 0:
            top5 = valid_df.nlargest(5, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
            for _, row in top5.iterrows():
                code = row['代码']
                name = row['名称']
                change = row['涨跌幅']
                price = row['最新价']
                report_lines.append(f"  • {code} {name}: {format_value(change)}% ({format_value(price)}元)")
        else:
            report_lines.append("  • 暂无数据")
    else:
        report_lines.append("  • 暂无数据")
    report_lines.append("")
    
    # 6. 跌幅前5
    report_lines.append("跌幅前5：")
    if stock_df is not None and len(stock_df) > 0:
        try:
            valid_df = stock_df.dropna(subset=['涨跌幅', '代码', '名称'])
            if len(valid_df) > 0:
                bottom5 = valid_df.nsmallest(5, '涨跌幅')[['代码', '名称', '涨跌幅', '最新价']]
                for _, row in bottom5.iterrows():
                    code = row['代码']
                    name = row['名称']
                    change = row['涨跌幅']
                    price = row['最新价']
                    report_lines.append(f"  • {code} {name}: {format_value(change)}% ({format_value(price)}元)")
            else:
                report_lines.append("  • 暂无数据")
        except:
            report_lines.append("  • 暂无数据")
    else:
        report_lines.append("  • 暂无数据")
    report_lines.append("")
    
    # 7. 活跃前5
    report_lines.append("活跃前5：")
    if stock_df is not None and len(stock_df) > 0:
        turnover_col = None
        for col in stock_df.columns:
            if '成交' in col and '额' in col:
                turnover_col = col
                break
        
        if turnover_col:
            try:
                stock_df[turnover_col] = pd.to_numeric(stock_df[turnover_col], errors='coerce')
                valid_df = stock_df.dropna(subset=[turnover_col, '代码', '名称'])
                if len(valid_df) > 0:
                    active5 = valid_df.nlargest(5, turnover_col)[['代码', '名称', turnover_col, '涨跌幅']]
                    for _, row in active5.iterrows():
                        code = row['代码']
                        name = row['名称']
                        turnover = row[turnover_col]
                        change = row.get('涨跌幅', 0)
                        report_lines.append(f"  • {code} {name}: {format_amount(turnover)} ({format_value(change)}%)")
                    has_data = True
                else:
                    report_lines.append("  • 暂无数据")
            except:
                report_lines.append("  • 暂无数据")
        else:
            report_lines.append("  • 暂无数据")
    else:
        report_lines.append("  • 暂无数据")
    report_lines.append("")
    
    # 8. 明日展望
    report_lines.append("明日展望：")
    if market_info:
        avg = market_info['avg_change']
        if avg > 0:
            report_lines.append("  • 大盘上涨，市场情绪乐观")
        elif avg < 0:
            report_lines.append("  • 大盘下跌，市场情绪谨慎")
        else:
            report_lines.append("  • 大盘震荡，市场观望情绪浓厚")
    
    report_lines.append("  • 建议关注：热点板块轮动、成交量变化")
    report_lines.append("  • 风险提示：股市有风险，投资需谨慎")
    report_lines.append("")
    report_lines.append("数据源：akshare（东方财富/同花顺）")
    report_lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(report_lines), has_data


def save_report(report, has_data):
    """保存报告"""
    reports_dir = "/root/.openclaw/workspace/skills/trading-simulation/reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d')
    report_file = f"{reports_dir}/收盘总结_{timestamp}.md"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {report_file}")
        
        if has_data:
            workspace_file = "/root/.openclaw/workspace/收盘总结_今日.md"
            with open(workspace_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到: {workspace_file}")
            
    except Exception as e:
        print(f"保存报告失败: {e}")


def main():
    """主函数"""
    start_time = time.time()
    
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 生成报告
    report, has_data = generate_report()
    
    elapsed_time = time.time() - start_time
    print(f"\n报告生成完成，耗时: {elapsed_time:.2f}秒")
    print("=" * 60)
    print(report)
    print("=" * 60)
    
    # 保存报告
    save_report(report, has_data)
    
    # 发送到钉钉群
    print("\n--- 发送到钉钉群 ---")
    result = send_to_dingtalk(report)
    
    if result.get("errcode") == 0:
        print("✓ 消息已成功发送到钉钉群")
    else:
        print(f"✗ 发送失败: {result.get('errmsg', '未知错误')}")
    
    return report, has_data


if __name__ == "__main__":
    report, has_data = main()
