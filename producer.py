# producer.py

# Producer-consumer problem
# PROBLEM TO DO THIS WITHOUT THREADS

import queue
import threading
import time
def producer(q, count):
    for n in range(count):
        print('Producing', n)
        q.put(n)
        time.sleep(1)
    print('Producer done')
    q.put(None) # "Sentinel" to shut down

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print('Consuming', item)
    print('Consumer done')


q = queue.Queue() # Thread-safe
threading.Thread(target=producer, args=(q,10)).start()
threading.Thread(target=consumer, args=(q,)).start()

