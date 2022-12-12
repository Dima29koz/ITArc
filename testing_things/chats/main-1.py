import socket
import struct
import random


class Server:
    server_name = ""
    bHost = True
    biggest_number = 0
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007
    IS_ALL_GROUPS = True
    server_number = random.randint(0, 100)
    number_sent = False

    def __init__(self, name):
        self.server_name = name

    def send_string(self, string):
        MULTICAST_TTL = 2
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sender_socket.sendto(string.encode('utf-8'), (self.MCAST_GRP, self.MCAST_PORT))

    def send_number(self):
        server_number_encoded = str(self.server_number)
        self.send_string(server_number_encoded)
        print("Number: " + str(self.server_number))

    def send_status(self):
        self.send_string(str(self.bHost))
        print("Host status: " + str(self.bHost))

    def call_send_status(self):
        self.send_string("send_status")
        print("status check called")

    def server_loop(self, sock):
        while True:
            data, address = sock.recvfrom(1024)
            received_string = str(data)
            if received_string.isnumeric():
                received_number = int(received_string)
                if received_number > self.server_number:
                    self.biggest_number = received_number
                if self.biggest_number < self.server_number:
                    self.bHost = True
                else:
                    self.bHost = False
                if not self.number_sent:
                    self.send_number()
            else:
                if received_string == "send_status":
                    self.send_status()

    def init_server(self, IS_ALL_GROUPS=True):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            sock.bind(('', self.MCAST_PORT))
        else:
            sock.bind((self.MCAST_GRP, self.MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.send_number()
        self.number_sent = True
        self.call_send_status()
        self.server_loop(sock)


server_index = random.randint(0, 100)
server = Server("Server")
server.server_name = "Server" + str(server.server_number)
server.init_server()
