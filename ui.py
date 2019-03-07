import pygame
import sprite2
from local import *

_uiElements = []
"""Class used to define UI elements on screen"""
class Panel:
    def __init__(self, parent = None, rect = pygame.Rect(0, 0, 0, 0), color = (64, 64, 64)):
        self._rect = rect
        self._parent = parent
        self._children = []
        if self._parent:
            self._parent._children.append(self)
        self._surface = pygame.Surface((rect.w, rect.h))
        self._color = color
        self._surface.fill(color)

        
        self.visible = True

        global _uiElements
        _uiElements.append(self)

    def destroy(self):
        global _uiElements
        _uiElements.remove(self)

        if self._parent:
            self._parent._children.remove(self)

        del self

    def getParent(self):
        return self._parent

    def setParent(self, target):
        if not Panel in target._class_.mro():
            raise TypeError('Target parent must derive from Panel')
        self._parent = target

    def getChildren(self):
        return self._children

    def offsetPosition(self, position):
        self._rect = self._rect.move(position)

    def setPosition(self, position):
        self._rect.topleft = position

    def setRect(self, rect):
        self._rect = rect

    def getPosition(self):
        if self._parent:
            return tuple(self._parent._rect[x] + self._rect[x] for x in range(2))
        else:
            return self._rect.topleft

    def __repr__(self):
        return "Panel " + str(self._rect)
        
class Text(Panel):     
    def __init__(self, parent = None, pos = (0, 0), text = "", textColor = (255, 255, 255), size = 1):
        super().__init__(parent, pygame.Rect(pos[0], pos[1], 1, 1), color = textColor)
        self._color = textColor
        self._font = pygame.font.SysFont("Courier", 12)
        self._size = size
        self.setText(text)
        
    """Set/change the text"""
    def setText(self, text):
        self.text = text
        self._surface = self._font.render(text, False, self._color)
        if self._size != 1:
            self._surface = pygame.transform.scale(self._surface, (self._surface.get_width() * self._size, self._surface.get_height() * self._size))
            

    def setColor(self, color):
        self._color = color

    def setPosition(self, position):
        self._rect = pygame.Rect(position[0], position[1], self._rect.w, self._rect.h)

    def render(self, display):
        display.blit(self._surface, self.getPosition())

    def __repr__(self):
        return "\"" + self.text + "\""
        
class ModalWindow(Panel):

    GENERIC = "art/ui/modal_generic"
    
    
    def __init__(self, parent = None, pos = (0, 0), size = (96, 96), windowType = GENERIC):
        #TODO: Expand these, add more stickies
        if type(pos) == str:
            displaySize = (SCREENWIDTH, SCREENHEIGHT)
            if pos == "center":
                pos = ((displaySize[0] / 2) - (size[0] / 2), (displaySize[1] / 2) - (size[1] / 2))

        super().__init__(parent, pygame.Rect(pos, size))
        self._surface = sprite2.loadSprite(ModalWindow.GENERIC, mode = "9slice", scale = size)

    def render(self, display):
        display.blit(self._surface, self.getPosition())

    def scale(self, size):
        self._rect = self._rect.inflate(size)
        self._surface = sprite2.loadSprite(ModalWindow.GENERIC, mode = "9slice", scale = self._rect.size, exclude = True)

    def __repr__(self):
        return "ModalWindow " + str(self._rect)
    
def render(display):
    for element in _uiElements:
        if element._parent:
            if element._parent.visible and element.visible:
                element.render(display)
        elif element.visible: element.render(display)
