#!/usr/bin/env python

import pygame
import random
import sys
import os

RESX=800
RESY=600
PANEL_HEIGHT=40
INFO_TEXT="SCORE: %s HIGH SCORE: %s"
TEXT_MARIGN=2
SLEEP=150
SCORE_FILE="~/.yasg"


class Snake(list):
    def __init__(self,screen,length=2,size=20,color=(255,255,255),width=0):
        list.__init__(self)
        self.collision=False
        self.size=size
        self.length=length
        self.screen=screen
        self.color=color
        self.width=width
        for i in range(length):
            self.append(pygame.Rect(self.screen.get_width()//2//self.size*self.size,
                        self.screen.get_height()//2//self.size*self.size,
                        self.size,self.size))
    def move(self,x,y):
        self[:] = [self[0].move(x*self.size,y*self.size)] + self[:-1]
    def draw(self):
        for i in self:
            pygame.draw.rect(self.screen,self.color,i,self.width)
    def grow(self):
        self.append(self[-1])
    def collide(self):
        self.collision=False
        if self[0].collidelist(self[1:]) > 0 :
            self.collision=True
        if s[0][0]>self.screen.get_width()-s.size or s[0][0]<0 or\
           s[0][1]>self.screen.get_height()-s.size or s[0][1]<0:
            self.collision=True
        return self.collision
    def get_head(self):
        return self[0]
            
class Apple():
    def __init__(self,screen,size=20,color=(255,0,0),width=0):
        self.x=size
        self.y=size
        self.screen=screen
        self.size=size
        self.color=color
        self.width=width
        self.rect=pygame.Rect(self.x,self.y,self.size,self.size)
        self.put()
    def put(self):
        self.x=random.randrange(0,self.screen.get_width(),self.size)
        self.y=random.randrange(0,self.screen.get_height(),self.size)
        self.rect[0]=self.x
        self.rect[1]=self.y
    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,self.width)


class HighScore():
    def __init__(self, filename=SCORE_FILE):
        self.filename=os.path.expanduser(filename)
        self.file_fd = open(self.filename, "a+")
        self.file_fd.seek(0)
        self.content=self.file_fd.readline()
    def get_high_score(self):
        return int(''.join(c for c in self.content if c.isdigit()) or 0)
    def set_high_score(self, score):
        if score > self.get_high_score():
            self.file_fd.seek(0)
            self.file_fd.truncate()
            self.file_fd.write(str(score))
    def close(self):
        self.file_fd.close()
      

if __name__=="__main__":
    res=(RESX,RESY)

    pygame.init()
    screen = pygame.display.set_mode(res)

    x_direction=0
    y_direction=0

    boardsize=(RESX,RESY-PANEL_HEIGHT)
    panelsize=(RESX,PANEL_HEIGHT)
    board=pygame.Surface(boardsize)
    panel=pygame.Surface(panelsize)
    s=Snake(board,2,20)
    a=Apple(board)
    h=HighScore()
    text=pygame.font.SysFont("monospace",PANEL_HEIGHT-TEXT_MARIGN*2, True)

    score=0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                h.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_direction=-1
                    x_direction=0
                if event.key == pygame.K_DOWN:
                    y_direction=1
                    x_direction=0
                if event.key == pygame.K_LEFT:
                    x_direction=-1
                    y_direction=0
                if event.key == pygame.K_RIGHT:
                    x_direction=1
                    y_direction=0

        s.move(x_direction,y_direction)
        board.fill((0,0,0))
        panel.fill((30,30,30))
        label=text.render(INFO_TEXT % (str(score),str(h.get_high_score())),1,(255,255,255))
        panel.blit(label,(TEXT_MARIGN,TEXT_MARIGN))
        s.draw()
        if a.rect.colliderect(s.get_head()):
           s.grow()
           a.put()
           score+=1
           h.set_high_score(score)
        a.draw()
        if s.collide():
            pygame.quit()
            sys.exit()
        screen.blit(board,(0,PANEL_HEIGHT))
        screen.blit(panel,(0,0))
        pygame.display.flip()
        pygame.time.wait(SLEEP)

