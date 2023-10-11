import socket
from _thread import *

port = int(input("Enter room number"))
name = str(input("Enter your username:"))

connection = socket.socket()
connection.connect(('localhost',port))
running = True
connection.send(name.encode())
def reciveData():
	global running
	while running:
		try:
			rec = str(connection.recv(4096).decode())
			if len(rec) > 0:
				if ("HOST" in rec and "LEFT" in rec) or "quit" in rec or ("HOST" in rec and "KICK" in rec):
					connection.close()
					running = False
					break
				print(rec)
		except:
			continue

while running:
	start_new_thread(reciveData, ())
	try:
		msg = str(input())
		if msg == "quit" and running != False:
			connection.send("quit".encode())
			connection.close()
			break
	except:
		break	
	connection.send(msg.encode())