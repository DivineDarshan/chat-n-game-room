import socket
import threading
import subprocess
import re
import common
import tkinter as tk

class Client:
	def __init__(self,name="Default user", host="localhost", port=5020, connection = None, address=None, isHost=False) -> None:
		self.host = host
		self.port = port
		self.name = name
		self.connection = connection
		self.address = address
		self.isHost = isHost
		self.screen = None
class Server:
	def __init__(self, host="localhost", port=5020):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		self.host = host
		self.port = port
		self.isServerRunning = False
		self.clients = []
		self.listOfMessage = []

	def Log(self,msg):
		self.listOfMessage.append(str(msg))
		label = tk.Label(self.screen, text=str(msg))
		label.pack()
		print(str(msg))

	def	listenToClient(self, client):
		while self.isServerRunning:
			try:
				msg = str(client.connection.recv(4096).decode())
				if msg:
					m = f"{client.name}({client.address}): {msg}"
					self.Log(m)
					if '@' in msg:
						pattern = r'@(\d{5})'
						user_ids = re.findall(pattern, msg)
						for c in self.clients:
							if str(c.address) in user_ids:
								try:
									c.connection.send(m.encode())
								except: 
									self.clients.remove(c)
									c.connection.close()
					elif msg == str(common.__EXIT__):
						if client.name == "HOST":
							self.broadcast(str(common.__CLOSE__))
							self.closeServer()
							break
						m = f"{client.name}({client.address}): LEFT"
						self.broadcast(m)
						self.clients.remove(client)
						client.connection.close()
						break
					else:
						self.broadcast(m)
			except:
				continue
	def closeServer(self):
		self.isServerRunning = False
		self.broadcast(str(common.__EXIT__))
		for c in self.clients:
			c.connection.close()
		self.server.close()
		self.screen.destroy()
		return

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
				self.Log(f"{client.name} JOINED AT {client.address}")
				self.broadcast(f"{client.name} JOINED AT {client.address}")
				threading.Thread(target=self.listenToClient,args=(client,)).start()
			except:
				continue

	def joinServer(self):
		subprocess.call(f"start /wait pythonw client.py {self.port}", shell=True)

	def startServer(self):


		self.server.bind((self.host,self.port))
		self.server.listen()
		self.isServerRunning = True
		
		self.screen = tk.Tk()
		self.screen.title(str(self.port)) 
		self.screen.geometry("200x700")

		threading.Thread(target=self.joinServer,args=()).start()
		threading.Thread(target=self.accept,args=()).start()
		self.screen.mainloop()