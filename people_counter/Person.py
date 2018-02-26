from random import randint
import time

class Person:
    tracks = []
    def __init__(self, i, xi, yi):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0,255)
        self.G = randint(0,255)
        self.B = randint(0,255)
        self.done = False
        self.dir = None
    def getRGB(self):
        return (self.R,self.G,self.B)
    def getTracks(self):
        return self.tracks
    def getId(self):
        return self.i
    def getDir(self):
        return self.dir
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def updateCoords(self, xn, yn):
        self.tracks.append([self.x,self.y])
        self.x = xn
        self.y = yn
    def setDone(self):
        self.done = True
    def timedOut(self):
        return self.done
    def goingLeft(self,line_left):
        if len(self.tracks) >= 2:
            if self.tracks[-1][0] < line_left and self.tracks[-2][0] >= line_left: #cross the line_up
                self.dir = 'left'
                return True
        return False

    def goingRight(self,line_right):
        if len(self.tracks) >= 2:
            if self.tracks[-1][0] > line_right and self.tracks[-2][0] <= line_right: #cross the line_down
                self.dir = 'right'
                return True
        return False

#
# class MultiPerson:
#     def __init__(self, persons, xi, yi):
#         self.persons = persons
#         self.x = xi
#         self.y = yi
#         self.tracks = []
#         self.R = randint(0,255)
#         self.G = randint(0,255)
#         self.B = randint(0,255)
#         self.done = False
