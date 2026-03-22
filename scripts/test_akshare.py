#!/usr/bin/env python3
"""测试 akshare 数据获取"""

import akshare as ak
import os
import sys

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:55555'
os.environ['https_proxy'] = 'http://127.0.0.1:55555'

print("测试 akshare 接口...")

try:
    df = ak.stock_zh_a_spot()
    print(f"获取成功，数据行数: {len(df)}")
    print(df.head())
except Exception as e:
    print(f"获取失败: {e}")
    sys.exit(1)
