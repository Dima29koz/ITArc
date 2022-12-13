import time
from multiprocessing import shared_memory

import win32file
import win32pipe


def pipe_server():
    print("pipe server")
    text = ''
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")
        shm_b = shared_memory.SharedMemory('wnsm_b17c100d')
        while True:
            print(f"writing message {count}")
            # convert to bytes
            some_data = str.encode(f"{count}")
            win32file.WriteFile(pipe, some_data)
            time.sleep(0.2)
            count += 1
            try:
                text += get_new_chunk(shm_b)

            except StopIteration:
                shm_b.close()
                break
        print("finished now")
    finally:
        win32file.CloseHandle(pipe)
        return text


def get_new_chunk(shm_b: shared_memory.SharedMemory):
    bytes_s = shm_b.buf[:10].tobytes()
    print(bytes_s)
    if bytes_s.startswith(b'\x00'):
        raise StopIteration
    return bytes_s.rstrip(b'\x00').decode('utf-8')


def read_data():
    text = ''
    shm_b = shared_memory.SharedMemory('wnsm_3e7b3ed2')
    while True:
        try:
            text += get_new_chunk(shm_b)
        except StopIteration:
            break
        input('type to continue')
    shm_b.close()
    return text


if __name__ == '__main__':
    print(pipe_server())
    # print(read_data())
