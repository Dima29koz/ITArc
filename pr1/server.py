import socket
import sys


class Server:
    def __init__(self):
        self.local_ip = "192.168.1.118"
        self.server_port = 5010
        self.buffer_size = 1024
        self.hello_msg = "Hello UDP Client"
        self.hello_msg_int = "1234"
        self.byte_hello_msg = self.hello_msg.encode()
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        self.udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_server_socket.bind((self.local_ip, self.server_port))
        print("UDP server up and listening")
        self.listen()

    def listen(self):
        while True:
            bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)
            message = bytes_address_pair[0]
            address = bytes_address_pair[1]
            print(f'Message from Client: {message.decode(encoding="utf-8")}')
            print(f'Client IP Address: {address}')
            # self.send_msg(message, address)
            self.broadcast(message)

    def broadcast(self, msg: bytes):
        self.udp_server_socket.sendto(msg, ('255.255.255.255', 5011))

    def send_msg(self, msg: bytes, address: tuple[str, int]):
        self.udp_server_socket.sendto(msg, address)


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, sys.byteorder)


if __name__ == '__main__':
    serv = Server()
