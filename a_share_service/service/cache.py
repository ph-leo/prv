# cache.py - 缓存层

import os
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path

class DataCache:
    """数据缓存管理"""
    
    def __init__(self, cache_dir="/root/.openclaw/workspace/a_share_service/cache", ttl_minutes=30):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def _get_cache_path(self, key):
        """获取缓存文件路径"""
        return self.cache_dir / f"{key}.pkl"
    
    def _get_meta_path(self, key):
        """获取元数据文件路径"""
        return self.cache_dir / f"{key}.meta"
    
    def get(self, key):
        """获取缓存数据"""
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        if not cache_path.exists():
            return None
        
        # 检查是否过期
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            cached_time = datetime.fromisoformat(meta['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                print(f"[CACHE] {key} 已过期")
                return None
        
        # 读取缓存
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            print(f"[CACHE] {key} 命中缓存")
            return data
        except Exception as e:
            print(f"[CACHE] {key} 读取失败: {e}")
            return None
    
    def set(self, key, data):
        """设置缓存数据"""
        cache_path = self._get_cache_path(key)
        meta_path = self._get_meta_path(key)
        
        try:
            # 保存数据
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            
            # 保存元数据
            meta = {
                'timestamp': datetime.now().isoformat(),
                'key': key
            }
            with open(meta_path, 'w') as f:
                json.dump(meta, f)
            
            print(f"[CACHE] {key} 已缓存")
        except Exception as e:
            print(f"[CACHE] {key} 保存失败: {e}")
    
    def clear_expired(self):
        """清理过期缓存"""
        for meta_file in self.cache_dir.glob("*.meta"):
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                cached_time = datetime.fromisoformat(meta['timestamp'])
                if datetime.now() - cached_time > self.ttl:
                    key = meta['key']
                    cache_file = self._get_cache_path(key)
                    cache_file.unlink(missing_ok=True)
                    meta_file.unlink(missing_ok=True)
                    print(f"[CACHE] 清理过期: {key}")
            except Exception as e:
                print(f"[CACHE] 清理失败: {e}")
