from functools import lru_cache
from datetime import datetime, timedelta
import hashlib
import json

class DataCache:
    def __init__(self, ttl_seconds=300):  # 5 minutos por defecto
        self.cache = {}
        self.ttl = ttl_seconds
        
    def _get_key(self, func_name, *args, **kwargs):
        """Generar clave única para caché"""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, func_name, *args, **kwargs):
        key = self._get_key(func_name, *args, **kwargs)
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, func_name, data, *args, **kwargs):
        key = self._get_key(func_name, *args, **kwargs)
        self.cache[key] = (data, datetime.now())
    
    def clear(self):
        self.cache.clear()
    
    def invalidate_pattern(self, pattern):
        """Invalidar caché por patrón"""
        keys_to_delete = [
            k for k in self.cache.keys() 
            if pattern in k
        ]
        for key in keys_to_delete:
            del self.cache[key]
