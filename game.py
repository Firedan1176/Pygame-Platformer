import pygame
import inputcontrol
import loading
from graphics import Camera
from pygame.math import Vector2
import math
import time
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

    def pauseGame(self, x):
        print("Pause game")
        
    def __init__(self):
        self.background = GameObject(0, position = Vector2(0, 0), scale = Vector2(480, 270))
        self.background.colorize((150, 210, 255))

        self.sun = GameObject(1, position = Vector2(220, 150), scale = Vector2(40, 40))
        self.sun.colorize((255, 255, 0))

        self.cloud = GameObject(2, position = Vector2(250, 155), scale = Vector2(100, 30))
        self.cloud.colorize((255, 255, 255))

        self.floor = Entity(10)
        self.floor.position = Vector2(40, 20)
        self.floor.scale = Vector2(400, 20)
        self.floor.colorize((20, 100, 30))

        self.phys = Entity(10)
        self.phys.position = Vector2(100, 100)
        self.phys.scale = Vector2(50, 20)
        self.phys.colorize((100, 100, 0))
        for x in range(30):
            b = GameObject(4, position = Vector2(x * 100, 0), scale = Vector2(95, 80))
            b.colorize((50, 50, 50))

        self.player = Player(10)
        self.player.position = Vector2(200, 100)
        self.player.scale = Vector2(16, 24)
        self.player.colorize((0, 0, 0))

        #Initialize inputs
        inputcontrol.createInput("Pause", K_ESCAPE, KEYDOWN, self.pauseGame)


a = testScene()
camera = Camera(15)
camera.setTarget(a.player)


while True:
    
    inputcontrol.evaluate(pygame.event.get())
    physics.solve(objects.getObjectsOfType(Entity))
    camera.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (960, 540))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(60)
