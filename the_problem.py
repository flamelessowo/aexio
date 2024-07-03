import time
from collections import deque
import heapq # Priority queues from the box

# ASYNCIO LIBRARIES DO TIME MANAGEMENT IN SCHEDULERS

class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = []
        self.sequence = 0

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        self.sequence += 1
        deadline = time.time() + delay # Expiration time
        # Priority queue
        heapq.heappush(self.sleeping, (deadline, self.sequence, func))


    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, func = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


sched = Scheduler()

def countdown(n):
    if n > 0:
        print('Down', n)
        sched.call_later(4, lambda: countdown(n-1))

def countup(n):
    def _run(x):
        if x < n:
            print('Up', x)
            sched.call_later(1, lambda: _run(x+1))
    _run(0)
    
if __name__ == '__main__':
    sched.call_soon(lambda: countup(20))
    sched.call_soon(lambda: countdown(5))
    sched.run()

# Problem: how to achive concurrency without threads?
# Issue: Figure out how to switch between tasks




