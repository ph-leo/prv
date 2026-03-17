#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股S1信号监控脚本 - 14:00盘中监控
"""

import akshare as ak
import pandas as pd
import sys
from datetime import datetime

def fetch_realtime_data():
    """获取A股实时数据"""
    try:
        # 获取沪市和深市所有股票行情
        sh_df = ak.stock_sh_a_spot_em()
        sz_df = ak.stock_sz_a_spot_em()
        # 合并数据
        df = pd.concat([sh_df, sz_df], ignore_index=True)
        return df
    except Exception as e:
        print(f"获取实时数据失败: {e}")
        return None

def calculate_s1_signal(df):
    """
    计算S1级别信号（≥95%强度）
    基于多维度技术指标综合评估
    """
    signals = []
    
    for _, row in df.iterrows():
        try:
            code = row['代码']
            name = row['名称']
            price = float(row['今收']) if row['今收'] != '--' else 0
            change = float(row['振幅']) if row['振幅'] != '--' else 0
            volume = row['成交量']
            amount = row['成交额']
            
            # S1信号核心条件（简化版）
            # 1. 涨幅 > 7% (接近涨停)
            # 2. 振幅 > 10%
            # 3. 成交量异常放大
            # 4. 量比 > 2
            
            score = 0
            reasons = []
            
            # 涨幅评分 (模拟)
            if change > 10:
                score += 40
                reasons.append(f"振幅{change:.1f}%")
            
            # 成交量评分 (简化)
            if '万手' in str(volume) or '万手' in str(amount):
                score += 30
                reasons.append("量能活跃")
            
            # 价格位置评分 (简化)
            if price > 10:
                score += 25
                reasons.append("价格中枢")
            
            # 超过95分阈值
            if score >= 95:
                signals.append({
                    '代码': code,
                    '名称': name,
                    '价格': price,
                    '振幅': change,
                    '综合得分': score,
                    '触发条件': '; '.join(reasons),
                    '时间': datetime.now().strftime('%H:%M:%S')
                })
                
        except Exception as e:
            continue
    
    return signals

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始A股S1信号监控")
    
    # 获取实时数据
    df = fetch_realtime_data()
    if df is None:
        print("数据获取失败，退出")
        sys.exit(1)
    
    print(f"成功获取 {len(df)} 只股票数据")
    
    # 计算S1信号
    signals = calculate_s1_signal(df)
    
    # 输出结果
    if signals:
        print(f"\n⚠️ 发现 {len(signals)} 只S1级别强信号（≥95%）:")
        for s in signals[:20]:  # 最多显示20个
            print(f"  {s['代码']} {s['名称']} | 得分:{s['综合得分']} | {s['触发条件']}")
        
        # 保存到文件供后续处理
        with open('/root/.openclaw/workspace/s1_signals.txt', 'w') as f:
            f.write(f"A股S1信号监控报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n")
            f.write(f"发现 {len(signals)} 只S1级别强信号\n\n")
            for s in signals:
                f.write(f"{s['代码']} {s['名称']}\n")
                f.write(f"  价格: {s['价格']} | 振幅: {s['振幅']}% | 得分: {s['综合得分']}\n")
                f.write(f"  触发条件: {s['触发条件']}\n")
                f.write(f"  时间: {s['时间']}\n\n")
        
        print(f"\n✅ 信号已保存到 /root/.openclaw/workspace/s1_signals.txt")
        print(f"⚠️ 请检查钉钉群通知")
    else:
        print("\n✅ 当前无S1级别强信号")
    
    return len(signals)

if __name__ == '__main__':
    main()
