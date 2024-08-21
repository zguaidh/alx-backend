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
        self.usage_order = []

    def put(self, key, item):
        """Adds an item in the cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                self.frequency[key] += 1
             else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    self.discard_least_frequently_used()
                self.cache_data[key] = item
                self.frequency[key] = 1
            if key in self.usage_order:
                self.usage_order.remove(key)
            self.usage_order.append(key)

    def get(self, key):
        """Gets an item by its key"""
        if key in self.cache_data:
            self.frequency[key] += 1
            if key in self.order:
                self.usage_order.remove(key)
            self.usage_order.append(key)
            return self.cache_data[key]
        return None

    def discard_least_frequently_used(self):
        """ Discard the least frequently used item from the cache """
        min_freq = min(self.frequency.values())
        lfu_items = [key for key in self.usage_order if self.frequency[key] == min_freq]
        if lfu_items:
            lru_item = lfu_items[0]
            self.usage_order.remove(lru_item)
            del self.cache_data[lru_item]
            del self.frequency[lru_item]
            print(f"DISCARD: {lru_item}")
