#!/usr/bin/env python3
"""
AI股票分析助手（产品级）- v2.0
整合a-shares-agent特性：
- 实时行情接口（东财）
- 并发数据获取
- AI选股模型
- 自动推送
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/a_share_service')

from service.data_service import AShareDataService
from service.ai_analyzer import AIAnalyzer
from service.publisher import DingTalkPublisher
from service.parallel_runner import ParallelRunner
from datetime import datetime

def generate_formatted_report(data, ai_report):
    """生成预定格式的报告"""
    lines = []
    lines.append("【A股收盘总结】")
    lines.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    # 大盘数据
    lines.append("📊 大盘：")
    if data['index_sh'] is not None:
        lines.append(f"- 上证指数：{data['index_sh']}")
    else:
        lines.append("- 上证指数：❌ 获取失败")
    
    if data['index_sz'] is not None:
        lines.append(f"- 深证成指：{data['index_sz']}")
    else:
        lines.append("- 深证成指：❌ 获取失败")
    
    if data['index_cy'] is not None:
        lines.append(f"- 创业板指：{data['index_cy']}")
    else:
        lines.append("- 创业板指：❌ 获取失败")
    lines.append("")
    
    # 涨跌家数
    lines.append("📈 涨跌家数：")
    if data['zt_pool'] is not None:
        lines.append(f"- 涨停家数：{len(data['zt_pool'])}家")
    else:
        lines.append("- 涨停家数：❌ 获取失败")
    lines.append("")
    
    # 涨幅前5
    lines.append("🔥 涨幅前5：")
    if data['top_gainers'] is not None and not data['top_gainers'].empty:
        for i, (idx, row) in enumerate(data['top_gainers'].head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            change = row.get('涨跌幅', 0)
            lines.append(f"{i}. {code} - {name} - {change:.2f}%")
    else:
        lines.append("❌ 获取失败")
    lines.append("")
    
    # 跌幅前5
    lines.append("📉 跌幅前5：")
    if data['top_losers'] is not None and not data['top_losers'].empty:
        for i, (idx, row) in enumerate(data['top_losers'].head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            change = row.get('涨跌幅', 0)
            lines.append(f"{i}. {code} - {name} - {change:.2f}%")
    else:
        lines.append("❌ 获取失败")
    lines.append("")
    
    # 活跃前5
    lines.append("💹 活跃前5（成交额）：")
    if data['active_stocks'] is not None and not data['active_stocks'].empty:
        for i, (idx, row) in enumerate(data['active_stocks'].head(5).iterrows(), 1):
            code = row.get('代码', 'N/A')
            name = row.get('名称', 'N/A')
            amount = row.get('成交额', 0) / 100000000
            lines.append(f"{i}. {code} - {name} - {amount:.2f}亿")
    else:
        lines.append("❌ 获取失败")
    lines.append("")
    
    # AI分析
    lines.append("【AI分析】")
    lines.append(f"热点板块：{ai_report['hot_sectors']}")
    lines.append("涨停原因：")
    for item in ai_report['zt_analysis'][:3]:
        lines.append(f"  - {item['code']} {item['name']}：{item['reason']}")
    lines.append(f"AI建议：{ai_report['recommendation']}")
    lines.append("")
    
    lines.append("---")
    lines.append("数据源：akshare + 实时行情")
    lines.append("AI分析助手 v2.0")
    
    return "\n".join(lines)

def main():
    """主函数"""
    print("═" * 50)
    print("🤖 AI股票分析助手 v2.0 启动")
    print("✨ 新增：实时行情 + 并发获取 + AI选股")
    print("═" * 50)
    
    # 1. 并发数据获取
    print("\n📊 [1/3] 并发获取市场数据...")
    service = AShareDataService()
    
    # 使用并行执行器
    runner = ParallelRunner(max_workers=5)
    results = runner.run_data_tasks(service)
    
    # 整合数据
    data = {
        'zt_pool': results[0] if not isinstance(results[0], Exception) else None,
        'spot': results[1] if not isinstance(results[1], Exception) else None,
        'index_sh': results[2] if not isinstance(results[2], Exception) else None,
        'index_sz': results[3] if not isinstance(results[3], Exception) else None,
        'index_cy': results[4] if not isinstance(results[4], Exception) else None,
        'timestamp': datetime.now()
    }
    
    # 计算排名（复用spot数据）
    if data['spot'] is not None:
        data['top_gainers'] = service.get_top_gainers(data['spot'])
        data['top_losers'] = service.get_top_losers(data['spot'])
        data['active_stocks'] = service.get_active_stocks(data['spot'])
    
    success_count = len([v for v in data.values() if v is not None and not isinstance(v, datetime)])
    print(f"✅ 数据获取完成：{success_count}/7 项成功")
    
    # 2. AI分析
    print("\n🧠 [2/3] AI 正在分析...")
    analyzer = AIAnalyzer()
    ai_report = analyzer.generate_daily_report(data)
    print("✅ AI 分析完成")
    
    # 3. 生成报告（预定格式）
    print("\n📄 [3/3] 生成报告...")
    formatted_report = generate_formatted_report(data, ai_report)
    
    # 推送
    publisher = DingTalkPublisher()
    publisher.publish_text(formatted_report)
    print("✅ 日报推送完成")
    
    print("\n" + "═" * 50)
    print("🎉 AI股票分析助手 v2.0 执行完成")
    print("═" * 50)
    
    return formatted_report

if __name__ == "__main__":
    main()
