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
gameScreen = pygame.Surface((480, 270))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


class testScene:
    
    def __init__(self):
        background = GameObject(0, position = Vector2(0, 0), scale = Vector2(480, 270))
        background.colorize((150, 210, 255))

        sun = GameObject(1, position = Vector2(220, 150), scale = Vector2(40, 40))
        sun.colorize((255, 255, 0))

        cloud = GameObject(2, position = Vector2(250, 155), scale = Vector2(100, 30))
        cloud.colorize((255, 255, 255))

        for x in range(30):
            a = GameObject(10, position = Vector2(x * 30, 0), scale = Vector2(28, 20))
            a.colorize((20, 100, 30))

            b = GameObject(4, position = Vector2(x * 100, 0), scale = Vector2(95, 80))
            b.colorize((50, 50, 50))
        

camera = Camera(15)

def moveCamera(direction):
    camera.position += direction

inputcontrol.createAxis("Move Horizontal", K_RIGHT, K_LEFT, lambda x: moveCamera(Vector2(x, 0)))
inputcontrol.createAxis("Move Vertical", K_UP, K_DOWN, lambda x: moveCamera(Vector2(0, -x)))


a = testScene()

while True:
    inputcontrol.evaluate(pygame.event.get())

    objects.solvePhysics()    
    camera.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (960, 540))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(30)
