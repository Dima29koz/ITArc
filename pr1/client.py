import random
import socket
import struct
import threading
from time import sleep


class Client:
    MCAST_GRP = '224.3.29.71'
    MCAST_PORT = 5010
    CLIENT_PORT = 5011
    BUFFER_SIZE = 1024

    def __init__(self):
        self.ip = (socket.gethostbyname(socket.gethostname()), self.CLIENT_PORT)
        self.server_address_port = None
        self.client_socket = self.create_socket(('', self.CLIENT_PORT), True)
        self.server_socket = None
        self.tr_server = None
        self.tr_choice = None
        self.tr_server_health = None
        self.numbers = []
        self.is_server = False
        if not self.check_server():
            self.send_cmd_to_rnd()

    def send_cmd_to_rnd(self):
        # print('sending gen command')
        self.client_socket.sendto('~gen_num'.encode('utf-8'), (self.MCAST_GRP, self.CLIENT_PORT))

    def send_number(self):
        self.numbers = []
        number = random.randint(0, 100)
        # print('sending number')
        self.client_socket.sendto(str(number).encode('utf-8'), (self.MCAST_GRP, self.CLIENT_PORT))
        self.tr_choice = threading.Thread(target=self.choice_host)
        self.tr_choice.start()

    def choice_host(self):
        sleep(0.5)
        # print('choosing proc start')
        self.server_address_port = sorted(self.numbers, key=lambda item: item[0], reverse=True)[0][1]
        if self.ip == self.server_address_port:
            self.create_server()
            self.check_server()
        return

    def create_server(self):
        self.is_server = True
        self.server_socket = self.create_socket(('', self.MCAST_PORT))
        self.tr_server = threading.Thread(target=self.server_loop)
        self.tr_server_health = threading.Thread(target=self.server_health_loop)
        self.tr_server.start()
        self.tr_server_health.start()
        print('im server now!')

    def create_socket(self, address, timeout=False):
        listen_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP)
        listen_socket.bind(address)
        group = socket.inet_aton(self.MCAST_GRP)
        listen_socket.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL', group, socket.INADDR_ANY))
        if timeout:
            listen_socket.settimeout(0.5)
        return listen_socket

    def check_server(self):
        self.client_socket.sendto("client connected".encode(), (self.MCAST_GRP, self.MCAST_PORT))
        try:
            data, address = self.client_socket.recvfrom(self.BUFFER_SIZE)
        except TimeoutError:
            # print('server doesnt exist')
            return False
        else:
            # print('server exists')
            # print('data:', data.decode('utf-8'))
            # print('addr', address)
            self.server_address_port = address
            return True

    def server_loop(self):
        while True:
            message, address = self.server_socket.recvfrom(self.BUFFER_SIZE)
            # print(f'Message from Client: {message.decode(encoding="utf-8")}', f'\nClient IP Address: {address}')
            self.server_socket.sendto(message, (self.MCAST_GRP, self.CLIENT_PORT))

    def server_health_loop(self):
        while True:
            self.server_socket.sendto(b'~health check', (self.MCAST_GRP, self.CLIENT_PORT))
            sleep(7)

    def send_msg(self, msg: bytes):
        self.client_socket.sendto(msg, self.server_address_port)

    def receive_msg(self):
        while True:
            self.client_socket.settimeout(20)
            try:
                data, address = self.client_socket.recvfrom(self.BUFFER_SIZE)
                if data:
                    if data.decode('utf-8') == "~gen_num":
                        # print('received gen command')
                        self.send_number()
                    elif data.decode('utf-8') == "~health check":
                        continue
                    elif data.decode('utf-8').isnumeric():
                        # print('received number')
                        num = int(data.decode('utf-8'))
                        self.numbers.append((num, address))
                    else:
                        print(f'Message from Server: {data.decode("utf-8")}')
            except Exception as e:
                print(e)
                self.send_cmd_to_rnd()
                continue

    def get_input(self):
        while True:
            try:
                msg = input()
                if msg:
                    self.send_msg(msg.encode('utf-8'))
            except UnicodeDecodeError:
                break

    def run(self):
        tr_listen = threading.Thread(target=self.receive_msg)
        tr_send = threading.Thread(target=self.get_input)
        tr_listen.start()
        tr_send.start()
        tr_listen.join()
        tr_send.join()
        self.tr_server.join()
        self.tr_server_health.join()
        self.tr_choice.join()


if __name__ == '__main__':
    client = Client()
    client.run()
