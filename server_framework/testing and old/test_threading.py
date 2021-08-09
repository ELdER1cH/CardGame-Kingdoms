#https://pymotw.com/2/threading/

import random
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def worker():
    """thread worker function"""
    t = threading.currentThread()
    pause = random.randint(1,5)
    logging.debug('sleeping %s', pause)
    time.sleep(pause)
    logging.debug('ending')
    return

for i in range(3):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

"""
main_thread = threading.currentThread()

for t in threading.enumerate():
    if t is main_thread:
        continue
    logging.debug('joining %s', t.getName())
    t.join()"""

"""import threading
import time

def worker():
    print(threading.currentThread().getName() + 'Starting')
    time.sleep(2)
    print(threading.currentThread().getName() + 'Exiting')

def my_service():
    print(threading.currentThread().getName() + 'Starting')
    time.sleep(3)
    print(threading.currentThread().getName() + 'Exiting')

w = threading.Thread(name='worker', target=worker)
w2 = threading.Thread(target=worker) # use default name
t = threading.Thread(name='my_service', target=my_service)


w.start()
w2.start()
t.start()"""
