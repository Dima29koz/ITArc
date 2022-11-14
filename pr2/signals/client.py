import os, sys
import time
import signal


def func(signum, frame):
    print('You raised a SIGTERM! Signal handler called with signal', signum)


signal.signal(signal.SIGTERM, func)

while True:
    print("Running...", os.getpid())
    time.sleep(2)
    # os.kill(os.getpid(),signal.SIGINT)
