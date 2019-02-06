import pygame
import inputcontrol
import loading
from graphics import Camera
from pygame.math import Vector2
import math
import time
import sys
import ui
from pygame.locals import *
from objects import *
from player import Player
import objects
import sprites

pygame.init()

SCREENWIDTH = 480
SCREENHEIGHT = 270
SCALEFACTOR = 2

gameScreen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
display = pygame.display.set_mode((SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


sprite_list = sprites.SpriteList()
sprite_list.loadFile('spritesheet.png', (32, 32))
sprite_list.setAnimation([0], "Brick")

class testScene:    

    def pauseGame(self, x):
        print("Pause game")
        
    def __init__(self):
        self.background = GameObject(0, position = Vector2(0, 0), scale = Vector2(480, 270))
        self.background.colorize((20, 20, 20))

        self.floor = Entity(10)
        self.floor.position = Vector2(-2500, 20)
        self.floor.scale = Vector2(5000, 20)
        self.floor.colorize((100, 100, 100))

        self.phys1 = Entity(10)
        self.phys1.position = Vector2(100, 110)
        self.phys1.scale = Vector2(20, 350)
        self.phys1.colorize((255, 255, 255))

        self.phys2 = Entity(10)
        self.phys2.position = Vector2(180, 110)
        self.phys2.scale = Vector2(20, 500)
        self.phys2.colorize((255, 255, 255))

        self.phys3 = Entity(10)
        self.phys3.position = Vector2(20, 450)
        self.phys3.scale = Vector2(100, 20)
        self.phys3.colorize((255, 255, 255))

        self.phys4 = Entity(10)
        self.phys4.position = Vector2(500, 40)
        self.phys4.scale = Vector2(100, 50)
        self.phys4.colorize((255, 255, 255))

        self.phys5 = Entity(10)
        self.phys5.position = Vector2(600, 70)
        self.phys5.scale = Vector2(50, 50)
        self.phys5.colorize((255, 255, 255))

        self.spriteTest = GameObject(10)
        self.spriteTest.position = Vector2(200, 110)
        self.spriteTest.scale = Vector2(32, 32)
        
        global sprite_list
        #self.spriteTest.anim = sprites.AnimationHandler("", sprite_list)
        #self.spriteTest.sprite = self.spriteTest.anim.pull("Brick")
        self.spriteTest.sprite = sprite_list.pullSprite(0)

        for x in range(15):
            b = GameObject(4, position = Vector2(-100 + x * 50, -150), scale = Vector2(2, 750))
            b.colorize((50, 50, 50))
        for x in range(30):
            b = GameObject(4, position = Vector2(-150, x * 50), scale = Vector2(900, 2))
            b.colorize((50, 50, 50))

        self.player = Player(10)
        self.player.position = Vector2(200, 100)
        self.player.scale = Vector2(16, 24)
        self.player.colorize((200, 200, 200))

        self.text = ui.Text(text = "HELLO WORLD")

        #Initialize inputs
        inputcontrol.createInput("Pause", K_ESCAPE, KEYDOWN, self.pauseGame)


a = testScene()
camera = Camera(15)
camera.setTarget(a.player)


while True:
    
    inputcontrol.evaluate(pygame.event.get())
    physics.solve(objects.getObjectsOfType(Entity))
    camera.render(gameScreen)
    ui.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(60)
