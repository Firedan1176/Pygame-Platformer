from pygame.math import Vector2
import physics

scene_gameobjects = []

class GameObject:
    spritesheet_surf = None
    spritesheet = []
    sprite_index = 0
    
    def __init__(self, position = Vector2(0, 0), scale = Vector2(1, 1), rotation = 0):
        scene_gameobjects.append(self)
        #self.id = len(scene_gameobjects) #Do something different than this        
        self.position = position
        self.scale = scale
        self.rotation = rotation


    def addSprite(self, rectangle):
        self.spritesheet.append(rectangle)

class Entity(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        self.static = True
        self.collisions = True
        self.velocity = Vector2(0, 0)
        self.mass = 1
        self.restitution = 0.2 #debug test value

#Returns sublist of scene_gameobjects where each item is the same class as classType or its base class(es)
def getObjectsOfType(classType = GameObject):
    return [item for item in scene_gameobjects if item.__class__ == classType or classType in item.__class__.__bases__]

def destroy(go):
    scene_gameobjects.remove(go)
    del go

#Initiates physics solving
def solvePhysics():
    physics.solve(getObjectsOfType(Entity))

#Draws objects.
def draw(display):
    for obj in getObjectsOfType(GameObject):
        if obj.spritesheet_surf and obj.spritesheet and len(obj.spritesheet) > 0:
            display.blit(obj.spritesheet_surf, (obj.position[0], display.get_height() - obj.position[1] - obj.spritesheet[obj.sprite_index].height), obj.spritesheet[obj.sprite_index])
