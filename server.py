#!/usr/bin/env python

import socket
import threading
import sys


class Server(object):
    sckt = None
    addresses = []
    connections = []
    connected = False

    # creates a socket, waits for connections from clients, and initiates the main menu for the user
    def start(self):
        self.create_socket()
        self.create_threads()

    # creates a socket to accept connections from clients
    def create_socket(self):
        try:
            self.sckt = socket.socket()
            self.sckt.bind(("", 10101))
            self.sckt.listen(5)
        except socket.error:
            print("\nUnable to configure socket at the moment.")
            print("Please try again in a few minutes.\n")
            sys.exit()

    # creates two threads to simultaneously accept connections from clients and manage input from the user
    def create_threads(self):
        for number in range(2):
            thread = None
            if number == 0:
                thread = threading.Thread(target=self.accept_connections)
            elif number == 1:
                thread = threading.Thread(target=self.show_main_menu())
            thread.daemon = True
            thread.start()

    # accepts connections from clients and adds them to the lists of connections and addresses
    def accept_connections(self):
        try:
            connection, address = self.sckt.accept()
            self.connections.append(connection)
            self.addresses.append(address)
            # checks if the output will interrupt the user managing a connection with a client
            if not self.connected:
                print("\n- connection established with IP address " + address[0])
                print("- select 1 to see more information on all connections\n")
                print("Select an option: ")
        except socket.error:
            print("\n- unable to accept a connection\n")

    # manages input from the user for the main menu
    def show_main_menu(self):
        menu_selections = ("\n1) Show Connections", "2) Manage Connection", "3) Quit Program")
        while True:
            for menu_selection in menu_selections:
                print(menu_selection)
            selection = raw_input("\nSelect an option: ")
            if not selection.isdigit():
                print("- selection not a number")
            elif int(selection) == 1:
                self.show_connections()
            elif int(selection) == 2:
                self.select_connection()
            elif int(selection) == 3:
                break
            else:
                print("- selection not available")
        self.close_connections()

    # shows a list of available connections to the user
    def show_connections(self):
        print("\n----------- Connections -----------")
        for index, address in enumerate(self.addresses):
            try:
                # sends a message to each connection in the list to determine which are still available
                self.connections[index].send("?")
                self.connections[index].recv(4096)
            except socket.error:
                # if an exception occurs, then the connection is no longer available
                self.remove_connection(index)
                continue
            print("\nID: " + str(index) + (" " * 5) + "IP: " + address[0] + (" " * 5) + "PORT: " + str(address[1]))
        if len(self.connections) == 0:
            print("\n           No Connections")
        print("\n-----------------------------------")

    # lets the user to select a connection to manage from a list of connections
    def select_connection(self):
        if len(self.connections) == 0:
            print("- no connections available")
            return
        while True:
            self.show_connections()
            print("\nEnter 'back' to return to main menu")
            selection = raw_input("\nSelect a connection ID: ")
            if selection.lower() == "back":
                break
            if not self.error_check_selection(selection):
                self.establish_connection(int(selection))
                break

    # checks whether the user entered an appropriate ID based on available connections
    def error_check_selection(self, argument):
        if not argument.isdigit():
            print("- " + argument + " is not a number")
            return True
        index = int(argument)
        if index >= len(self.connections):
            print("- connection " + str(index) + " is not available")
            return True
        elif self.connections[index] is None:
            print("- connection " + str(index) + " is not available")
            self.remove_connection(index)
            return True
        return False

    # directly connects the user to the connection selected
    def establish_connection(self, index):
        self.connected = True
        print("\nEnter 'done' to exit the connection\n")
        while True:
            # commands entered by the user are processed by the client
            command = raw_input(self.addresses[index][0] + "> ")
            if command == "done":
                break
            elif len(command) > 0:
                try:
                    # commands are sent to the client, and the output is returned to the server
                    self.connections[index].send(command)
                    response = str(self.connections[index].recv(4096))
                    print(response)
                except socket.error:
                    # if an exception occurs, then the client closed the connection while the user was managing it
                    print("- lost connection")
                    break
        self.connected = False

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
