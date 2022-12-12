import os
import threading
# from asyncio import sleep
from time import sleep

protected_resource = 1
unprotected_resource = 1
res = ''
NUM = 100
mutex = threading.Lock()


def show():
    global protected_resource
    global unprotected_resource
    for i in range(100):
        print(protected_resource, unprotected_resource)
        sleep(0.001)


def safe_plus():
    global protected_resource
    for i in range(NUM):
        mutex.acquire()
        protected_resource *= 4
        sleep(0.0000001)
        protected_resource /= 4
        mutex.release()


def safe_mult():
    global protected_resource
    for i in range(NUM):
        sleep(0.00005)
        mutex.acquire()
        protected_resource *= 3
        mutex.release()


def safe_minus():
    global protected_resource
    for i in range(NUM):
        mutex.acquire()
        protected_resource += 3
        sleep(0.000008)
        protected_resource -= 3
        mutex.release()


def risky_plus():
    global unprotected_resource
    for i in range(NUM):
        unprotected_resource *= 4
        print('pause+')
        sleep(0.05)
        unprotected_resource /= 4
        print('end+')


def risky_mult():
    global unprotected_resource
    for i in range(NUM):
        sleep(0.00002)
        unprotected_resource *= 3


def risky_minus():
    global unprotected_resource
    for i in range(NUM):
        unprotected_resource += 3
        print('pause-')
        sleep(0.03)
        # sleep(0.0005)
        unprotected_resource -= 3
        sleep(0.03)
        print('end-')


for i in range(10):
    protected_resource = 1
    unprotected_resource = 1
    thread1 = threading.Thread(target=safe_plus)
    thread2 = threading.Thread(target=safe_minus)
    thread3 = threading.Thread(target=risky_plus)
    thread4 = threading.Thread(target=risky_minus)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    res += f"\n{i}\nРезультат при работе с блокировкой {protected_resource}"
    res += f"\nРезультат без блокировки {unprotected_resource}"
    res += f'\nравенство результатов {protected_resource == unprotected_resource}'

os.system('cls')
print(res)
