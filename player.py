import objects
from objects import *
from pygame.locals import *
from pygame.math import Vector2
import inputcontrol

"""The Player that the user plays as"""
class Player(objects.Entity):

    speed = 5
    jumpSpeed = 10
    inertia = 0.1   #Higher value stops player movement faster
    jump_off_wall = True
    wallFriction = 0.6 #0-1. Higher value causes less friction
    
    """Applies a smooth velocity to the player from raw input"""
    def move(self, val):
        self.velocity = Vector2.lerp(self.velocity, Vector2(val * self.speed, self.velocity.y), self.inertia)

    def jump(self, val):
        if self.wall_hug:
            self.velocity += Vector2(-self.wall_hug, abs(self.wall_hug)) * self.jumpSpeed
            self.wall_hug = None
            
        if self.jumped: return
        self.jumped = True
        self.velocity = Vector2(self.velocity.x, self.jumpSpeed)

    def checkJump(self, val):
        #Reset jumped if landed on a flat surface
        if val.y == -1:
            self.jumped = False
        if val.x != 0:
            self.wall_hug = val.x
            self.velocity.y *= self.wallFriction
        else: self.wall_hug = None

    def attack(self, x):
        print("Attack!")

        
    def __init__(self, z):
        super().__init__(z)
        self.static = False
        self.jumped = False
        self.wall_hug = False
        inputcontrol.createAxis("Move Horizontal", K_RIGHT, K_LEFT, self.move) 
        #inputcontrol.createInput("Attack", 1, KEYDOWN, self.attack)
        inputcontrol.createInput("Jump", K_SPACE, KEYDOWN, self.jump)
        self.collisionCallbacks.append(self.checkJump)


"""All enemies and other CPU controlled players' root type"""
class NPC(Entity):
    
    speed = 3
    inertia = 0.2

    def update(self):
        if self.target:
            if self.target.__class__ == Vector2:
                _x = -1 if self.position.x - self.target.x > 0 else 1
                self.move(Vector2(_x, 0))
            else:
                _x = -1 if self.position.x - self.target.position.x > 0 else 1
                self.move(Vector2(_x, 0))
    
    def __init__(self, z):
        super().__init__(z)
        #Hook update function
        self.target = None
        global scene_update_funcs
        scene_update_funcs.append(self.update)

    """Set the current target of the NPC"""
    def setTarget(self, target):
        if not GameObject in target.__class__.mro() and not target.__class__ == Vector2:
            raise TypeError('NPC target must be a GameObject or Vector2 (' + str(target.__class__) + ')')
        self.target = target

    """Move the NPC in a direction. val should be a normal with magnitude of 1 on any axis"""
    def move(self, val):
        self.velocity = Vector2.lerp(self.velocity, Vector2(val * self.speed, self.velocity.y), self.inertia)
