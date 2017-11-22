#!/usr/bin/python

import socket

server_address = socket.gethostname()
server_port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

while True:
	msg, client_address = sock.recvfrom(1024)
	print(str(client_address) + ": " + msg)
