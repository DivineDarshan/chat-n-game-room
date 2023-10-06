import socket
import threading
from _thread import *

# connection = socket.socket()
# connection.connect(('localhost',5021))

# running = True

# def reciveData():
# 	global running
# 	while running:
# 		try:
# 			rec = str(connection.recv(4096).decode())
# 			if len(rec) > 6:
# 				sender = rec[0:6]
# 				msg = rec[6:]
# 				print(sender + ": " + msg)
# 				if "quit" == msg:
# 					connection.close()
# 					running = False
# 					break
# 		except:
# 			continue

# while running:
# 	start_new_thread(reciveData, ())
# 	msg = str(input())
# 	connection.send(msg.encode())
# 	if msg == "quit":
# 		connection.close()
# 		break	

class Client:
	def __init__(self,name="noname", host="localhost", port=5020) -> None:
		self.host = host
		self.post = port
		self.name = name
		self.connection = socket.socket()
		self.connection.connect((self.host,self.port))
		self.isConnected = True
		self.connectionObject = None
		self.address = None
		self.writeData();

	def setConnectionObject(self, connectionObject, address):
		self.connectionObject = connectionObject
		self.address = address

	def writeData(self):
		while self.isConnected:
			msg = str(input())
			self.connection.send(msg.encode())
			threading.Thread(self.reciveData, ()).start()
			if msg == "quit":
				self.connection.close()
				break
	
	def reciveData(self):
		while self.isConnected:
			try:
				rec = str(self.connection.recv(4096).decode())
				if len(rec) > 6:
					sender = rec[0:6]
					msg = rec[6:]
					print(sender + ": " + msg)
					if "quit" == msg:
						self.connection.close()
						self.isConnected = False
						break
			except:
				continue

#for what will client be used for 
#for servers or for other purposes

client = Client(name="vedant", host="localhost", port=5020)