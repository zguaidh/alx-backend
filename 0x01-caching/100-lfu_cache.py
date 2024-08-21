#!/usr/bin/env python3
"""LFUCache module"""

from collections import defaultdict
from base_caching import BaseCaching

class LFUCache(BaseCaching):
    """LFUCache defines a caching system with LFU algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.frequency = defaultdict(int)
        self.order = []

    def put(self, key, item):
        """Adds an item in the cache"""
        if key and item:
            if key in self.cache_data:
                self.frequency[key] += 1
            else:
                self.frequency[key] = 1
                if len(self.cache_data) >= self.MAX_ITEMS:
                    min_freq = min(self.frequency.values())
                    lfu_items = [k for k in self.order if self.frequency[k] == min_freq]
                    lru_item = lfu_items[0]
                    self.order.remove(lru_item)
                    print(f"DISCARD: {lru_item}")
                    del self.cache_data[lru_item]
                    del self.frequency[lru_item]
            self.cache_data[key] = item
            if key in self.order:
                self.order.remove(key)
            self.order.append(key)

    def get(self, key):
        """Gets an item by its key"""
        if key in self.cache_data:
            self.frequency[key] += 1
            if key in self.order:
                self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None

