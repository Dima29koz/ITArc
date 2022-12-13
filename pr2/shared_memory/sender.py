import time
from multiprocessing import shared_memory

import pywintypes
import win32file
import win32pipe


def pipe_client(size):
    print("pipe client")
    quit = False

    shm_a = shared_memory.SharedMemory(create=True, size=size)
    buffer = shm_a.buf
    print('shared_mem name:', shm_a.name)

    data = get_data(size)

    while not quit:
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\Foo',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                print(1)
                resp = win32file.ReadFile(handle, 64*1024)
                print(f"message: {resp}")
                try:
                    load_chunk(size, data, buffer)
                except StopIteration:
                    break
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True

    shm_a.close()
    shm_a.unlink()

def get_data(size):
    with open('short.txt', 'r', encoding='utf-8') as file:
        chunk = file.read(size)
        while chunk:
            yield chunk
            chunk = file.read(size)


def load_chunk(size, data, buffer):
    try:
        string = next(data)
        print(string)
        b_string = string.encode('utf-8')
        if len(b_string) < size:
            b_string += b'\x00' * (size - len(b_string))
        buffer[:] = bytearray(b_string)

    except StopIteration:
        b_string = b'\x00' * size
        buffer[:] = bytearray(b_string)
        raise


def main(size=10):
    shm_a = shared_memory.SharedMemory(create=True, size=size)
    buffer = shm_a.buf
    print('shared_mem name:', shm_a.name)

    data = get_data(size)

    while True:
        try:
            load_chunk(size, data, buffer)
        except StopIteration:
            break
        input('type to continue')
    shm_a.close()
    shm_a.unlink()


if __name__ == "__main__":
    pipe_client(10)
