# parallel_runner.py - 并发执行器（借鉴a-shares-agent）

import asyncio
import concurrent.futures
from functools import partial

class ParallelRunner:
    """并行任务执行器"""
    
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
    
    async def run_tasks(self, tasks):
        """并发执行多个任务"""
        """
        tasks: list of (func, args, kwargs)
        """
        loop = asyncio.get_event_loop()
        
        # 创建线程池任务
        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for func, args, kwargs in tasks:
                future = loop.run_in_executor(
                    executor,
                    partial(func, *args, **kwargs)
                )
                futures.append(future)
            
            # 等待所有任务完成
            results = await asyncio.gather(*futures, return_exceptions=True)
        
        return results
    
    def run_sync(self, tasks):
        """同步执行并发任务"""
        return asyncio.run(self.run_tasks(tasks))
    
    def run_data_tasks(self, data_service):
        """并发获取多种数据"""
        tasks = [
            (data_service.get_zt_pool, [], {}),
            (data_service.get_spot_data, [], {}),
            (data_service.get_index_data, ['000001'], {}),
            (data_service.get_index_data, ['399001'], {}),
            (data_service.get_index_data, ['399006'], {}),
        ]
        
        return self.run_sync(tasks)
