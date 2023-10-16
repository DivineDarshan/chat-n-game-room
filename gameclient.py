import socket
from _thread import start_new_thread
from tkinter import messagebox
import tkinter as Tk
from functools import partial
import sys

server=socket.socket((socket.AF_INET),(socket.SOCK_STREAM))
host = "127.0.0.1"
port = int(sys.argv[1])
server.connect((host,port))

window = Tk.Tk()
window.title("Tic Tac Toe")
window.geometry("300x300")

player_symbol = 'X'
Opponent_symbol = 'O'

my_turn =1 
def clicked(btns , i, j ):
    global my_turn
    global player_symbol
    global server  
    if (bts[i][j]["text"]== ' ' and my_turn==1) :
        bts[i][j]["text"]= player_symbol
        button_number = i*3+j
        server.send(str(button_number).encode('utf-8'))
        my_turn=0
        check(player_symbol)
interation = 1
def check(turn):
    global interation
    global bts 
    global player_symbol
    win = 0 
    for i in range(3):
        if ((bts[i][0]["text"]==bts[i][1]["text"] and bts[i][0]["text"]==bts[i][2]["text"] and bts[i][0]["text"]!= " " )
        or (bts[0][i]["text"]==bts[1][i]["text"] and bts[0][i]["text"]==bts[2][i]["text"] and bts[0][i]["text"]!= " " )):
            if(turn==player_symbol):
                messagebox.showinfo("showinfo" , "Congratulations! You won")
            else:
                messagebox.showerror("showerror" , "Better Luck Next Time")
            win==1
            reset()

    if win ==0:
        if ((bts[0][0]["text"]==bts[1][1]["text"] and bts[0][0]["text"]==bts[2][2]["text"] and bts[0][0]["text"]!= " " )
        or (bts[0][2]["text"]==bts[1][1]["text"] and bts[0][2]["text"]==bts[2][0]["text"] and bts[0][2]["text"]!= " " )):
            if(turn==player_symbol):
                messagebox.showinfo("showinfo" , "Congratulations! You won")
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
    global bts
    for i in range(3):
        for j in range(3):
            bts[i][j].config(text=" ")
    my_turn = 1
    interation = 0

bts = [[0 for x in range (3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        bts[i][j] = Tk.Button(window,text = " " , bg = "Red" , fg = "Black" , width = 8 , height = 4)
        bts[i][j].config(command = partial(clicked ,  bts[i][j] , i , j ))
        bts[i][j].grid(row=i+10 , column=j+3)
def recvThread (server):
    global bts
    global my_turn
    while True:
        button_number = int(server.recv(1024).decode('utf-8'))
        row = int(button_number/3)
        column = int(button_number%3)
        bts[row][column]["text"] = Opponent_symbol
        my_turn=1
        check(Opponent_symbol)

start_new_thread(recvThread , (server,))

window.mainloop()
