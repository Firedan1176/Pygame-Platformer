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

scene = loading.load("test_map03")

chest = objects.getObjectsOfType(Chest)[0]
chest._items = [Item("Potion"), Item("Potion"), Item("Book")]

animTile = GameObject(z = 10, position = Vector2(0, 50))
animTile.sprite = sprite2.loadSpriteAnimation("player_idle")
animTile.play("player_idle")

_player = objects.getObjectsOfType(player.Player)[0]
_player.sprite = sprite2.loadSpriteAnimation("eggy")
_player.play("eggy")

#####
camera = Camera(15)
camera.setTarget(player.getPlayer())

fps_delay = 60 #Show fps every second
fps_delta = 0

while True:
    inputcontrol.evaluate(pygame.event.get())
    physics.solve(objects.getObjectsOfType(Entity))
    camera.render(gameScreen)
    ui.render(gameScreen)
    scaled_display = pygame.transform.scale(gameScreen, (SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    display.blit(scaled_display, (0, 0))
    pygame.display.update()
    clock.tick(60)

    #Show FPS
    if fps_delta >= fps_delay and DEBUGGING:
        fps_delta = 0
        print("%0.2f" % clock.get_fps() + " FPS")

    fps_delta += 1
