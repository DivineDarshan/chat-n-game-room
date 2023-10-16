import tkinter as tk
from server import Server
import subprocess

def createRoom():
	serverid = int(serverid_entry.get())
	root.destroy()
	room = Server(host="localhost",port=serverid)
	room.startServer()

def joinRoom():
		root.destroy()
		subprocess.call(f"start /wait pythonw client.py", shell=True)

root = tk.Tk()
root.title("create room")
root.geometry("1200x700")

serverid_label = tk.Label(root, text="Server id")
serverid_label.pack()

serverid_entry = tk.Entry(root)
serverid_entry.pack()

submit_button = tk.Button(root, text="Create", command=createRoom)
submit_button.pack()

join_button = tk.Button(root, text="Join", command=joinRoom)
join_button.pack(padx=30)

root.mainloop()
