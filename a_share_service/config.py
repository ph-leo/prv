# config.py - A股数据服务配置

import os
from datetime import timedelta

class Config:
    """服务配置"""
    
    # 缓存配置
    CACHE_DIR = "/root/.openclaw/workspace/a_share_service/cache"
    CACHE_TTL = timedelta(minutes=30)  # 缓存30分钟
    
    # 代理配置
    USE_PROXY = True
    PROXY_URL = "http://127.0.0.1:55555"
    
    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # 秒
    BACKOFF_FACTOR = 2  # 指数退避
    
    # 超时配置
    REQUEST_TIMEOUT = 30  # 秒
    
    # 数据源配置
    DATA_SOURCES = {
        'zt_pool': 'akshare',  # 涨停池
        'spot': 'akshare',     # 实时行情
        'index': 'akshare',    # 大盘指数
    }
    
    # 钉钉配置
    DINGTALK_GROUP = "cidPRZXi2wt7jEmvEe4h6ye2w=="
