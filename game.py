import pygame
import inputcontrol
import loading
from graphics import Camera
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

        import random            

        self.obj = GameObject(0)
        self.obj.position = Vector2(0, 0)
        self.obj.scale = Vector2(32, 32)
        self.obj.buildSprite("tiles_spritesheet_256.png")
        self.obj.sprite.partition("Test", pygame.Rect(0, 0, 256, 256), (32, 32))

camera = Camera(15)

a = testScene()

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

    #objects.solvePhysics()    
    camera.render(display)
    a.obj.position += Vector2(1, 0)
    pygame.display.update()
    clock.tick(30)
