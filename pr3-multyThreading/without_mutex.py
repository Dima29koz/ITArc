import threading
from time import sleep


def add(amount, repeats):
    global value
    for i in range(repeats):
        value += amount


def sub(amount, repeats):
    global value
    for i in range(repeats):
        value -= amount




value = 0

add_thread = threading.Thread(target=add, args=(1, 1000000))
add_thread.start()

subtract_thread = threading.Thread(target=sub, args=(1, 1000000))
subtract_thread.start()

add_thread.join()
subtract_thread.join()

print(value)
