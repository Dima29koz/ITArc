import random
import socket
import struct
import threading


class Client:
    MCAST_GRP = '224.3.29.71'
    MCAST_PORT = 5010
    CLIENT_PORT = 5011
    BUFFER_SIZE = 1024

    def __init__(self):
        self.server_address_port = None
        self.broadcast_listen_socket = self.create_socket(('', self.CLIENT_PORT), True)
        self.server_socket = None
        self.tr_server = None
        self.max_number = 0
        if not self.check_server():
            self.create_server()
            self.check_server()

    def send_cmd_to_rnd(self):
        self.broadcast_listen_socket.sendto(
            '~gen_num'.encode('utf-8'),
            (self.MCAST_GRP, self.CLIENT_PORT))

    def send_number(self):
        number = random.randint(0, 100)
        self.broadcast_listen_socket.sendto(
            str(number).encode('utf-8'),
            (self.MCAST_GRP, self.CLIENT_PORT))

    def create_server(self):

        self.server_socket = self.create_socket(('', self.MCAST_PORT))
        self.tr_server = threading.Thread(target=self.server_loop)
        self.tr_server.start()
        print('server started')

    def create_socket(self, address, timeout=False):
        listen_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP)
        listen_socket.bind(address)
        group = socket.inet_aton(self.MCAST_GRP)
        listen_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL', group, socket.INADDR_ANY))
        if timeout:
            listen_socket.settimeout(1)
        return listen_socket

    def check_server(self):
        self.broadcast_listen_socket.sendto("client connected".encode(), (self.MCAST_GRP, self.MCAST_PORT))
        try:
            data, address = self.broadcast_listen_socket.recvfrom(self.BUFFER_SIZE)
        except TimeoutError:
            print('create server')
            return False
        else:
            print('server exists')
            print(data.decode('utf-8'))
            print(address)
            self.server_address_port = address
            return True

    def server_loop(self):
        while True:
            message, address = self.server_socket.recvfrom(self.BUFFER_SIZE)
            # print(f'Message from Client: {message.decode(encoding="utf-8")}')
            # print(f'Client IP Address: {address}')
            if message.decode('utf-8') == "~gen_num":
                print('generate and send')
            self.server_socket.sendto(message, (self.MCAST_GRP, self.CLIENT_PORT))

    def send_msg(self, msg: bytes):
        self.broadcast_listen_socket.sendto(msg, self.server_address_port)

    def receive_msg(self):
        while True:
            try:
                data, address = self.broadcast_listen_socket.recvfrom(self.BUFFER_SIZE)
                if data:
                    print(f'Message from Server: {data.decode("utf-8")}')
            except:
                continue

    def get_input(self):
        while True:
            msg = input()
            if msg:
                self.send_msg(msg.encode('utf-8'))

    def run(self):
        tr_listen = threading.Thread(target=self.receive_msg)
        tr_send = threading.Thread(target=self.get_input)
        tr_listen.start()
        tr_send.start()
        tr_listen.join()
        tr_send.join()
        self.tr_server.join()


if __name__ == '__main__':
    client = Client()
    client.run()
