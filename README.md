# reverse-shell
reverse-shell is a multi-threaded reverse shell program for remotely managing files on other computers simultaneously.

## Description
reverse-shell was written in Python 2.7 and is intended to be used on a command line. With reverse-shell, you can
run the server program on your computer and remotely manage the files on other computers that run the client
program and connect to you.

While running reverse-shell as a server, you can view all the connections from computers that have connected to you, and
you can directly manage a connection so that you can manage the files on any connected computers. Since it is multi-
threaded, reverse-shell also notifies you the moment that a new computer connects to you.

## Details
reverse-shell has currently only been tested on Mac computers. Furthermore, reverse-shell as a server can only send
commands where the client returns output, and does not work properly on commands that require additional input other
than the input required normally for the command line.