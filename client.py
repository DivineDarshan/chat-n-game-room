import socket
from _thread import *
import common

port = int(input("Enter room number: "))
name = str(input("Enter your username: "))

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
				if len(rec) <= 3:
					if (int(rec) == common.__CLOSE__) or (int(rec) == common.__EXIT__)  or (int(rec) == common.__KICK__):
						running = False
						connection.close()
						break
				print(rec)
		except error as e:
			continue

while running:
	start_new_thread(reciveData, ())
	try:
		msg = str(input())
		if msg == "QUIT":
			connection.send(str(common.__EXIT__).encode())
			connection.close()
			break
		connection.send(msg.encode())
	except:
		break	