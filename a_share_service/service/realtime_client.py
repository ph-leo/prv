# realtime_client.py - 实时行情客户端（借鉴a-shares-agent）

import requests
import json
from datetime import datetime

class RealtimeClient:
    """实时行情客户端 - 东财接口"""
    
    def __init__(self):
        self.base_url = "https://push2.eastmoney.com/api/qt"
        self.timeout = 5
    
    def get_realtime_index(self, secids="1.000001,0.399001,0.399006"):
        """获取实时大盘指数"""
        try:
            url = f"{self.base_url}/ulist.np/get"
            params = {
                "fltt": "2",
                "secids": secids,
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100"
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            data = response.json()
            
            if 'data' in data and 'diff' in data['data']:
                return self._parse_index_data(data['data']['diff'])
            return None
        except Exception as e:
            print(f"[Realtime] 获取失败: {e}")
            return None
    
    def _parse_index_data(self, diff_data):
        """解析指数数据"""
        result = {}
        for item in diff_data:
            code = item.get('f12', '')
            name = item.get('f14', '')
            price = item.get('f2', 0) / 100  # 价格要除以100
            change = item.get('f3', 0) / 100  # 涨跌幅要除以100
            
            result[code] = {
                '代码': code,
                '名称': name,
                '最新价': price,
                '涨跌幅': change
            }
        return result
    
    def get_realtime_stocks(self, codes):
        """获取实时个股数据"""
        try:
            # 构建secids
            secids = ",".join([f"0.{code}" if code.startswith('0') or code.startswith('3') else f"1.{code}" for code in codes])
            
            url = f"{self.base_url}/ulist.np/get"
            params = {
                "fltt": "2",
                "secids": secids,
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100"
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            data = response.json()
            
            if 'data' in data and 'diff' in data['data']:
                return self._parse_stock_data(data['data']['diff'])
            return None
        except Exception as e:
            print(f"[Realtime] 获取失败: {e}")
            return None
    
    def _parse_stock_data(self, diff_data):
        """解析个股数据"""
        result = []
        for item in diff_data:
            result.append({
                '代码': item.get('f12', ''),
                '名称': item.get('f14', ''),
                '最新价': item.get('f2', 0) / 100,
                '涨跌幅': item.get('f3', 0) / 100,
                '涨跌额': item.get('f4', 0) / 100,
                '成交量': item.get('f5', 0),
                '成交额': item.get('f6', 0),
                '振幅': item.get('f7', 0) / 100,
                '最高': item.get('f15', 0) / 100,
                '最低': item.get('f16', 0) / 100,
                '今开': item.get('f17', 0) / 100,
                '昨收': item.get('f18', 0) / 100
            })
        return result
