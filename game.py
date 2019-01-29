import pygame
import inputcontrol
from pygame.math import Vector2
import sys
from pygame.locals import *
from objects import *
import objects

pygame.init()

display = pygame.display.set_mode((480, 360))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


class testScene:
    def move(self, args):
        self.player.velocity = args[0][0]

    def __init__(self):
        test_sprite_surf = pygame.image.load("test_spritesheet.png").convert_alpha()

        self.floor = Entity()
        self.floor.position = Vector2(0, 10)
        self.floor.scale = Vector2(480, 20)
        self.floor.spritesheet_surf = test_sprite_surf
        self.floor.addSprite(pygame.Rect(0, 0, self.floor.scale.x, self.floor.scale.y))
        
        self.player = Entity()
        self.player.static = False
        self.player.position = Vector2(50, 200)
        self.player.scale = Vector2(64, 64)
        self.player.spritesheet_surf = test_sprite_surf
        self.player.addSprite(pygame.Rect(64, 0, self.player.scale.x, self.player.scale.y))

        move_r_start = inputcontrol.createInput("move", K_RIGHT, KEYDOWN, self.move, Vector2(1, 0))
        move_r_stop = inputcontrol.createInput("move", K_RIGHT, KEYUP, self.move, Vector2(0, 0))

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
