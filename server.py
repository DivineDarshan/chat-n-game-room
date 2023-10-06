import socket
import threading

class Server:
	def __init__(self, host="localhost", port=5020):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.host = host
		self.port = port
		self.isServerRunning = False
		self.clients = []

	def Log(self,msg, sender=0):
		if sender == 0:
			print("server: " + msg)
		else:
			print(sender + ": " + msg)

	def	listenToClient(self, client, address):
		self.broadcast(str(address)[13:19] + " connected")
		while self.isServerRunning:
			try:
				msg = str(client.recv(4096).decode())
				if msg:
					if msg == "quit":
						self.clients.remove(client)
						client.close()
						#self.closeServer() #not close but leave
						break
					self.Log(msg, str(address)[13:19])
					msg = str(address)[13:19] + msg
					self.broadcast(msg)

			except:
				continue 

	def closeServer(self):
		self.isServerRunning = False
		self.server.close()

	def broadcast(self, msg):
		for c in self.clients:
			try:
				c.send(msg.encode())
			except: 
				self.clients.remove(c)
				c.close()

	def accept(self):
		while (self.isServerRunning): 
			try: 
				client, address = self.server.accept()
				self.clients.append(client)
				self.Log(str(address)[13:19] + " connected")
				threading.Thread(target=self.listenToClient,args=(client, address)).start()
			except:
				continue

	def startServer(self):
		self.server.bind((self.host,self.port))
		self.server.listen()
		self.isServerRunning = True
		self.accept()

server = Server("localhost", 5020)
server.startServer()

#leaving
#kick