# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = "127.0.0.1"
Port = 5010
server.bind((IP_address, Port))


server.listen(100)

list_of_clients = []


def clientthread(conn: socket.socket, addr):
    print("Welcome to this chatroom!")
    print(conn)
    print(addr)
    conn.send("Welcome to this chatroom!".encode())

    while True:
        print(1)
        try:
            message = conn.recvfrom(2048)
            if message:

                """prints the message and address of the
                user who just sent the message on the server
                terminal"""
                print("<" + addr[0] + "> " + message)

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(conn)

        except:
            continue


"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                # if the link is broken, we remove the client
                remove(clients)



def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()
    list_of_clients.append(conn)

    print(addr[0] + " connected")
    start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()