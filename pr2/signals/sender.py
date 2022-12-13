import psutil
import signal


def func(signum, frame):
    print('You raised a SigInt! Signal handler called with signal', signum)


def stop_proc(pid: int):

    try:
        p = psutil.Process(pid=pid)
        with p.oneshot():
            # p.send_signal(signal.signal(signal.SIGBREAK, func))
            p.send_signal(signal.SIGTERM)
    except ProcessLookupError:
        print('pid is incorrect')
    except psutil.NoSuchProcess:
        print('pid is incorrect')


if __name__ == "__main__":
    stop_proc(int(input('pid: ')))
