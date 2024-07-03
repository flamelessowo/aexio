# producer.py

# Producer-consumer problem

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

