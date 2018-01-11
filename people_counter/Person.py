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
    def going_UP(self,line_up):
        if len(self.tracks) >= 2:
            if self.tracks[-1][1] < line_up and self.tracks[-2][1] >= line_up: #cross the line_up
                self.dir = 'up'
                return True
        return False

    def going_DOWN(self,line_down):
        if len(self.tracks) >= 2:
            if self.tracks[-1][1] > line_down and self.tracks[-2][1] <= line_down: #cross the line_down
                self.dir = 'down'
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
