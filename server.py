import socket


class Server(object):
    sckt = None
    addresses = []
    connections = []

    def __init__(self):
        self.sckt = socket.socket()
        self.sckt.bind(("", 10101))
        self.sckt.listen(5)

    def accept_connections(self):
        index = len(self.connections)
        self.connections[index], self.addresses[index] = self.sckt.accept()

    def remove_connection(self, index):
        del self.addresses[index]
        del self.connections[index]

    def show_clients(self):
        # should show connections and prompt for input
        pass

    def send_commands(self, index):
        while True:
            command = raw_input(">> ")
            if command == "quit":
                break
            if len(command) > 0:
                self.connections[index].send(command)
                response = str(self.connections[index].recv(1024))
                print(response)
        self.show_clients()

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.sckt.close()
