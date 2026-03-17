# ak_client.py - akshare客户端封装

import os
import akshare as ak
import requests
from datetime import datetime

class AKClient:
    """akshare客户端 - 统一入口"""
    
    def __init__(self, use_proxy=True):
        self.use_proxy = use_proxy
        self.session = requests.Session()
        
        if use_proxy:
            os.environ['HTTP_PROXY'] = 'http://127.0.0.1:55555'
            os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:55555'
    
    def get_zt_pool(self, date_str):
        """获取涨停池 - 单次请求多数据复用"""
        try:
            df = ak.stock_zt_pool_em(date=date_str)
            return df if not df.empty else None
        except Exception as e:
            print(f"[AK] 涨停池获取失败: {e}")
            return None
    
    def get_spot_data(self):
        """获取实时行情 - 单次请求多数据复用"""
        try:
            df = ak.stock_zh_a_spot_em()
            return df if not df.empty else None
        except Exception as e:
            print(f"[AK] 实时行情获取失败: {e}")
            return None
    
    def get_index_data(self, symbol):
        """获取大盘指数 - 简化请求"""
        try:
            today = datetime.now().strftime('%Y%m%d')
            df = ak.index_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=today,
                end_date=today
            )
            return df if not df.empty else None
        except Exception as e:
            print(f"[AK] 指数{symbol}获取失败: {e}")
            return None
