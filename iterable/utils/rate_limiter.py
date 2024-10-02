import time

class RateLimiter:
    def __init__(self, rate=50, per=1.0):
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()

    def wait(self):
        now = time.time()
        time_passed = now - self.last_check
        self.last_check = now
        self.allowance += time_passed * (self.rate / self.per)
        if self.allowance > self.rate:
            self.allowance = self.rate
        if self.allowance < 1:
            time.sleep(1 - self.allowance)
            self.allowance = 0
        else:
            self.allowance -= 1
