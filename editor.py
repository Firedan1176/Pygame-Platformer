import pygame
import objects
import inputcontrol
import loading
from graphics import Camera
from pygame.math import Vector2
import sys
from pygame.locals import *




if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((960, 540))
    pygame.display.set_caption("Pygame Level Editor")

    clock = pygame.time.Clock()

    camera = Camera(15)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                import ctypes
                if ctypes.windll.user32.MessageBoxW(0, "Any unsaved progress will be lost!", "Are you sure?", 1) == 1:
                    print("Editor exit")
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEMOTION:
                pygame.display.update()


        clock.tick(30)
