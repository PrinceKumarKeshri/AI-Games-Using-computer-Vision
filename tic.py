import os
from random import randint

CLEAR = "clear" if os.name == "posix" else "cls"

class tictaktoe:
    def __init__(self,game):
        self.game = game

    def pvp(self,player,row,column): # makes the moves and decides the next step.
        if player: # Player 1 i.e. "X"
            if self.check_pos(row, column):
                self.game[row][column]=1
                output=["",True,not player]
            else:output=["Position already occupied.",True,player]
        else: # Player 2 i.e. "O"
            if self.check_pos(row, column):
                self.game[row][column]=-1
                output=["",True,not player]
            else:output=["Position already occupied.",True,player]
        if self.check_tie():
            output=["It's Tie",False,player]
        if self.check_win():
            if player:output=["'X' Won!",False,player]
            else: output=["'O' Won!",False,player]
        return output

    def check_win(self) -> bool: # Check if someone won or not
        game=self.game
        win = False
        if game[1][1] !=0:
            if game[0][0]==game[1][1] and game[1][1]==game[2][2]:
                win = True
            elif game[0][2]==game[1][1] and game[1][1]==game[2][0]:
                win = True
            if win:
                return win
        l=[0,0,0]
        for row in game:
            if (1 not in row or -1 not in row) and 0 not in row:
                win = True
                return win
            else:
                for i in range(3):
                    if row[i]!=0:
                        l[i]+=row[i]
        if -3 in l or 3 in l:
            win = True
        return win

    def check_tie(self) -> bool: # Checks if game is tied or not
        for row in self.game:
            if 0 in row:
                return False
        return True

    def check_pos(self,row,column) -> bool: # Checks if a perticular position is empty or not
        return True if self.game[row][column]==0 else False
    
    def print_board(self) -> None:
        print("    0   1   2\n")
        for count, row in enumerate(self.game):
            print(count,end="  ")
            for i in range(len(row)):
                if row[i]==1:
                    print(f" X ",end="")
                elif row[i]==-1:
                    print(f" O ",end="")
                else:
                    print(f"   ",end="")
                if i!=2:
                    print("|",end="")
                else:
                    print("")
            if count!=2:
                print("   -----------")
        print("")
    
    def minimax(self,alpha,beta,isMaximizing,depth=0):
        """
            This Algorithm is using Minimax Algorithm with
            Alpha-Beta Pruning.
        """
        # Terminating Conditions
        if self.check_win():
            return -1 if isMaximizing else 1
        if self.check_tie() or depth ==5:
            return 0

        # If the game continues
        bestScore = float("-inf") if isMaximizing else float("inf")
        for row in range(len(self.game)):
            for col in range(len(self.game[row])):
                if self.check_pos(row, col):
                    self.game[row][col] = 1 if isMaximizing else -1
                    score = self.minimax(alpha,beta,isMaximizing=False if isMaximizing else True,depth=depth+1)
                    self.game[row][col] = 0
                    if isMaximizing: # this is human player
                        bestScore=max(score,bestScore)
                        alpha = max(alpha,bestScore)
                    else: # this is AI
                        bestScore=min(score,bestScore)
                        beta = max(beta,bestScore)
            if beta<=alpha:
                break
        return bestScore

    def AI(self):
        """
            AI is always (O) or player 2.
            The value of AI on game board is -1.
        """
        bestscore = float("inf")
        bestmove = [0,0]
        for row in range(len(self.game)):
            for col in range(len(self.game[row])):
                if self.check_pos(row, col):
                    self.game[row][col] = -1
                    score = self.minimax(float("-inf"),float("inf"),isMaximizing=True)
                    self.game[row][col] = 0
                    if score<bestscore:
                        bestscore=score
                        bestmove=[row,col]
        return bestmove
        

if __name__=="__main__":
    game= [[ 0, 0, 0 ],
            [ 0, 0, 0 ],
            [ 0, 0, 0 ]]
    start = tictaktoe(game)
    while True:
        player = int(input("Choose one of the following:\n1.P v P\n2.CPU vs P\n=> "))
        if player == 1:
            print("Player 1 is 'X' and Player 2 is 'O'\nTo make a move enter row and column number")
            print("First Input row then input column seperated with a space\n")
            loop=True
            while loop: # Driver loop of pvp game
                start.print_board()
                try:
                    if player: # Player 1 i.e. "X"
                        row,column = map(int,input("Player 1 =>").strip().split(" "))
                    else: # Player 2 i.e. "O"
                        row,column = map(int,input("Player 2 =>").strip().split(" "))
                except ValueError: #Value error
                    print("Please insert correct values.")
                    continue
                string,loop,player=start.pvp(player,row,column)
                os.system(CLEAR)
                print(string)
            start.print_board()
        elif player == 2:
            player=0#randint(0,1) # randomize the player to randomize which player will move first
            print("You are 'X' and AI is 'O'\nTo make a move enter row and column number")
            print("First Input row then input column seperated with a space\n")
            loop=True
            while loop: # Driver loop of pvp game
                start.print_board()
                if player: # Player 1 i.e. "X"
                    try:
                        row,column = map(int,input("Your Turn =>").strip().split(" "))
                    except ValueError: #Value error
                        print("Please insert correct values.")
                        continue
                    string,loop,player=start.pvp(player,row,column)
                    os.system(CLEAR)
                    print(string)
                else: # Player 2 i.e. "O"
                    row,column = start.AI()
                    string,loop,player=start.pvp(player,row,column)
                    os.system(CLEAR)
                    print(string)
            start.print_board()
        else:
            print("Wrong input! Enter Again")
        break