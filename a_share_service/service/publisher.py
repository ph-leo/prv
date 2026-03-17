# publisher.py - 消息推送模块

import json
import requests
from datetime import datetime

class DingTalkPublisher:
    """钉钉消息推送"""
    
    def __init__(self, webhook_url=None):
        # 使用 OpenClaw 内置消息工具
        self.channel = "dingtalk"
        self.target = "cidPRZXi2wt7jEmvEe4h6ye2w=="
    
    def format_report(self, report_data):
        """格式化日报"""
        lines = []
        lines.append("═" * 40)
        lines.append("📊 AI股票分析日报")
        lines.append(f"📅 {report_data['date']}")
        lines.append("═" * 40)
        lines.append("")
        
        # 市场总结
        lines.append("【市场概览】")
        lines.append(report_data['market_summary'])
        lines.append("")
        
        # 热点板块
        lines.append("【热点板块】")
        lines.append(report_data['hot_sectors'])
        lines.append("")
        
        # 涨停分析
        lines.append("【涨停分析】")
        for item in report_data['zt_analysis']:
            lines.append(f"🔸 {item['code']} {item['name']}")
            lines.append(f"   原因：{item['reason']}")
        lines.append("")
        
        # 投资建议
        lines.append("【AI建议】")
        lines.append(f"💡 {report_data['recommendation']}")
        lines.append("")
        
        lines.append("═" * 40)
        lines.append("🤖 由 AI股票分析助手生成")
        lines.append("═" * 40)
        
        return "\n".join(lines)
    
    def publish(self, report_data):
        """发布日报"""
        formatted = self.format_report(report_data)
        
        # 这里应该调用 OpenClaw 的 message 工具
        # 简化版：打印到控制台
        print("\n" + "=" * 50)
        print("准备推送钉钉消息...")
        print("=" * 50)
        print(formatted)
        print("=" * 50)
        
        return formatted
