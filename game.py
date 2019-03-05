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
from local import *
from objects import *
import player
import objects
import sprite2

if not __name__ == "__main__":
    sys.exit(0)

pygame.init()

gameScreen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
display = pygame.display.set_mode((SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


#####Debug stuff here

scene = loading.load("test_map02")



#####
camera = Camera(15)
camera.setTarget(player.getPlayer())

while True:
    inputcontrol.evaluate(pygame.event.get())
    physics.solve(objects.getObjectsOfType(Entity))
    camera.render(gameScreen)
    ui.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(60)
    
