import pygame
from pygame.math import Vector2
import utils
import physics

scene_gameobjects = []

scene_sprites = {}

#Insert an object deriving from GameObject into the scene
def insertObject(obj):
    global scene_gameobjects
    #Get the index of the next highest value
    #Change 'x.z' to search by a different value other than the z depth
    i = utils.binarySearch([x.z for x in scene_gameobjects], obj.z, 0, len(scene_gameobjects) - 1)
    scene_gameobjects = scene_gameobjects[:i] + [obj] + scene_gameobjects[i:]

#Remove an object from the scene
#It may be wise to find a way to binary search and remove it
#Note that you may need to iterate over the matched index a few times as some game elements
#will have the same z value
def removeObject(obj):
    global scene_gameobjects
    scene_gameobjects.remove(obj)
    del obj

class GameObject:

    def __init__(self, z):
        self.z = z
        self.position = Vector2(0, 0)
        self.scale = Vector2(32, 32)
        self.rotation = 0
        self.sprite_index = 0 #default to the first sprite
        self.sprites = []

        global scene_gameobjects
        insertObject(self)

    def loadSprite(self, filename, coords):
        global scene_sprites
        if filename not in scene_sprites:
            scene_sprites[filename] = pygame.image.load(filename).convert_alpha()
        self.sprite_source = scene_sprites[filename]
        for x in coords:
            self.sprites.append(pygame.Rect(x[0], x[1], self.scale.x, self.scale.y))


#This sets position and allows input of two integers, a tuple, or a vector2
    def setPosition(self, x, y = None):
        if type(x) == Vector2:
            self.position = x
        elif type(x) == tuple:
            self.postion = Vector2(x[0],x[1])
        elif type(x) == int and type(y) == int:
            self.position = Vector2(x,y)

#This is the same as setPosition but adding position instead of setting it
    def move(self,dx,dy = None):
        if type(dx) == Vector2:
            self.position += dx
        elif type(dx) == tuple:
            self.position += Vector2(dx[0],dx[1])
        elif type(dx) == int and type(dy) == int:
            self.position += Vector2(dx,dy)

"""
Object for anything moving/organic in the game
"""
class Entity(GameObject):
    def __init__(self, z):
        super().__init__(z)
        #GameObject.__init__(self)
        self.static = True
        self.collisions = True
        self.velocity = Vector2(0, 0)
        self.mass = 1
        self.restitution = 0.2 #debug test value


#Returns sublist of scene_gameobjects where each item is the same class as classType or its base class(es)
def getObjectsOfType(classType = GameObject):
    return [item for item in scene_gameobjects if item.__class__ == classType or classType in item.__class__.__bases__]


#Initiates physics solving
def solvePhysics():
    physics.solve(getObjectsOfType(Entity))

#Draws objects.
def draw(display):
    for obj in getObjectsOfType(GameObject):
        if obj.sprites and len(obj.sprites) > 0:
            display.blit(obj.sprite_source, (obj.position[0] - obj.sprites[obj.sprite_index].width, display.get_height() - obj.position[1] - obj.sprites[obj.sprite_index].height), obj.sprites[obj.sprite_index])
