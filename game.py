import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" "," "," "] , [" "," "," "] , [" "," "," "] ]
        self.turn = "X" 
        self.you = "X"
        self.opponent = "Y"
        self.winner = None
        self.game_over = False

        self.counter = 0  

    def host_game(self,host,port):
        server = socket.socket()
        server.bind((host,port))
        server.listen(1)

        client , addr = server.accept()

        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection , args=(client,)).start()
        # server.close()

    def connect_to_game(self,host,port):
        client = socket.socket()
        client.connect((host,port))

        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection , args=(client,)).start()

    def handle_connection(self,client):
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row , column): ")
                if self.check_valid_move([move[:1],move[2:]]):
                    self.apply_move([move[:1],move[2:]], self.you)
                    self.turn = self.opponent
                    client.send(move.encode('utf-8'))
                else:
                    print("Invalid move!")
            else:
                data = client.recv(1824)
                if not data:
                    break
                else:
                    move = data.decode('utf-8')
                    k = [move[:1],move[2:]]
                    self.apply_move(k,self.opponent)
                    self.turn = self.you
        client.close()

    def apply_move(self , move , player):
        if self.game_over:
            return
        self.counter = self.counter + 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You win!")
                exit()
            elif self.winner == self.oppoennt:
                print("YOu lose!")
                exit()
        else:
            if self.counter ==9:
                print("It is a tie!!")
                exit()
    def check_valid_move(self,move):
        if int(move[0]) < 3 and int(move[1]) < 3:
            return self.board[int(move[0])][int(move[1])] == " "
        return False
    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True 
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False
    def print_board(self):
        for row in range(3):
            print(" ! ".join(self.board[row]))
            if row != 2:
                print("-----------")
