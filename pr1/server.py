import socket
import struct
import sys


class Server:
    MCAST_GRP = '224.3.29.71'
    MCAST_PORT = 5010
    BUFFER_SIZE = 1024

    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.udp_server_socket = self.create_socket()
        print("UDP server up and listening")
        self.listen()

    def create_socket(self):
        server_socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_DGRAM,
            proto=socket.IPPROTO_UDP)
        server_socket.bind(('', self.MCAST_PORT))
        group = socket.inet_aton(self.MCAST_GRP)
        server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL', group, socket.INADDR_ANY))
        return server_socket
        # self.udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.udp_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        # self.udp_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        # self.udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # group = socket.inet_aton(MCAST_GRP)
        # mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        # self.udp_server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        # self.udp_server_socket.setsockopt(
        #     socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.local_ip))
        # self.udp_server_socket.setsockopt(
        #     socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(self.local_ip))

    def listen(self):
        while True:
            message, address = self.udp_server_socket.recvfrom(self.BUFFER_SIZE)
            print(f'Message from Client: {message.decode(encoding="utf-8")}')
            print(f'Client IP Address: {address}')
            # self.send_msg(message, address)
            self.broadcast(message)

    def broadcast(self, msg: bytes):
        self.udp_server_socket.sendto(msg, ('224.3.29.71', 5011))

    def send_msg(self, msg: bytes, address: tuple[str, int]):
        self.udp_server_socket.sendto(msg, address)


if __name__ == '__main__':
    serv = Server()
