import pygame
import inputcontrol
from pygame.math import Vector2
import sys
from pygame.locals import *
from objects import *
import objects

pygame.init()

display = pygame.display.set_mode((950, 540))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


class testScene:
    
    def __init__(self):
        test_sprite_surf = pygame.image.load("test_spritesheet.png").convert_alpha()

        
        self.a = Entity()
        self.a.static = False
        self.a.position = Vector2(300, 400)
        self.a.scale = Vector2(32, 32)
        self.a.spritesheet_surf = test_sprite_surf
        self.a.addSprite(pygame.Rect(0, 0, self.a.scale.x, self.a.scale.y))

        self.b = Entity()
        self.b.static = False
        self.b.position = Vector2(150, 0)
        self.b.velocity = Vector2(10, 25)
        self.b.scale = Vector2(32, 32)
        self.b.spritesheet_surf = test_sprite_surf
        self.b.addSprite(pygame.Rect(32, 0, self.b.scale.x, self.b.scale.y))

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
            self.b.evaluate(event)

    objects.solvePhysics()
    objects.draw(display)

    pygame.display.update()
    clock.tick(30)
