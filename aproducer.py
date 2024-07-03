# aproducer.py

# Producer-consumer problem
# The same but no threads

import time
from the_problem import Scheduler
from collections import deque

sched = Scheduler()


class AsyncQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.waiting = deque() # All getters waiting for data

    def put(self, item):
        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()
            # Do we call it right away?
            sched.call_soon(func)
            # func() ---> might get deep calls, recursion, etc

    def get(self, callback):
        # Wait till item available. Then return
        if self.items:
            callback(self.items.popleft())
        else:
            self.waiting.append(lambda: self.get(callback))



def producer(q, count):
    def _run(n):
        if n < count:
            print('Producing', n)
            q.put(n)
            sched.call_later(1, lambda: _run(n+1))
        else:
            print('Producer done')
            q.put(None)
    _run(0)

def consumer(q):
    def _consume(item):
        if item is None:
            print('Consumer done')
        else:
            print('Consuming', item)
            sched.call_soon(lambda: consumer(q))
    q.get(callback=_consume)

q = AsyncQueue()
sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q, ))
sched.run()
