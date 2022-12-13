import time
import csv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

header = ['id', 'name', 'age', 'email']
data = [
    [1, 'tester1', 124, 't1@t.t'],
    [2, 'tester2', 23, 't2@t.t'],
    [3, 'tester3', 312, 't3@t.t'],
]


def create_file():
    with open('data1/file.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
        return


def show_data(path):
    with open(path, 'r') as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            print(row)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("on_modified", event.src_path)
        show_data(event.src_path)


create_file()
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='data2/', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
