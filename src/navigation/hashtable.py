class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def contains(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        return any(k == key for k, _ in bucket)

    def keys(self):
        result = []
        for bucket in self.buckets:
            for k, _ in bucket:
                result.append(k)
        return result

    def values(self):
        result = []
        for bucket in self.buckets:
            for _, v in bucket:
                result.append(v)
        return result

    def __len__(self):
        return self.size

    def __repr__(self):
        items = {k: v for bucket in self.buckets for k, v in bucket}
        return f"HashTable({items})"
