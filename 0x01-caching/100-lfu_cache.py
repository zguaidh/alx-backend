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
            if key in self.usage_order:
                self.usage_order.remove(key)
            self.usage_order.append(key)
            return self.cache_data[key]
        return None

    def discard_least_frequently_used(self):
        """ Discard the least frequently used item from the cache """
        min_freq = min(self.frequency.values())
        for key in self.usage_order:
            if self.frequency[key] == min_freq:
                self.usage_order.remove(key)
                del self.cache_data[key]
                del self.frequency[key]
                print(f"DISCARD: {key}")

    def update_usage_order(self, key):
        """ Update the usage order to the key that was recently used"""
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)
