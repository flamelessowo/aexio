import time
from collections import deque

class Scheduler:
    def __init__(self):
        self.ready= deque()

    def call_soon(self, func):
        self.ready.append(func)

    def start(self):
        while self.ready:
            func = self.ready.popleft()
            func()

sched = Scheduler()

def countdown(n):
    if n > 0:
        print('Down', n)
        time.sleep(1)
        sched.call_soon(lambda: countdown(n-1))
    

def countup(n):
    x = 0
    if x < n:
        print('Up', x)
        time.sleep(1)
        sched.call_soon(lambda: countup(n-x))
     

countdown(5)
countup(5)
 
# Problem: how to achive concurrency without threads?
# Issue: Figure out how to switch between tasks




