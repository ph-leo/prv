#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股每日收盘总结报告生成器
执行时间：每天 15:05
"""

import akshare as ak
import pandas as pd
import requests
import time
import sys
from typing import Dict, List, Optional
from datetime import datetime
import traceback

# 钉钉机器人配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=91322610c217c67236b9d12a8dfe0603c3d961615d2263118b9a001704470664"

def send_dingtalk_message(message: str) -> bool:
    """发送钉钉消息"""
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【收盘总结】" + datetime.now().strftime("%Y-%m-%d"),
                "text": message
            },
            "at": {
                "isAtAll": False
            }
        }
        response = requests.post(DINGTALK_WEBHOOK, json=data, headers=headers, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"发送钉钉消息失败: {e}")
        return False

def retry_request(max_retries: int = 3, delay: float = 2.0):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"第 {attempt + 1} 次失败，{delay}秒后重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry_request(max_retries=3, delay=2)
def get_stock_zh_index_spot_em() -> pd.DataFrame:
    """获取指数实时行情（东方财富）"""
    return ak.stock_zh_index_spot_em()

@retry_request(max_retries=3, delay=2)
def get_stock_zh_a_spot_em() -> pd.DataFrame:
    """获取A股实时行情（东方财富）"""
    return ak.stock_zh_a_spot_em()

@retry_request(max_retries=3, delay=2)
def get_stock_board_industry_spot_em() -> pd.DataFrame:
    """获取行业板块实时行情（东方财富）"""
    return ak.stock_board_industry_spot_em()

@retry_request(max_retries=3, delay=2)
def get_stock_hsgt_daily() -> pd.DataFrame:
    """获取沪深港通资金流向（东方财富）"""
    return ak.stock_hsgt_flow_em()

class StockSummaryGenerator:
    def __init__(self):
        self.data = {}
        self.errors = []
        
    def fetch_all_data(self):
        """获取所有数据源"""
        print("开始获取A股数据...")
        
        # 1. 获取指数数据（上证指数）
        try:
            df = get_stock_zh_index_spot_em()
            sz_df = df[df['代码'] == 'sh000001']
            if len(sz_df) > 0:
                self.data['index'] = sz_df.iloc[0]
                print(f"✅ 上证指数数据: {self.data['index']['今开']}")
            else:
                self.errors.append("上证指数数据不存在")
                print("❌ 上证指数数据获取失败")
        except Exception as e:
            self.errors.append(f"指数数据获取失败: {e}")
            print(f"❌ 指数数据获取失败: {e}")
        
        # 2. 获取实时行情（用于涨跌统计）
        try:
            df = get_stock_zh_a_spot_em()
            self.data['spot'] = df
            print(f"✅ A股实时行情数据: {len(df)} 行")
        except Exception as e:
            self.errors.append(f"A股实时行情数据获取失败: {e}")
            print(f"❌ A股实时行情数据获取失败: {e}")
        
        # 3. 获取行业板块数据
        try:
            df = get_stock_board_industry_spot_em()
            self.data['board'] = df
            print(f"✅ 行业板块数据: {len(df)} 行")
        except Exception as e:
            self.errors.append(f"行业板块数据获取失败: {e}")
            print(f"❌ 行业板块数据获取失败: {e}")
        
        # 4. 获取沪深港通资金流向
        try:
            df = get_stock_hsgt_daily()
            self.data['hsgt'] = df
            print(f"✅ 沪深港通资金流向数据: {len(df)} 行")
        except Exception as e:
            self.errors.append(f"沪深港通资金流向数据获取失败: {e}")
            print(f"❌ 沪深港通资金流向数据获取失败: {e}")
        
        # 5. 获取涨幅、跌幅、成交量数据
        try:
            df = get_stock_zh_a_spot_em()
            df_sorted = df.sort_values(by='涨跌幅', ascending=False)
            self.data['increase'] = df_sorted.head(5)
            print(f"✅ 涨幅前5数据: 已获取")
        except Exception as e:
            self.errors.append(f"涨幅数据获取失败: {e}")
            print(f"❌ 涨幅数据获取失败: {e}")
        
        try:
            df = get_stock_zh_a_spot_em()
            df_sorted = df.sort_values(by='涨跌幅', ascending=True)
            self.data['decrease'] = df_sorted.head(5)
            print(f"✅ 跌幅前5数据: 已获取")
        except Exception as e:
            self.errors.append(f"跌幅数据获取失败: {e}")
            print(f"❌ 跌幅数据获取失败: {e}")
        
        try:
            df = get_stock_zh_a_spot_em()
            df_sorted = df.sort_values(by='成交量', ascending=False)
            self.data['volume'] = df_sorted.head(5)
            print(f"✅ 成交量前5数据: 已获取")
        except Exception as e:
            self.errors.append(f"成交量数据获取失败: {e}")
            print(f"❌ 成交量数据获取失败: {e}")
        
        print(f"\n共获取 {len(self.data)} 个数据集，{len(self.errors)} 个错误")
        
    def generate_report(self) -> str:
        """生成收盘总结报告"""
        report_lines = []
        
        # 标题
        report_lines.append(f"## 📊 {datetime.now().strftime('%Y年%m月%d日')} A股收盘总结\n")
        
        # 1. 大盘走势
        report_lines.append("### 📈 大盘走势")
        try:
            if 'index' in self.data:
                idx = self.data['index']
                report_lines.append(f"- **上证指数**: {idx.get('最新价', 'N/A')} 点")
                report_lines.append(f"- **涨跌幅**: {idx.get('涨跌幅', 'N/A')}%")
                report_lines.append(f"- **涨跌额**: {idx.get('涨跌额', 'N/A')} 点")
            else:
                report_lines.append("- **上证指数**: 数据获取失败")
        except Exception as e:
            report_lines.append(f"- **上证指数**: 数据异常 - {e}")
        
        report_lines.append("")
        
        # 2. 涨跌家数
        report_lines.append("### 📊 涨跌家数")
        if 'spot' in self.data:
            df = self.data['spot']
            # 统计涨跌家数
            up_count = len(df[df['涨跌幅'] > 0])
            down_count = len(df[df['涨跌幅'] < 0])
            flat_count = len(df[df['涨跌幅'] == 0])
            total = len(df)
            
            report_lines.append(f"- **涨家数**: {up_count} 家")
            report_lines.append(f"- **跌家数**: {down_count} 家")
            report_lines.append(f"- **平家数**: {flat_count} 家")
            report_lines.append(f"- **总计**: {total} 家")
            
            # 涨跌比
            if down_count > 0:
                ratio = round(up_count / down_count, 2)
                report_lines.append(f"- **涨跌比**: {ratio}")
        else:
            report_lines.append("- 涨跌家数数据: 获取失败")
        
        report_lines.append("")
        
        # 3. 热点板块 (前5)
        report_lines.append("### 💡 热点板块")
        try:
            if 'board' in self.data:
                df = self.data['board']
                # 按涨跌幅排序
                df_sorted = df.sort_values(by='涨跌幅', ascending=False).head(5)
                for idx, row in df_sorted.iterrows():
                    board_name = row.get('板块', 'N/A')
                    change = row.get('涨跌幅', 'N/A')
                    report_lines.append(f"- {board_name}: {change}%")
            else:
                report_lines.append("- 行业板块数据: 获取失败")
        except Exception as e:
            report_lines.append(f"- 行业板块数据异常: {e}")
        
        report_lines.append("")
        
        # 4. 北向资金
        report_lines.append("### 💰 北向资金")
        try:
            if 'hsgt' in self.data:
                df = self.data['hsgt']
                if len(df) > 0:
                    row = df.iloc[0]
                    # 获取最近的沪深港通资金流向
                    report_lines.append(f"- **沪深300指数**: {row.get('收盘价', 'N/A')}")
                    report_lines.append(f"- **涨跌幅**: {row.get('涨跌幅', 'N/A')}%")
                else:
                    report_lines.append("- 沪深港通资金流向数据: 空")
            else:
                report_lines.append("- 北向资金: 数据获取失败")
        except Exception as e:
            report_lines.append(f"- 北向资金异常: {e}")
        
        report_lines.append("")
        
        # 5. 涨幅前5
        report_lines.append("### 📈 涨幅前5")
        try:
            if 'increase' in self.data:
                df = self.data['increase']
                for idx, row in df.iterrows():
                    code = row.get('代码', 'N/A')
                    name = row.get('名称', 'N/A')
                    price = row.get('最新价', 'N/A')
                    change = row.get('涨跌幅', 'N/A')
                    report_lines.append(f"- `{code}` {name}: {price}元 (+{change}%)")
            else:
                report_lines.append("- 涨幅数据: 获取失败")
        except Exception as e:
            report_lines.append(f"- 涨幅数据异常: {e}")
        
        report_lines.append("")
        
        # 6. 跌幅前5
        report_lines.append("### 📉 跌幅前5")
        try:
            if 'decrease' in self.data:
                df = self.data['decrease']
                for idx, row in df.iterrows():
                    code = row.get('代码', 'N/A')
                    name = row.get('名称', 'N/A')
                    price = row.get('最新价', 'N/A')
                    change = row.get('涨跌幅', 'N/A')
                    report_lines.append(f"- `{code}` {name}: {price}元 ({change}%)")
            else:
                report_lines.append("- 跌幅数据: 获取失败")
        except Exception as e:
            report_lines.append(f"- 跌幅数据异常: {e}")
        
        report_lines.append("")
        
        # 7. 成交量前5
        report_lines.append("### 📊 成交量前5")
        try:
            if 'volume' in self.data:
                df = self.data['volume']
                for idx, row in df.iterrows():
                    code = row.get('代码', 'N/A')
                    name = row.get('名称', 'N/A')
                    volume = row.get('成交量', 'N/A')
                    report_lines.append(f"- `{code}` {name}: {volume}手")
            else:
                report_lines.append("- 成交量数据: 获取失败")
        except Exception as e:
            report_lines.append(f"- 成交量数据异常: {e}")
        
        report_lines.append("")
        
        # 8. 明日展望
        report_lines.append("### 🔮 明日展望")
        report_lines.append("""
**市场展望:**
- 关注北向资金流向变化
- 观察热点板块持续性
- 留意量能变化
- 注意市场情绪转向

**风险提示:**
- 近期市场波动加大
- 注意仓位控制
- 避免追高杀跌
- 关注政策面消息
        """.strip())
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("数据源: akshare (东方财富/同花顺)")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report_lines)
    
    def print_errors(self):
        """打印错误信息"""
        if self.errors:
            print("\n⚠️  数据获取错误:")
            for error in self.errors:
                print(f"- {error}")

def main():
    """主函数"""
    print("=" * 60)
    print("A股收盘总结报告生成器")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 生成报告
    generator = StockSummaryGenerator()
    
    print("\n开始获取数据...")
    generator.fetch_all_data()
    
    print("\n生成报告...")
    report = generator.generate_report()
    
    # 打印报告
    print("\n" + "=" * 60)
    print("📋 收盘总结报告")
    print("=" * 60)
    print(report)
    
    # 打印错误
    generator.print_errors()
    
    # 发送钉钉消息
    print("\n" + "=" * 60)
    print("📤 发送钉钉消息...")
    success = send_dingtalk_message(report)
    
    if success:
        print("✅ 钉钉消息发送成功")
    else:
        print("❌ 钉钉消息发送失败")
    
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
