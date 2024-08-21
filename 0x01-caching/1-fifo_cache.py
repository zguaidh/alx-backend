#!/usr/bin/env python3
"""FIFOCache module"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache defines a caching system with FIFO algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Adds an item in the cache"""
        if key and item:
            if key not in self.cache_data:
                if len(self.cache_data) >= self.MAX_ITEMS:
                    discarded = self.order.pop(0)
                    print(f"DISCARD: {discarded}")
                    del self.cache_data[discarded]
            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """Gets an item its key"""
        return self.cache_data.get(key, None)
