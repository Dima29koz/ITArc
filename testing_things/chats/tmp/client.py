import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '127.0.0.1'
Port = 5010
server.connect((IP_address, Port))

while True:
    sockets_list = [sys.stdin, server]

    try:
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    except OSError:
        read_sockets = [sys.stdin]
    for socks in read_sockets:
        if socks == server:
            message = socks.recvfrom(2048)
            print(message)
        else:
            message = input('<<<')
            # message = sys.stdin.readline()
            server.send(message.encode())
            print(f'<You>{message}')
            # sys.stdout.write("<You>")
            # sys.stdout.write(message)
            # sys.stdout.flush()
server.close()