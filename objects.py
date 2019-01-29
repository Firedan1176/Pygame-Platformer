from pygame.math import Vector2
import physics

scene_objects = []

#TODO: This should be done from loading a scene?
scene_gameobjects = []
scene_entities = []
scene_objects.append(scene_gameobjects)
scene_objects.append(scene_entities)

class GameObject:
    spritesheet_surf = None
    spritesheet = []
    sprite_index = 0
    
    def __init__(self, position = Vector2(0, 0), scale = Vector2(1, 1), rotation = 0):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        if type(self) == GameObject: scene_gameobjects.append(self)

    def addSprite(self, rectangle):
        self.spritesheet.append(rectangle)

class Entity(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        global scene_entities
        scene_entities.append(self)
        
        self.static = True
        self.collisions = True
        self.velocity = Vector2(0, 0)
        self.mass = 1
        self.restitution = 0.2 #debug test value

def getAllObjects():
    return [item for sublist in scene_objects for item in sublist]

def destroy(go):
    scene_gameobjects.remove(go)

#Initiates physics solving
def solvePhysics():
    physics.solve(scene_entities)

#Draws objects.
def draw(display):
    for obj in getAllObjects():
        if obj.spritesheet_surf and obj.spritesheet and len(obj.spritesheet) > 0:
            display.blit(obj.spritesheet_surf, (obj.position[0], display.get_height() - obj.position[1] - obj.spritesheet[obj.sprite_index].height), obj.spritesheet[obj.sprite_index])
