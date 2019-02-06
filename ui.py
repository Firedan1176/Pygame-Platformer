import pygame

scene_uiElements = []
"""Class used to define UI elements on screen"""
class Panel:
    def __init__(self, rect, parent = None, color = (64, 64, 64)):
        self.rect = rect
        self.parent = parent
        self._surface = pygame.Surface((rect.w, rect.h))
        self.color = color
        self._surface.fill(color)

        global uiElements
        scene_uiElements.append(self)

class Text(Panel):     
    def __init__(self, pos = (0, 0), text = "", textColor = (255, 255, 255)):
        super().__init__(pygame.Rect(pos[0], pos[1], 1, 1), color = textColor)
        self.text = text
        self.color = textColor
        self._font = pygame.font.SysFont("Courier", 12)
        self.setText(text)
        
    """Set/change the text"""
    def setText(self, text):
        self.text = text
        self._surface = self._font.render(text, False, self.color)

    
def render(display):
    for element in scene_uiElements:
        display.blit(element._surface, element.rect)
