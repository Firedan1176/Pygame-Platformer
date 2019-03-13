import objects
import pygame
from pygame.locals import *
from pygame.math import Vector2
import inputcontrol
import sprite2

def getPlayer():
    player = objects.getObjectsOfType(Player)
    return player[0] if len(player) != 0 else None

class Player(objects.Entity):

    speed = 3
    frozen = False
    jumpSpeed = 6
    inertia = 0.1   #Higher value stops player movement faster
    jump_off_wall = True
    wallFriction = 0.6 #0-1. Higher value causes less friction

    def __init__(self, z = 10):
        super().__init__(z)
        self.static = False
        self.jumped = False
        self.wall_hug = False
        self.dir = 1
        self.currentInteraction = None

        #0 = Idle
        #1 = Started moving
        #2 = Stopped moving
        #3 = Moving
        self.state = 0
        
        inputcontrol.createAxis("Move Horizontal", K_RIGHT, K_LEFT, self.move) 
        inputcontrol.createInput("Attack", 1, KEYDOWN, self.attack)
        inputcontrol.createInput("Jump", K_SPACE, KEYDOWN, self.jump)
        inputcontrol.createInput("Interact", K_e, KEYDOWN, self.interact)
        self.collisionCallbacks.append(self.checkJump)
        
    """Applies velocity to the player from raw input"""
    def move(self, val):
        #Set the 'state' of the player's movement
        if val == 0:
            if self.state == 1 or self.state == 3: self.state = 2
            else: self.state = 0
        else:
            if self.state == 0 or self.state == 2: self.state = 1
            else: self.state = 3
            
        if self.frozen:
            #Move to a stop
            self.velocity = Vector2.lerp(self.velocity, Vector2(0, 0), self.inertia)
        else:
            if val != 0:
                self.dir = val
            #Regular movement
            self.velocity = Vector2.lerp(self.velocity, Vector2(val * self.speed, self.velocity.y), self.inertia)

    def jump(self, val):
        if self.wall_hug:
            self.velocity += Vector2(-self.wall_hug, abs(self.wall_hug)) * self.jumpSpeed
            self.wall_hug = None
            
        if self.jumped: return
        self.jumped = True
        self.velocity = Vector2(self.velocity.x, self.jumpSpeed)

    def checkJump(self, collisions):
        for pair in collisions:
            if pair[0].collisions:
                #Reset jumped if landed on a flat surface
                if pair[1][1] == -1:
                    self.jumped = False
                #Hugging a wall right now
                if pair[1][0] != 0:
                    self.wall_hug = pair[1][0]
                    self.velocity.y *= self.wallFriction
                else: self.wall_hug = None

    def attack(self, x):
        print("Attack!")

    def interact(self, val):
        for pair in self.collisionData:
            if not pair[0].collisions:
                pair[0].interact(self)
                return #Remove this line to have multi-entity interactions
        #Didn't return, not interacting with anything
        if self.currentInteraction:
            self.currentInteraction.interact(self)

    def render(self, display, position):
        _sprite = self.updateSprite()
        if self.dir == -1:
            _sprite = pygame.transform.flip(_sprite, True, False)
        display.blit(_sprite, position)
