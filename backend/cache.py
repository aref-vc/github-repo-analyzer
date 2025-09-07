"""
In-Memory Caching System
TTL-based cache for repository analysis data
"""

import time
import hashlib
import json
from typing import Any, Optional, Dict
from functools import wraps
from threading import Lock

class RepositoryCache:
    """Thread-safe in-memory cache with TTL support"""
    
    def __init__(self, max_size: int = 100, default_ttl: int = 900):
        """
        Initialize cache
        
        Args:
            max_size: Maximum number of entries to cache
            default_ttl: Default time-to-live in seconds (15 minutes)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
        self._lock = Lock()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from function arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if still valid"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry['expires_at']:
                    self.hits += 1
                    self._access_times[key] = time.time()
                    return entry['value']
                else:
                    # Expired, remove it
                    del self._cache[key]
                    del self._access_times[key]
            
            self.misses += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Store value in cache with TTL"""
        with self._lock:
            # Evict oldest entry if cache is full
            if len(self._cache) >= self.max_size:
                self._evict_oldest()
            
            expires_at = time.time() + (ttl or self.default_ttl)
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            self._access_times[key] = time.time()
    
    def _evict_oldest(self):
        """Evict least recently accessed entry"""
        if not self._access_times:
            return
        
        oldest_key = min(self._access_times, key=self._access_times.get)
        del self._cache[oldest_key]
        del self._access_times[oldest_key]
    
    def clear(self):
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'entries': len(self._cache),
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': f"{hit_rate:.1f}%",
                'max_size': self.max_size,
                'default_ttl': self.default_ttl
            }

# Global cache instance
repository_cache = RepositoryCache(max_size=100, default_ttl=900)  # 15 minutes TTL

def cache_result(ttl: Optional[int] = None):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time-to-live in seconds (uses default if not specified)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{repository_cache._generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = repository_cache.get(cache_key)
            if cached_result is not None:
                print(f"✅ Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            # Don't cache errors or partial results
            if not isinstance(result, dict) or not result.get("error"):
                repository_cache.set(cache_key, result, ttl)
                print(f"💾 Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

def cache_repository_analysis(owner: str, repo: str, analysis_data: Dict[str, Any]):
    """Cache complete repository analysis"""
    cache_key = f"analysis:{owner}/{repo}"
    repository_cache.set(cache_key, analysis_data, ttl=1800)  # Cache for 30 minutes

def get_cached_analysis(owner: str, repo: str) -> Optional[Dict[str, Any]]:
    """Get cached repository analysis if available"""
    cache_key = f"analysis:{owner}/{repo}"
    return repository_cache.get(cache_key)

def invalidate_repository_cache(owner: str, repo: str):
    """Invalidate cache for specific repository"""
    # This would need more implementation to track all keys for a repo
    # For now, just clear all cache
    repository_cache.clear()
    print(f"🗑️ Cache cleared for {owner}/{repo}")

def get_cache_stats() -> Dict[str, Any]:
    """Get current cache statistics"""
    return repository_cache.get_stats()