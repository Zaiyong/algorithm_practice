import numpy as np
import random
class Queen:
    def __init__(self,index,available):
        self.index=index
        self.available=available

    def move(self):
        self.available=False

    def resetMove(self):
        self.available=True

def checkValid(chess_table,move):
    x=move[0]
    y=move[1]
    for i in range(0,8):
        if chess_table[x,i]==1 or chess_table[i,y]==1:
            return False
        if x+i<8:
            if y+i<8 and chess_table[x+i,y+i]==1:
                return False
            if y-i>=0 and chess_table[x+i,y-i]==1:
                return False
        if x-i>=0:
            if y+i<8 and chess_table[x-i,y+i]==1:
                return False
            if y-i>=0 and chess_table[x-i,y-i]==1:
                return False
    return True

def allPossibleMoves(chess_table):
    possible_moves=[]
    for i in range(8):
        for j in range(8):
            if chess_table[i][j]==0:
                possible_moves.append([i,j])
    random.shuffle(possible_moves)
    return possible_moves

def NextQueen(queens):
    for i in range(8):
        if queens[i].available==True:
            return i
    return -1

def initEightQueens():
    queens=[]
    for i in range(8):
        queens.append(Queen(i,True))
    return queens

def putQueen(queens,chess_table):
    next_queen_index=NextQueen(queens)
    if next_queen_index==-1:
        return True
    for move in allPossibleMoves(chess_table):
        if checkValid(chess_table,move):
            queens[next_queen_index].move()
            chess_table[move[0]][move[1]]=1
            if putQueen(queens,chess_table):
                return True
            queens[next_queen_index].resetMove()
            chess_table[move[0]][move[1]]=0
    return False

if __name__=='__main__':
    chess_table=np.zeros((8,8),dtype=int)
    queens=initEightQueens()
    if putQueen(queens,chess_table):
        print(chess_table)
