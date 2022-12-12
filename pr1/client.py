import socket
import threading


class Client:
    def __init__(self):
        self.server_address_port = ("192.168.1.118", 5010)
        self.broadcast_address_port = ("192.168.1.118", 5010)
        self.buffer_size = 1024
        self.udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        self.udp_client_socket.bind((ip, 5011))

        self.name = 'skipper'.encode()
        # self.search_server()

        self.hello_msg = f"client connected"
        self.byte_hello_msg = self.hello_msg.encode()
        self.send_msg(self.byte_hello_msg)

    def search_server(self):
        self.udp_client_socket.sendto(self.name, self.broadcast_address_port)

    def send_msg(self, msg: bytes):
        self.udp_client_socket.sendto(msg, self.server_address_port)

    def receive_msg(self):
        while True:
            try:
                msg_from_server = self.udp_client_socket.recvfrom(self.buffer_size)
                if msg_from_server:
                    print(f'Message from Server: {msg_from_server[0]}')
            except:
                continue

    def get_input(self):
        while True:
            msg = input()
            if msg:
                self.send_msg(msg.encode())


if __name__ == '__main__':
    client = Client()
    tr_listen = threading.Thread(target=client.receive_msg)
    tr_send = threading.Thread(target=client.get_input)
    tr_listen.start()
    tr_send.start()
    tr_listen.join()
    tr_send.join()

