import time
from collections import deque


class Scheduler:
    def __init__(self) -> None:
        self.ready = deque()
        self.current = None # Currently executing generator

    def new_task(self, coro):
        self.ready.append(coro)

    def run(self):
        while self.ready:
            self.current = self.ready.popleft()
            # Drive as a generator
            try:
                self.current.send(None) # Send to a coroutine
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass

sched = Scheduler() # Background scheduler object


class Awaitable:
    def __await__(self):
        yield


def switch():
    return Awaitable()

async def countdown(n):
    while n > 0:
        print('Down', n)
        time.sleep(1)
        await switch() # Switch tasks
        n -= 1

async def countup(stop):
    x = 0
    while x < stop:
        print('Up', x)
        time.sleep(1)
        await switch()
        x += 1

sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()

# In new python verisons they tried to hide yield from the user (async/await)
