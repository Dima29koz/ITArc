import psutil
import signal


def func(signum, frame):
    print('You raised a SigInt! Signal handler called with signal', signum)


def main():
    print(signal.valid_signals())

    try:
        p = psutil.Process(pid=2492)
        with p.oneshot():
            p.send_signal(signal.signal(signal.SIGBREAK, func))
    except ProcessLookupError:
        print('pid is incorrect')
    except psutil.NoSuchProcess:
        print('pid is incorrect')


if __name__ == "__main__":
    main()
