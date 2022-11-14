import requests
import random


def main():
    for _ in range(100):
        path = f'data/{random.randint(0, 100)}'
        response = requests.get(f'http://127.0.0.1:5000/{path}')
        print(response.json(), response.status_code)


if __name__ == "__main__":
    main()
