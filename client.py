import re
import socket
from _thread import *
import common
import tkinter as tk
import sys
import subprocess
import threading

port = 5000
name = "HOST"

if len(sys.argv) == 1:
	def submit():
		global name, port
		name = str(name_entry.get())
		port = int(port_entry.get())
		root.destroy()

	root = tk.Tk()
	root.title("create room")
	root.geometry("1200x700")

	name_label = tk.Label(root, text="Name")
	name_label.pack()
	name_entry = tk.Entry(root)
	name_entry.pack()

	port_label = tk.Label(root, text="Server id")
	port_label.pack()
	port_entry = tk.Entry(root)
	port_entry.pack()

	submit_button = tk.Button(root, text="Join", command=submit)
	submit_button.pack()
	root.mainloop()
else:
	port = int(sys.argv[1])
	host = "HOST"

screen = tk.Tk()
screen.title(f"Chat room")
screen.geometry("1200x700")
screen.resizable = False

msgFrame = tk.Frame(screen)
msgFrame.pack()

inputMsg = tk.Entry(screen)
inputMsg.bind("<Return>", (lambda event: inputText(inputMsg.get())))
inputMsg.place(x=100 ,y=650 ,height=50, width=1000)

connection = socket.socket()
connection.connect(('localhost',port))
running = True
connection.send(name.encode())
listOfMessages = []

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
						screen.destroy()	
						break
				listOfMessages.append(str(rec))
				label = tk.Label(msgFrame, text=str(rec))
				label.pack()
		except error as e:
			continue

start_new_thread(reciveData, ())

def runGame(flag, user_id):
	global name
	print(name)
	if flag==0:
		subprocess.call(args=f"start /wait pythonw game.py {user_id} {name}", shell=True)
	else:		
		subprocess.call(args=f"start /wait pythonw gameclient.py {user_id} {name}", shell=True)
	
def inputText(msg):
	inputMsg.delete(0, tk.END)
	msg = str(msg)
	try:
		if msg == "QUIT":
			connection.send(str(common.__EXIT__).encode())
			connection.close()
			screen.destroy()
		if msg.startswith("/game") and "@" in msg:
			user_id = str(connection.getsockname()[1])[:4]
			print(user_id)
			threading.Thread(target=runGame,args= (0,user_id)).start()
		if msg.startswith("/accept") and "@" in msg:
			pattern = r'@(\d{5})'
			user_id = str(re.findall(pattern, msg)[0])[:4]
			print(user_id)
			threading.Thread(target=runGame,args= (1,user_id)).start()
		connection.send(msg.encode())
	except:
		pass

screen.mainloop()