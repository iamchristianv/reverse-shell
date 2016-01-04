# reverse-shell

reverse-shell is a multi-threaded reverse shell program to remotely manage files on other computers simultaneously.


**Written in Python 2.7 and Executable from the command line (./server.py or ./client.py).** 


In order to run reverse-shell, server.py must be run on a computer first in order to prepare for accepting connections from other clients. Once server.py is running on a computer, client.py can be run from other remote computers, as long as the IP address of the computer running server.py is included in parentheses in main() of client.py (e.g. Client(“192.168.1.1”)). 

Use the **list** command to see a list of all available connections from clients. 

**EXAMPLE:**

(ID)       (IP Address)      (Port Number)
---------- Connections ----------
0          192.168.1.1          40201
1          127.0.0.1            51012

Use the **select {ID}** command to select a connection to connect with and manage its files.

Use the **done** command to exit out of a connection with a computer.

Use the **quit** command to exit out of reverse-shell. 