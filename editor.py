import pygame
import objects
import inputcontrol
import loading
import ui
from graphics import Camera
from pygame.math import Vector2
import sys
from pygame.locals import *

EDITOR_UI = []

class EDITOR_TEXT:
    def __init__(self, TEXT, POS = (0, 0), COLOR = (255, 255, 255), ACTION = None):
        self.POS = POS
        self.COLOR = COLOR
        self.SETTEXT(TEXT)
        self.ACTION = ACTION
        self.CLICKED = False

        global EDITOR_UI
        EDITOR_UI.append(self)

    def RENDER(self):
        global EDITOR_FONT
        self.SURF = EDITOR_FONT.render(self.TEXT, False, self.COLOR)
        self.RECT = pygame.Rect(self.POS[0], self.POS[1], self.SURF.get_width(), self.SURF.get_height())

    def SETTEXT(self, TEXT):
        self.TEXT = TEXT
        self.RENDER()

    def SETPOS(self, POS):
        self.RECT = pygame.Rect(POS[0], POS[1], self.RECT.x, self.RECT.y)

    def SETCOLOR(self, COLOR):
        self.COLOR = COLOR
        self.RENDER()

def SAVEDIALOG():
    pass

def LOADDIALOG():
    pass

HEADERS = {"SAVE":SAVEDIALOG, "LOAD":LOADDIALOG}

if __name__ == "__main__":
    
    SCREENWIDTH = 480
    SCREENHEIGHT = 270
    SCALEFACTOR = 2
    BORDERSIZE = 64

    pygame.init()
    viewport = pygame.Surface((SCREENWIDTH - BORDERSIZE, SCREENHEIGHT - BORDERSIZE))
    display = pygame.display.set_mode((SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    pygame.display.set_caption("Pygame Editor")

    editorBg = pygame.Surface((SCREENWIDTH * SCALEFACTOR, SCREENHEIGHT * SCALEFACTOR))
    editorBg.fill((50, 50, 50))

    EDITOR_FONT = pygame.font.SysFont("Courier", 24)

    index = 0
    for X in HEADERS.items():
        TXT = EDITOR_TEXT(X[0], POS = (X * 16 * len(X[0]), 0), ACTION = X[1])

    clock = pygame.time.Clock()
    camera = Camera(15)

    def moveCursor(pos):
        pass
    
    #Create inputs for the editor
    inputcontrol.createAxis("Move Horiztonal", K_RIGHT, K_LEFT, lambda x: camera.move(Vector2(x, 0)))
    inputcontrol.createAxis("Move Vertical", K_RIGHT, K_LEFT, lambda y: camera.move(Vector2(0, y)))
    inputcontrol.createInput("Move Cursor", 32, MOUSEMOTION, moveCursor)
        
    while True:
        events = pygame.event.get()
        inputcontrol.evaluate(events)
        ###Editor Buttons Click###
        MOUSEPOS = pygame.mouse.get_pos()
        MOUSECLICK = pygame.mouse.get_pressed()
        for BUTTON in [B for B in EDITOR_UI if B.__class__ == EDITOR_TEXT]:
            if BUTTON.RECT.x + BUTTON.RECT.w > MOUSEPOS[0] > BUTTON.RECT.x and BUTTON.RECT.y + BUTTON.RECT.h > MOUSEPOS[1] > BUTTON.RECT.y:
                if MOUSECLICK[0] == 1 and BUTTON.ACTION and not BUTTON.CLICKED:
                    BUTTON.CLICKED = True
                    BUTTON.ACTION()
                elif not MOUSECLICK[0] and BUTTON.CLICKED:
                    BUTTON.CLICKED = False

        ##########EDITOR WINDOW#################
        display.blit(editorBg, (0, 0))

        for UI in EDITOR_UI:
            display.blit(UI.SURF, UI.RECT)

        ##########VIEWPORT##################
        camera.render(viewport)
        ui.render(viewport)
        scaled_viewport = pygame.transform.scale(viewport, ((SCREENWIDTH - BORDERSIZE) * SCALEFACTOR, (SCREENHEIGHT - BORDERSIZE) * SCALEFACTOR))
        display.blit(scaled_viewport, (0, BORDERSIZE / 2))
        
        pygame.display.update()
        clock.tick(30)
