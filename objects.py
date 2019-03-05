import pygame
from pygame.math import Vector2
import utils
import physics
import sprites
import ui

scene_gameobjects = []

"""
Base object for game, used for display, movement and position
"""
class GameObject():
    def __init__(self, z = 1, position = Vector2(0, 0), scale = Vector2(32, 32)):
        self.z = z
        self.position = position if type(position) == Vector2 else Vector2(position)
        self.scale = scale if type(scale) == Vector2 else Vector2(scale)
        self.rotation = 0
        self.visible = True
        self.sprite = None
        self.color = None

        insertObject(self)

    def __str__(self):
        return "GameObject " + str(self.position) 

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

    def getSprite(self):
        return self.sprite

"""
Object which has physics interactions
"""
class Entity(GameObject):
    def __init__(self, z = 1, position = Vector2(0, 0), scale = Vector2(32, 32), static = True, collisions = True, velocity = Vector2(0, 0)):
        super().__init__(z)
        self.static = static
        self.collisions = collisions #Disable for trigger events
        self.velocity = velocity
        self.collisionCallbacks = [] #Call these functions on collision

        def __str__(self):
            return "Entity " + str(self.position)

"""
An entity that holds objects for the player.
"""
class Chest(Entity):
    def __init__(self, z = 1, position = Vector2(0, 0), items = [], capacity = 32):
        super().__init__(z, position, Vector2(32, 2), True, False, Vector2(0, 0))
        self._items = items
        self.opened = False
        self.window = ui.ModalWindow(pos = "center", size = (96, 128))
        self.window.offsetPosition((-96, 0))
        self.window.visible = False

    def __str__(self):
        return "Chest " + str(self.position)

    """Add an item to the Chest. Returns True if successfully added."""
    def addItem(self, item):
        if len(self._items) == self.capacity:
            return False
        self._items += item
        return True

    """Removes an item from the Chest. Returns True if successfully removed."""
    def removeItem(self, item):
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def updateWindow(self):
        for item in self._items:
            pass
            #TODO: parent items to the ModalWindow as Text objects

    def interact(self, player):
        if not self.opened:
            player.frozen = True
            print("Open chest!")
            self.updateWindow()
            self.window.visible = True
            self.opened = True
        else:
            player.frozen = False
            print("Close chest!")
            self.window.visible = False
            self.opened = False

        
#Returns sublist of scene_gameobjects if it's the same classtype or one of its inherited are
    #i.e. Entity will return all entities and classes that inherit from Entity (i.e. Player, Enemy, etc.)
    #Note: Higher classes that inherit from a lower class will be returned.
    #i.e. Entity will return <type 'Player'>, not its child <type 'Entity'>
def getObjectsOfType(classType = GameObject):
    if classType == GameObject:
        return scene_gameobjects
    return [item for item in scene_gameobjects if classType in item.__class__.mro()]

"""Inserts a GameObject into the scene."""
def insertObject(obj):
    if not GameObject in obj.__class__.mro():
        raise TypeError('The object passed must inherit GameObject')
    
    global scene_gameobjects
    #Get the index of the next highest value
    #Change 'x.z' to search by a different value other than the z depth
    i = utils.binarySearch([x.z for x in scene_gameobjects], obj.z, 0, len(scene_gameobjects) - 1)
    scene_gameobjects = scene_gameobjects[:i] + [obj] + scene_gameobjects[i:]

"""Clears all objects from the scene."""
def unloadScene():
    scene_gameobjects.clear()
    

#Remove an object from the scene
#It may be wise to find a way to binary search and remove it
#Note that you may need to iterate over the matched index a few times as some game elements
#will have the same z value
"""Removes a GameObject from the scene."""
def removeObject(obj):
    global scene_gameobjects
    scene_gameobjects.remove(obj)
    del obj

"""Returns a formatted string in a JSON-readable format. Used in saving"""
def formattedPropertyString(obj):
    if not GameObject in obj.__class__.mro():
        raise TypeError("The object passed must inherit GameObject")

    _str = "\"" + obj.name + "\": {\n" + \
           "\t\"z\": \"" + str(obj.z) + "\",\n" + \
           "\t\"position\": \"" + str(obj.position) + "\",\n" + \
           "\t\"scale\": \"" + str(obj.scale) + "\"\n" + \
           "}"

    return _str
