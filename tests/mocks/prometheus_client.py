class Gauge:
    def __init__(self, name, documentation, labelnames=(), registry=None):
        self.name = name
        self.documentation = documentation
        self.labelnames = labelnames
        self._value = MockValue()

    def labels(self, **kwargs):
        return self

    def set(self, value):
        self._value.set(value)

class Counter:
    def __init__(self, name, documentation, labelnames=(), registry=None):
        pass
    def labels(self, **kwargs):
        return self
    def inc(self, amount=1):
        pass

class Histogram:
    def __init__(self, name, documentation, labelnames=(), buckets=(), registry=None):
        pass
    def labels(self, **kwargs):
        return self
    def observe(self, amount):
        pass

class MockValue:
    def __init__(self):
        self.val = 0
    def set(self, val):
        self.val = val
    def get(self):
        return self.val

REGISTRY = object()
