# aproducer.py

# Producer-consumer problem
# The same but no threads

import time
from the_problem import Scheduler
from collections import deque

sched = Scheduler()


class Result:
    def __init__(self, value=None, exc=None) -> None:
        self.value = value
        self.exc = exc

    def result(self):
        if self.exc:
            raise self.exc
        else:
            return self.value


class AsyncQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.waiting = deque() # All getters waiting for data
        self._closed = False # Can queue be used anymore?

    def close(self):
        self._closed = True
        if self.waiting and not self.items:
            for func in self.waiting:
                sched.call_soon(func)

    def put(self, item):
        if self._closed:
            raise RuntimeError('Queue closed')
        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()
            # Do we call it right away?
            sched.call_soon(func)
            # func() ---> might get deep calls, recursion, etc

    def get(self, callback):
        # Wait till item available. Then return
        # How does a closed queue interact with get()
        if self.items:
            callback(Result(value=self.items.popleft())) # Good result
        else:
            # No items available (must wait)
            if self._closed:
                # Now what?
                callback(Result(exc=RuntimeError('Queue closed'))) # error result
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
            q.close() # No more items produced
    _run(0)

def consumer(q):
    def _consume(result):
        try:
            item = result.result()
            print('Consuming', item) # <<<<< Queue item result
            sched.call_soon(lambda: consumer(q))
        except RuntimeError:
            print("Consumer done")
    q.get(callback=_consume)

q = AsyncQueue()
sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q, ))
sched.run()
