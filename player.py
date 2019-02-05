import objects
from pygame.locals import *
import inputcontrol

class Player(objects.Entity):
    def __init__(self, z):
        super().__init__(z)
        #inputcontrol.createInput("Move right+", K_RIGHT, KEYDOWN, lambda obj: print("HELLO"))
        #inputcontrol.createInput("Move right-", K_RIGHT, KEYUP, lambda obj: print("HELLO"))
