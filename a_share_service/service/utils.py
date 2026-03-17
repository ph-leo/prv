# utils.py - 工具函数

import time
import functools
from datetime import datetime

def retry_with_backoff(max_retries=3, delay=2, backoff=2):
    """指数退避重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for i in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                    # 数据为空，继续重试
                    if i < max_retries - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                except Exception as e:
                    if i < max_retries - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        raise e
            return None
        return wrapper
    return decorator

def log_execution(func):
    """执行日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        try:
            result = func(*args, **kwargs)
            elapsed = (datetime.now() - start).total_seconds()
            print(f"[OK] {func.__name__} 耗时 {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = (datetime.now() - start).total_seconds()
            print(f"[FAIL] {func.__name__} 耗时 {elapsed:.2f}s, 错误: {e}")
            raise
    return wrapper

def get_today_str():
    """获取今天日期字符串"""
    return datetime.now().strftime('%Y%m%d')
