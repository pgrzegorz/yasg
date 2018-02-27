#!/usr/bin/env python3

import pygame
import sys

class Snake(list):
    def __init__(self,screen,length=2,size=10):
        list.__init__(self)
        self.size=size
        self.length=length
        self.screen=screen
        for i in range(length):
            self.append(pygame.Rect(self.size,self.size,self.size,self.size))
    def move(self,x,y):
        self[:] = [self[0].move(x*self.size,y*self.size)] + self[:-1]
        print(x*self.size)
    def draw(self):
        for i in self:
            pygame.draw.rect(self.screen,(255,255,255 ),i,0)
            print(i)



res=(800,600)

pygame.init()
screen = pygame.display.set_mode(res)
s=Snake(screen,10,20)

x_direction=0
y_direction=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
    screen.fill((0,0,0))
    s.draw()
    pygame.display.flip()
    if s[0][0]>800 or s[0][0]<0 or s[0][1]>600 or s[0][1]<0:
        pygame.quit()
    pygame.display.flip()
    pygame.time.wait(100)
