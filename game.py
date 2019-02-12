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
import player
import objects

pygame.init()

SCREENWIDTH = 480
SCREENHEIGHT = 270
SCALEFACTOR = 2

gameScreen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
display = pygame.display.set_mode((SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()

scene = loading.load("test_map")

camera = Camera(15)
camera.setTarget(player.getPlayer())

x = 0
for obj in objects.getObjectsOfType():
    t = ui.Text(text = str(type(obj)) + " " + str(obj.z) + " " + str(obj.position) + " " + str(obj.color))
    t.setPosition((0, x))
    x += 12

while True:
    inputcontrol.evaluate(pygame.event.get())
    physics.solve(objects.getObjectsOfType(Entity))
    camera.render(gameScreen)
    ui.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(60)
