import socket
from _thread import start_new_thread
from tkinter import messagebox
import tkinter as Tk
from functools import partial
import sys

server=socket.socket((socket.AF_INET),(socket.SOCK_STREAM))
host = "localhost" 
port = int(sys.argv[1])
server.bind((host,port))
server.listen(50)
c , ad=server.accept()

window = Tk.Tk()
window.title("Tic Tac Toe")
window.geometry("300x300")

player_symbol = 'O'
Opponent_symbol = 'X'

my_turn =0
def clicked( i, j ):
	global my_turn
	global player_symbol
	global c  
	if (button[i][j]["text"]== ' ' and my_turn==1) :
		button[i][j]["text"]= player_symbol
		button_number = i*3+j
		c.send(str(button_number).encode('utf-8'))
		my_turn=0
		check(player_symbol)
interation = 1
def check(turn):
	global interation
	global player_symbol
	win = 0 
	for i in range(3):
		if (button[i][0]["text"]==button[i][1]["text"] and button[i][0]["text"]==button[i][2]["text"] and button[i][0]["text"] != " " ) or (button[0][i]["text"]==button[1][i]["text"] and button[0][i]["text"]==button[2][i]["text"] and str(button[0][i]["text"]) != " " ):
			if(turn==player_symbol):
				messagebox.showinfo("showinfo" , "Congratulations! You won ")
			else:
				messagebox.showerror("showerror" , "Better Luck Next Time")
			win==1
			reset()

	if win ==0:
		if((button[0][0]["text"]==button[1][1]["text"] and button[0][0]["text"]==button[2][2]["text"] and button[0][0]["text"] != " " )or (button[0][2]["text"]==button[1][1]["text"] and button[0][2]["text"]==button[2][0]["text"] and str(button[0][2]["text"]) != " " )):
			if(turn==player_symbol):
				messagebox.showinfo("showinfo" , "Congratulations! You won ")
			else:
				messagebox.showerror("showerror" , "Better Luck Next Time")
			win==1
			reset()
	
	if win==0 and interation==9:
		messagebox.showinfo("showinfo" , "No Player Won")
		reset()
	
	interation = interation + 1  

def reset():
	global interation
	global my_turn
	global button
	for i in range(3):
		for j in range(3):
			button[i][j].config(text=" ")
	my_turn = 0
	interation = 0

button = [[0 for _ in range (3)] for _ in range(3)]
for i in range(3):
	for j in range(3):
		button[i][j] = Tk.Button(window,text = " " , bg = "Red" , fg = "Black" , width = 8 , height = 4)
		button[i][j].config(command = partial(clicked , i , j ))
		button[i][j].grid(row=i+10 , column=j+3)
def recvThread (c):
	global button
	global my_turn
	while True:
		button_number = int(c.recv(1024).decode('utf-8'))
		row = int(button_number/3)
		column = int(button_number%3)
		button[row][column]["text"] = Opponent_symbol
		my_turn=1
		check(Opponent_symbol)

start_new_thread(recvThread , (c,))

window.mainloop()
