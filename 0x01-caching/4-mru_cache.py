#!/usr/bin/env python3
"""MRUCache module"""


from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache defines a caching system with MRU algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.cache_data = OrderedDict()
        self.most_recent_key = None

    def put(self, key, item):
        """Adds an item in the cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
            else:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    if self.most_recent_key:
                        discarded = self.most_recent_key
                        del self.cache_data[discarded]
                        print(f"DISCARD: {discarded}")
                self.cache_data[key] = item
            self.most_recent_key = key
            self.cache_data.move_to_end(key)

    def get(self, key):
        """Gets an item by its key"""
        if key in self.cache_data:
            self.most_recent_key = key
            self.cache_data.move_to_end(key)
            return self.cache_data[key]
        return None
