from collections import deque, defaultdict
from enum import Enum


class TokenBucket:
    def __init__(self, capacity, rate):
        self.amount = capacity
        self.capacity = capacity
        self.rate = rate
        self.prev = 0

    def _allow(self, time):
        gained = (time - self.prev) * self.rate
        self.amount = min(self.amount + gained, self.capacity)
        self.prev = time
        if self.amount >= 1:
            return True
        return False

    def allow(self, time):
        if self._allow(time):
            self.amount -= 1
            return True
        return False

    def default(self, time):
        gained = (time - self.prev) * self.rate
        self.amount = min(self.amount + gained, self.capacity)
        self.prev = time
        if self.amount == self.capacity:
            return True
        return False


class SlidingWindow:
    def __init__(self, n, window):
        self.num_reqs = n
        self.window_size = window
        self.window = deque()

    def _allow(self, time):
        start_time = time - self.window_size
        while len(self.window) > 0 and self.window[0] < start_time:
            self.window.popleft()
        if len(self.window) >= self.num_reqs:
            return False
        return True

    def allow(self, time):
        if self._allow(time):
            self.window.append(time)
            return True
        return False

    def default(self, time):
        start_time = time - self.window_size
        while len(self.window) > 0 and self.window[0] < start_time:
            self.window.popleft()
        if len(self.window) == 0:
            return True
        return False


class LimiterType(Enum):
    TOKEN_BUCKET = "token"
    SLIDING_WINDOW = "sliding"


class KeyedLimiter:
    def __init__(self, limit_type, capacity=None, rate=None, n=None, window=None):
        if limit_type == LimiterType.TOKEN_BUCKET:
            self.limiter = defaultdict(lambda: TokenBucket(capacity, rate))
        else:
            self.limiter = defaultdict(lambda: SlidingWindow(n, window))

    def allow(self, key, time):
        return self.limiter[key].allow(time)

    def cleanup(self, time):
        to_remove = set()
        for key, value in self.limiter.items():
            if value.default(time):
                to_remove.add(key)
        for key in to_remove:
            del self.limiter[key]


class Composition:
    def __init__(self, capacity=None, rate=None, n=None, window=None):
        self.limiter_bucket = defaultdict(lambda: TokenBucket(capacity, rate))
        self.limiter_window = defaultdict(lambda: SlidingWindow(n, window))

    def allow(self, key, time):
        if self.limiter_bucket[key]._allow(time) and self.limiter_window[key]._allow(
            time
        ):
            self.limiter_window[key].allow(time)
            self.limiter_bucket[key].allow(time)
            return True
        return False
