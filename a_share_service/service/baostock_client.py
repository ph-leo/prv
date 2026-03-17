# baostock_client.py - Baostock 备用接口

import baostock as bs
import pandas as pd
from datetime import datetime

class BaostockClient:
    """Baostock 备用数据源"""
    
    def __init__(self):
        self.lg = None
        self._login()
    
    def _login(self):
        """登录 Baostock"""
        try:
            self.lg = bs.login()
            if self.lg.error_code != '0':
                print(f"[Baostock] 登录失败: {self.lg.error_msg}")
                self.lg = None
            else:
                print("[Baostock] 登录成功")
        except Exception as e:
            print(f"[Baostock] 登录异常: {e}")
            self.lg = None
    
    def logout(self):
        """登出"""
        if self.lg:
            bs.logout()
    
    def get_index_data(self, symbol):
        """获取大盘指数"""
        if self.lg is None:
            return None
        
        try:
            # 转换代码格式
            code_map = {
                '000001': 'sh.000001',  # 上证指数
                '399001': 'sz.399001',  # 深证成指
                '399006': 'sz.399006',  # 创业板指
            }
            
            if symbol not in code_map:
                return None
            
            code = code_map[symbol]
            today = datetime.now().strftime('%Y-%m-%d')
            
            rs = bs.query_index_data(code=code, start_date=today, end_date=today)
            
            if rs.error_code != '0':
                print(f"[Baostock] 获取失败: {rs.error_msg}")
                return None
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                return None
            
            result = pd.DataFrame(data_list, columns=rs.fields)
            return result
            
        except Exception as e:
            print(f"[Baostock] 获取异常: {e}")
            return None
    
    def get_stock_data(self, code):
        """获取个股数据"""
        if self.lg is None:
            return None
        
        try:
            # 转换代码格式
            if code.startswith('6'):
                bs_code = f"sh.{code}"
            else:
                bs_code = f"sz.{code}"
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            rs = bs.query_history_k_data_plus(
                bs_code,
                "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                start_date=today,
                end_date=today,
                frequency="d",
                adjustflag="3"
            )
            
            if rs.error_code != '0':
                return None
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                return None
            
            result = pd.DataFrame(data_list, columns=rs.fields)
            return result
            
        except Exception as e:
            print(f"[Baostock] 获取异常: {e}")
            return None
