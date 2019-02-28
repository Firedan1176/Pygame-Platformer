import pygame
import objects
from player import Player
from pygame.math import Vector2
from objects import GameObject
import utils

class Camera(GameObject):

    
    def __init__(self, z = 15):
        super().__init__(z)
        self.target = None #Call setTarget to set a target for the camera to follow
        self.targetSpeed = 0.2

    #TODO: Add chunking of objects for complex scenes
    def render(self, display):
        if self.target:
            screen_center = Vector2(display.get_size()) / 2

            #Smooth camera movement
            #TODO: Add borders for edges of map???
            goal = (self.target.position - screen_center) / (self.target.z)
            self.position = Vector2.lerp(self.position, goal, self.targetSpeed)


        for obj in objects.getObjectsOfType(GameObject):
            #Excluded GameObjects
            if obj.__class__ in [Camera]: continue
            if obj.visible and obj.tex and obj.z < self.z:
                #Reorient the position
                new_pos = Vector2(obj.position.x, display.get_height() - obj.position.y - obj.scale.y)

                #Offset based on camera position and parallax
                new_pos -= Vector2(self.position.x, -self.position.y) * obj.z


                display.blit(obj.tex, new_pos)
                
    """Set the target of the camera to follow a GameObject"""
    def setTarget(self, obj):
        if GameObject in obj.__class__.mro():
            self.target = obj

