import objects
from pygame.locals import *
from pygame.math import Vector2
import inputcontrol

class Player(objects.Entity):

    speed = 5
    jumpSpeed = 15
    
    """Applies velocity to the player"""
    def move(self, val):
        self.velocity = Vector2(val * self.speed, self.velocity.y)

    def jump(self, val):
        self.velocity = Vector2(self.velocity.x, self.jumpSpeed)
        
    def __init__(self, z):
        super().__init__(z)
        self.static = False
        inputcontrol.createAxis("Move Horizontal", K_RIGHT, K_LEFT, lambda x: self.move(x))
        #inputcontrol.createAxis("Move Vertical", K_UP, K_DOWN, lambda y: self.jump(y))
        inputcontrol.createInput("Jump", K_SPACE, KEYDOWN, lambda y: self.jump(y))
