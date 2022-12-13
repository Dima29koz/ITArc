import time
import csv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def create_file(header, data):
    with open('data2/file.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def change_data(path):
    with open(path, 'r') as f:
        rows = []
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            rows.append(row)
        for row in rows[1:]:
            row[2] *= 2
        create_file(rows[0], rows[1:])
        print('data changed')


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("on_modified", event.src_path)
        change_data(event.src_path)


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='data1/', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
