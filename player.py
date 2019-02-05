import objects
from pygame.locals import *
from pygame.math import Vector2
import inputcontrol

class Player(objects.Entity):

    speed = 5
    jumpSpeed = 10
    inertia = 0.1   #Higher value stops player movement faster
    
    """Applies velocity to the player from raw input"""
    def move(self, val):
        self.velocity = Vector2.lerp(self.velocity, Vector2(val * self.speed, self.velocity.y), self.inertia)

    def jump(self, val):
        if self.jumped: return
        self.jumped = True
        self.velocity = Vector2(self.velocity.x, self.jumpSpeed)

    def checkJump(self, val):
        #Reset jumped if landed on a flat surface
        if val.y == -1:
            self.jumped = False

    def attack(self, x):
        print("Attack!")

        
    def __init__(self, z):
        super().__init__(z)
        self.static = False
        self.jumped = False
        inputcontrol.createAxis("Move Horizontal", K_RIGHT, K_LEFT, self.move) 
        inputcontrol.createInput("Attack", 1, KEYDOWN, self.attack)
        inputcontrol.createInput("Jump", K_SPACE, KEYDOWN, self.jump)
        self.collisionCallbacks.append(self.checkJump)
