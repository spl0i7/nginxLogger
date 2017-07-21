from event_handler import moniter_change

import os, signal
moniter = moniter_change('/tmp/foo.bar')

def handler(signum, frame):
    moniter.join()
    print('Moniter stopped')

signal.signal(signal.SIGINT, handler)

