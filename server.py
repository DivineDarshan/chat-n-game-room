import socket
import threading
import subprocess

class Client:
	def __init__(self,name="noname", host="localhost", port=5020, connection = None, address="undefined", isHost=False) -> None:
		self.host = host
		self.post = port
		self.name = name
		self.connection = connection
		self.address = address
		self.isHost = isHost

class Server:
	def __init__(self, host="localhost", port=5020):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.host = host
		self.port = port
		self.isServerRunning = False
		self.clients = []

	def Log(self,msg):
		print(str(msg))

	def	listenToClient(self, client):
		while self.isServerRunning:
			try:
				msg = str(client.connection.recv(4096).decode())
				if msg:
					m = f"{client.name}({client.address}): {msg}"
					if msg in "quit":
						if client.name == "HOST":
							self.Log(m)
							self.broadcast(m)
							self.closeServer()
							break
						m = f"{client.name}({client.address}): LEFT"
						self.Log(m)
						self.broadcast(m)
						self.clients.remove(client)
						client.connection.close()
						break
					else:
						self.Log(m)
						self.broadcast(m)
			except:
				continue

	def closeServer(self):
		self.isServerRunning = False
		self.broadcast("quit")
		for c in self.clients:
			c.connection.close()
		self.server.close()

	def broadcast(self, msg):
		for c in self.clients:
			try:
				c.connection.send(msg.encode())
			except: 
				self.clients.remove(c)
				c.connection.close()

	def accept(self):
		while (self.isServerRunning): 
			try: 
				_client, _address = self.server.accept()
				name = str(_client.recv(4096).decode())
				isHost = False
				if name == "HOST":
					isHost = True
				client = Client(name=name, host="localhost", port=5020, connection=_client, address=str(_address)[14:19], isHost=isHost)
				self.clients.append(client)
				self.Log(client.address + " JOINED")
				self.broadcast(client.address + " JOINED")
				threading.Thread(target=self.listenToClient,args=(client,)).start()
			except:
				continue

	def joinServer(self):
		subprocess.call("start /wait python client.py", shell=True)

	def startServer(self):
		self.server.bind((self.host,self.port))
		self.server.listen()
		self.isServerRunning = True
		threading.Thread(target=self.joinServer,args=()).start()
		self.accept()

	def sentPersonalMsg(self, msg, id):
		for c in self.clients: 
			if c.port == id:
				try:
					c.connection.send(msg.encode());
				except:
					self.clients.remove(c)
					c.connection.close()


server = Server("localhost", 5020)
server.startServer()

#TODO personal message
#TODO kick
#TODO tag and chat
