import numpy as np
import sys

class Point:
    def __init__(self,x,y,value=0):
        self.x=x
        self.y=y
        self.value=value
        self.possibilites=list(range(1,10))
        self.sub_group_x=self.x//3
        self.sub_group_y=self.y//3

    def removePossibility(self,removed_value):
        self.possibilites.remove(removed_value)

    def setValue(self,value):
        self.value=value

def readInput(input_file):
    return np.genfromtxt(input_file,delimiter=',',dtype=int)

def initAllPoints(input_matrix):
    all_points={}
    unfixed_pos=[]
    for x in range(0,9):
        all_points[x]={}
        for y in range(0,9):
            all_points[x][y]=Point(x,y,input_matrix[x,y])
            if input_matrix[x,y]==0:
                unfixed_pos.append([x,y])
    return all_points,unfixed_pos

def initPossibilities(point,all_points,unfixed_pos):
    if point.value!=0 and len(point.possibilites)>1:
        point.possibilites=[]
        return True
    if len(point.possibilites)==1:
        point.value=point.possibilites[0]
        point.possibilites=[]
        unfixed_pos.remove([point.x,point.y])
        print('fixed-> [%d,%d]: %d'%(point.x,point.y,point.value))
        return True
    impossible_values=[]
    for i in range(0,9):
        impossible_values.append(all_points[point.x][i].value)
        impossible_values.append(all_points[i][point.y].value)
    for i in range(point.sub_group_x*3,point.sub_group_x*3+3):
        for j in range(point.sub_group_y*3,point.sub_group_y*3+3):
            impossible_values.append(all_points[i][j].value)
    impossible_values=list(set(impossible_values))
    point.possibilites=[v for v in point.possibilites if v not in impossible_values]
    return False

def checkValid(value,point,all_points):
    for i in range(0,9):
        if all_points[point.x][i].value==value and [point.x,i] !=[point.x,point.y]:
            return False
        if all_points[i][point.y].value==value and [i,point.y] !=[point.x,point.y]:
            return False
    for i in range(point.sub_group_x*3,point.sub_group_x*3+3):
        for j in range(point.sub_group_y*3,point.sub_group_y*3+3):
            if all_points[i][j].value ==value and [i,j]!=[point.x,point.y]:
                return False
    return True

def findNextFill(all_points,current_pos):
    for x in range(0,9):
        for y in range(0,9):
                if all_points[x][y].value == 0:
                        return x,y
    return -1,-1

def checkComplete(all_points):
    for x in range(0,9):
        for y in range(0,9):
            if all_points[x][y].value==0:
                return False
    return True

def search(all_points,current_pos=[0,0]):
    x,y = findNextFill(all_points, current_pos)
    if x==-1:
        return True
    point=all_points[x][y]
    for value in point.possibilites:
        if checkValid(value,point,all_points):
            point.setValue(value)
            if search(all_points,[x,y]):
                return True
            point.setValue(0)
    return False

def showSudoku(all_points):
    for x in range(0,9):
        print(','.join([ str(p.value) for p in all_points[x].values()]))

if __name__=='__main__':
    input_matrix=readInput(sys.argv[1])
    all_points,unfixed_pos=initAllPoints(input_matrix)
    modified=1
    while(modified>0):
        modified-=1
        for x in all_points.keys():
            for y in all_points[x].keys():
                point=all_points[x][y]
                if initPossibilities(point,all_points,unfixed_pos) and modified==0:
                    modified+=1
    if checkComplete(all_points):
        showSudoku(all_points)
    else:
        if search(all_points):
            showSudoku(all_points)
            # print(point.x,point.y,point.possibilites)
