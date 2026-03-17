#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股S1信号监控脚本 - 备用方案：使用新浪财经接口
"""

import requests
import re
from datetime import datetime

def fetch_sina_realtime_data():
    """从新浪财经获取A股实时数据"""
    try:
        # 沪市A股
        sh_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount"
        sh_count = requests.get(sh_url, params={"node": "hs_a"}, timeout=10).json()
        
        # 深市A股
        sz_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
        sz_data = requests.get(sz_url, params={
            "page": 1,
            "num": 80,
            "node": "sz_a",
            "symbol": "",
            "sort": "symbol",
            "asc": 1,
            "market": "001"
        }, timeout=10)
        
        return sz_data.json() if sz_data.status_code == 200 else None
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def check_index():
    """检查主要指数"""
    try:
        # 上证指数
        sh_url = "http://hq.sinajs.cn/?format=text&list=sse_index"
        sh_response = requests.get(sh_url, timeout=10)
        sh_data = sh_response.text
        
        # 深证成指
        sz_url = "http://hq.sinajs.cn/?format=text&list=sse_index"
        sz_response = requests.get(sz_url, timeout=10)
        sz_data = sz_response.text
        
        return sh_data, sz_data
    except Exception as e:
        print(f"指数获取失败: {e}")
        return None, None

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始A股S1信号监控（备用方案）")
    
    # 尝试获取指数信息
    sh_data, sz_data = check_index()
    
    if sh_data:
        print(f"上证指数数据: {sh_data[:100]}...")
    else:
        print("指数数据获取失败")
    
    print("\n提示：实时个股数据由于接口限制需要分批获取")
    print("建议：使用专业股票软件或API获取完整实时数据")
    print("当前监控方案：等待用户确认或使用其他数据源")

if __name__ == '__main__':
    main()
