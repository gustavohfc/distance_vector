#!/usr/bin/python

import socket

server_address = '127.0.0.1'
server_port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = (server_address, server_port)

while True:
	msg = raw_input()
	sock.sendto(msg, server)
