import pygame
from sprites import Sprite
import json
from pygame.math import Vector2
import utils
import physics

scene_gameobjects = []

"""Inserts a GameObject into the scene."""
def insertObject(obj):
    if not Gameobject in obj.mbo():
        raise TypeError('The object passed must inherit GameObject')
    
    global scene_gameobjects
    #Get the index of the next highest value
    #Change 'x.z' to search by a different value other than the z depth
    i = utils.binarySearch([x.z for x in scene_gameobjects], obj.z, 0, len(scene_gameobjects) - 1)
    scene_gameobjects = scene_gameobjects[:i] + [obj] + scene_gameobjects[i:]

#Remove an object from the scene
#It may be wise to find a way to binary search and remove it
#Note that you may need to iterate over the matched index a few times as some game elements
#will have the same z value
"""Removes a GameObject from the scene."""
def removeObject(obj):
    global scene_gameobjects
    scene_gameobjects.remove(obj)
    del obj

"""
Base object for game, used for display, movement and position
"""
class GameObject():
    def __init__(self, z = 1, position = Vector2(0, 0), scale = Vector2(32, 32)):
        self.z = z
        self.position = position
        self.scale = scale
        self.rotation = 0
        self.visible = True

        insertObject(self)

    """Used to color the GameObject for testing"""
    def colorize(self, color):
        self.sprite = pygame.Surface(self.scale)
        self.sprite.fill(color)
    
        
    """Sets position and allows input of two integers, a tuple, or a vector2"""
    def setPosition(self, x, y = None):
        if type(x) == Vector2:
            self.position = x
        elif type(x) == tuple:
            self.postion = Vector2(x[0],x[1])
        elif type(x) == int and type(y) == int:
            self.position = Vector2(x,y)

    """The same as setPosition but adding position instead of setting it"""
    def move(self,dx,dy = None):
        if type(dx) == Vector2:
            self.position += dx
        elif type(dx) == tuple:
            self.position += Vector2(dx[0],dx[1])
        elif type(dx) == int and type(dy) == int:
            self.position += Vector2(dx,dy)

"""
Object which has physics interactions
"""
class Entity(GameObject):
    def __init__(self, z, static = True, collisions = True, velocity = Vector2(0, 0)):
        super().__init__(z)
        self.static = static
        self.collisions = collisions
        self.velocity = velocity
    
    def __init__(self, z):
        super().__init__(z)
        self.static = True
        self.collisions = True
        self.velocity = Vector2(0, 0)
        self.mass = 1
        self.restitution = 0.2 #debug test value

#Returns sublist of scene_gameobjects if it's the same classtype or one of its inherited are
    #i.e. Entity will return all entities and classes that inherit from Entity (i.e. Player, Enemy, etc.)
    #Note: Higher classes that inherit from a lower class will be returned.
    #i.e. Entity will return <type 'Player'>, not its child <type 'Entity'>
def getObjectsOfType(classType = GameObject):
    return [item for item in scene_gameobjects if classType in item.__class__.mro()]


#Initiates physics solving
def solvePhysics():
    physics.solve(getObjectsOfType(Entity))

