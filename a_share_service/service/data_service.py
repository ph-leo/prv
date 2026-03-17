# data_service.py - 核心数据服务

from .ak_client import AKClient
from .cache import DataCache
from .realtime_client import RealtimeClient
from .baostock_client import BaostockClient
from .utils import retry_with_backoff, log_execution, get_today_str
from datetime import datetime

class AShareDataService:
    """A股数据服务 - 统一入口（Baostock优先）"""
    
    def __init__(self):
        self.client = AKClient(use_proxy=True)
        self.realtime = RealtimeClient()
        self.baostock = BaostockClient()  # Baostock备用
        self.cache = DataCache()
        self.today = get_today_str()
    
    def _get_with_cache(self, key, fetch_func):
        """带缓存的数据获取"""
        # 先查缓存
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        
        # 缓存未命中，获取数据
        data = fetch_func()
        if data is not None:
            self.cache.set(key, data)
        return data
    
    @log_execution
    def get_zt_pool(self):
        """获取涨停池 - 带缓存"""
        return self._get_with_cache(
            f"zt_pool_{self.today}",
            lambda: self.client.get_zt_pool(self.today)
        )
    
    @log_execution
    def get_spot_data(self):
        """获取实时行情 - 带缓存，单次请求多数据复用"""
        return self._get_with_cache(
            f"spot_{self.today}",
            self.client.get_spot_data
        )
    
    @log_execution
    def get_index_data(self, symbol):
        """获取大盘指数 - Baostock优先"""
        # 优先使用 Baostock
        bs_data = self.baostock.get_index_data(symbol)
        if bs_data is not None and not bs_data.empty:
            print(f"[DataService] 使用 Baostock 数据")
            return bs_data
        
        # Baostock 失败，尝试实时接口
        realtime_data = self.realtime.get_realtime_index()
        if realtime_data and symbol in realtime_data:
            return realtime_data[symbol]
        
        # 都失败，用缓存的akshare数据
        return self._get_with_cache(
            f"index_{symbol}_{self.today}",
            lambda: self.client.get_index_data(symbol)
        )
    
    def get_top_gainers(self, spot_df=None):
        """获取涨幅榜 - 从缓存的spot数据计算"""
        if spot_df is None:
            spot_df = self.get_spot_data()
        
        if spot_df is not None and not spot_df.empty:
            try:
                return spot_df.nlargest(5, '涨跌幅')
            except:
                pass
        return None
    
    def get_top_losers(self, spot_df=None):
        """获取跌幅榜 - 从缓存的spot数据计算"""
        if spot_df is None:
            spot_df = self.get_spot_data()
        
        if spot_df is not None and not spot_df.empty:
            try:
                return spot_df.nsmallest(5, '涨跌幅')
            except:
                pass
        return None
    
    def get_active_stocks(self, spot_df=None):
        """获取活跃股票 - 从缓存的spot数据计算"""
        if spot_df is None:
            spot_df = self.get_spot_data()
        
        if spot_df is not None and not spot_df.empty:
            try:
                return spot_df.nlargest(5, '成交额')
            except:
                pass
        return None
    
    def get_all_data(self):
        """获取所有数据 - 统一入口"""
        result = {
            'timestamp': datetime.now(),
            'zt_pool': None,
            'spot': None,
            'index_sh': None,
            'index_sz': None,
            'index_cy': None,
            'top_gainers': None,
            'top_losers': None,
            'active_stocks': None,
        }
        
        # 获取基础数据
        result['zt_pool'] = self.get_zt_pool()
        result['spot'] = self.get_spot_data()
        
        # 获取大盘指数
        result['index_sh'] = self.get_index_data('000001')
        result['index_sz'] = self.get_index_data('399001')
        result['index_cy'] = self.get_index_data('399006')
        
        # 从spot计算排名（复用数据）
        if result['spot'] is not None:
            result['top_gainers'] = self.get_top_gainers(result['spot'])
            result['top_losers'] = self.get_top_losers(result['spot'])
            result['active_stocks'] = self.get_active_stocks(result['spot'])
        
        return result
