# reverse-shell

##Description##
reverse-shell is a multi-threaded reverse shell program to remotely manage files on other computers simultaneously.

In order to run reverse-shell, server.py must be run on a computer first in order to prepare for accepting connections from other clients. Once server.py is running on a computer, client.py can be run from other remote computers, as long as the IP address of the computer running server.py is included in parentheses in main() of client.py (e.g. Client(“192.168.1.1”)). 

Written in Python 2.7 and Executable from the command line (**./server.py** or **./client.py**).


##Commands##
Use the **list** command to see a list of all available connections from clients. 

Use the **select {ID}** command to select a connection to connect with and manage its files.
- **{ID}** corresponds to the leftmost number seen after running the **list** command.

Use the **done** command to exit out of a connection with a computer.

Use the **quit** command to exit out of reverse-shell. 