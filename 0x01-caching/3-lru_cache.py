#!/usr/bin/env python3
"""LRUCache module"""


from collections import OrderedDict
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache defines a caching system with LRU algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item in the cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data.move_to_end(key)
            self.cache_data[key] = item
            if len(self.cache_data) > self.MAX_ITEMS:
                discarded, _ = self.cache_data.popitem(last=False)
                print(f"DISCARD: {discarded}")

    def get(self, key):
        """Gets an item by its key"""
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return None
