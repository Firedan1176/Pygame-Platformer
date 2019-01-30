import pygame
import inputcontrol
import loading
from pygame.math import Vector2
import sys
from pygame.locals import *
from objects import *
from player import Player
import objects

pygame.init()

display = pygame.display.set_mode((960, 540))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


class testScene:
    
    def __init__(self):
        
        self.a = Entity(1)
        self.a.static = False
        self.a.position = Vector2(300, 400)
        self.a.scale = Vector2(64, 64)
        self.a.mass = 1
        self.a.loadSprite("test_spritesheet.png", [(0, 0)])

        self.b = Entity(1)
        self.b.static = False
        self.b.position = Vector2(200, 100)
        self.b.velocity = Vector2(10, 25)
        self.b.scale = Vector2(32, 32)
        self.b.mass = 1
        self.b.loadSprite("test_spritesheet.png", [(32, 0)])

        self.bg = GameObject(0)
        self.bg.position = Vector2(960, 0)
        self.bg.scale = Vector2(960, 540)
        self.bg.loadSprite("dark_grey.png", [(0, 0)])

        for x in range(10):
            a = Entity(1)
            #self.floor.static = False
            a.position = Vector2(x * 65, 10)
            #a.velocity = Vector2(0, 50)
            a.scale = Vector2(64, 64)
            a.loadSprite("test_spritesheet.png", [(32, 32)])

testScene()

while True:
    for event in pygame.event.get():
        #Exit game
        if event.type == QUIT:
            print("Closing game...")
            pygame.quit()
            sys.exit(0)

        #Uber awesome event key processing
        elif event.type == KEYDOWN or event.type == KEYUP:
            inputcontrol.evaluate(event)

    objects.solvePhysics()
    objects.draw(display)

    pygame.display.update()
    clock.tick(30)
