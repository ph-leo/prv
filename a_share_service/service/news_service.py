# news_service.py - 新闻服务（多数据源 + 降级）

import akshare as ak
import requests
from datetime import datetime

class NewsService:
    """新闻服务 - 多数据源 + 模拟数据降级"""
    
    def __init__(self):
        self.data_source = None
        self.is_mock = False
    
    def get_ai_news(self, limit=5):
        """
        获取AI/科技新闻
        优先级：真实API > akshare > 模拟数据
        """
        # 1. 尝试 akshare
        news = self._try_akshare(limit)
        if news:
            self.data_source = "akshare（新浪财经）"
            self.is_mock = False
            return news
        
        # 2. 都失败，使用模拟数据
        news = self._get_mock_news(limit)
        self.data_source = "模拟数据（演示用）"
        self.is_mock = True
        return news
    
    def _try_akshare(self, limit):
        """尝试使用akshare获取新闻"""
        try:
            # 尝试多个akshare接口
            try:
                df = ak.stock_news_em()
                if df is not None and not df.empty:
                    return self._format_akshare_news(df.head(limit))
            except:
                pass
            
            try:
                df = ak.stock_news_main_cx()
                if df is not None and not df.empty:
                    return self._format_akshare_news(df.head(limit))
            except:
                pass
            
            return None
        except Exception as e:
            print(f"[News] akshare获取失败: {e}")
            return None
    
    def _format_akshare_news(self, df):
        """格式化akshare新闻（限制内容长度）"""
        news_list = []
        for _, row in df.iterrows():
            title = row.get('新闻标题', row.get('标题', 'N/A'))
            content = row.get('新闻内容', row.get('内容', ''))
            url = row.get('新闻链接', '')
            source = row.get('文章来源', '新浪财经')
            
            # 限制内容长度，避免超长
            summary = content[:50] + '...' if len(content) > 50 else content
            
            news_list.append({
                'title': title,
                'summary': summary,
                'source': source,
                'url': url
            })
        return news_list
    
    def _get_mock_news(self, limit=5):
        """获取模拟新闻数据"""
        mock_news = [
            {
                "title": "OpenAI发布GPT-5预览版，性能提升显著",
                "summary": "新一代大语言模型在推理能力和多模态处理上有重大突破，参数规模达到10万亿级别...",
                "source": "模拟数据",
                "url": "#模拟数据-无真实链接"
            },
            {
                "title": "谷歌Gemini 2.0正式上线，支持百万token上下文",
                "summary": "谷歌宣布Gemini 2.0全面开放，企业级应用加速落地，API价格降低50%...",
                "source": "模拟数据",
                "url": "#模拟数据-无真实链接"
            },
            {
                "title": "国内AI芯片厂商发布新一代训练芯片",
                "summary": "国产AI算力持续提升，单卡算力达到A100水平，降低大模型训练成本30%...",
                "source": "模拟数据",
                "url": "#模拟数据-无真实链接"
            },
            {
                "title": "自动驾驶技术取得新进展，L4级测试扩大",
                "summary": "多家车企宣布L4级自动驾驶进入城市道路测试阶段，预计2026年商业化...",
                "source": "模拟数据",
                "url": "#模拟数据-无真实链接"
            },
            {
                "title": "AI医疗诊断系统获批，精准度超95%",
                "summary": "人工智能在医学影像诊断领域应用获得重大突破，已获FDA认证...",
                "source": "模拟数据",
                "url": "#模拟数据-无真实链接"
            }
        ]
        return mock_news[:limit]
    
    def format_report(self, news_list):
        """格式化新闻报告"""
        lines = []
        lines.append("【AI News Daily】")
        lines.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 标明数据来源
        if self.is_mock:
            lines.append("⚠️ 数据源：[模拟数据] 仅作演示用")
        else:
            lines.append(f"📰 数据源：{self.data_source}")
        
        lines.append("")
        lines.append("今日AI/科技热点新闻：")
        lines.append("")
        
        for i, news in enumerate(news_list, 1):
            lines.append(f"{i}. {news['title']}")
            if news.get('summary'):
                lines.append(f"   {news['summary']}")
            if news.get('url') and news['url'] != '#模拟数据-无真实链接':
                lines.append(f"   链接：{news['url']}")
            lines.append("")
        
        lines.append("---")
        if self.is_mock:
            lines.append("⚠️ 注意：当前为模拟数据，非真实新闻")
            lines.append("建议：配置真实新闻API（NewsAPI/RSS等）")
        else:
            lines.append(f"数据源：{self.data_source}")
        
        return "\n".join(lines)
