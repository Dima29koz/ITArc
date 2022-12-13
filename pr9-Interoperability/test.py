import csv

header = ['id', 'name', 'age', 'email']
data = [
    [1, 'tester1', 124, 't1@t.t'],
    [2, 'tester2', 23, 't2@t.t'],
    [3, 'tester3', 312, 't3@t.t'],
]


def create_file():
    with open('data1/file1.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def main():
    create_file()


if __name__ == '__main__':
    main()