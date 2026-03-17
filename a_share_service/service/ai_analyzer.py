# ai_analyzer.py - AI 分析模块

import os
from datetime import datetime

class AIAnalyzer:
    """AI 股票分析器"""
    
    def __init__(self):
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
    
    def analyze_zt_reason(self, stock_name, stock_code, industry=''):
        """AI 分析涨停原因"""
        # 模拟 AI 分析结果
        # 实际应调用 GPT API
        reasons = [
            "政策利好驱动，行业景气度提升",
            "业绩超预期，机构资金流入",
            "技术突破形态，市场热点轮动",
            "板块联动效应，龙头带动上涨",
            "资金面宽松，市场情绪回暖"
        ]
        import random
        return random.choice(reasons)
    
    def summarize_hot_sectors(self, top_stocks_df):
        """AI 总结热点板块"""
        if top_stocks_df is None or top_stocks_df.empty:
            return "暂无热点板块数据"
        
        # 提取行业信息（模拟）
        sectors = {}
        for _, row in top_stocks_df.iterrows():
            # 实际应从股票代码映射行业
            sector = self._get_sector_by_code(row.get('代码', ''))
            if sector:
                sectors[sector] = sectors.get(sector, 0) + 1
        
        if not sectors:
            return "热点分散，无明显板块效应"
        
        # 排序找出最热点
        hot_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)
        top_sector = hot_sectors[0]
        
        return f"🔥 最热点：{top_sector[0]}（{top_sector[1]}只涨停）"
    
    def _get_sector_by_code(self, code):
        """根据股票代码获取行业（简化版）"""
        # 实际应有完整映射表
        sector_map = {
            '60': '沪市主板',
            '00': '深市主板',
            '30': '创业板',
            '68': '科创板',
            '8': '北交所',
        }
        for prefix, sector in sector_map.items():
            if code.startswith(prefix):
                return sector
        return '其他'
    
    def generate_daily_report(self, data):
        """自动生成日报"""
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'market_summary': self._analyze_market(data),
            'hot_sectors': self.summarize_hot_sectors(data.get('zt_pool')),
            'zt_analysis': self._analyze_zt_stocks(data.get('zt_pool')),
            'recommendation': self._generate_recommendation(data)
        }
        return report
    
    def _analyze_market(self, data):
        """分析市场整体情况"""
        sh = data.get('index_sh')
        if sh is not None and not sh.empty:
            change = sh.iloc[0]['涨跌幅']
            if change > 1:
                return "强势上涨，市场情绪积极"
            elif change > 0:
                return "小幅上涨，情绪平稳"
            elif change > -1:
                return "小幅调整，情绪谨慎"
            else:
                return "明显下跌，情绪偏空"
        return "数据不足，无法判断"
    
    def _analyze_zt_stocks(self, zt_df):
        """分析涨停股票"""
        if zt_df is None or zt_df.empty:
            return []
        
        analysis = []
        for _, row in zt_df.head(3).iterrows():
            analysis.append({
                'code': row.get('代码'),
                'name': row.get('名称'),
                'reason': self.analyze_zt_reason(
                    row.get('名称'), 
                    row.get('代码')
                )
            })
        return analysis
    
    def _generate_recommendation(self, data):
        """生成投资建议"""
        zt_count = len(data.get('zt_pool', [])) if data.get('zt_pool') is not None else 0
        
        if zt_count > 50:
            return "市场情绪高涨，建议关注强势股，但注意追高风险"
        elif zt_count > 30:
            return "市场情绪积极，可适度参与热点板块"
        elif zt_count > 10:
            return "市场情绪一般，建议观望或轻仓"
        else:
            return "市场情绪低迷，建议谨慎操作，控制风险"
