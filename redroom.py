import tkinter as tk
from server import Server

def createRoom():
	serverid = int(serverid_entry.get())
	root.destroy()
	room = Server(host="localhost",port=serverid)
	room.startServer()
	

root = tk.Tk()
root.title("create room")
root.geometry("1200x700")

serverid_label = tk.Label(root, text="Server id")
serverid_label.pack()

serverid_entry = tk.Entry(root)
serverid_entry.pack()

submit_button = tk.Button(root, text="Create", command=createRoom)
submit_button.pack()

root.mainloop()
