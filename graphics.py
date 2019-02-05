import pygame
import objects
from player import Player
from pygame.math import Vector2
from objects import GameObject

class Camera(GameObject):

    def __init__(self, z):
        super().__init__(z)
        self.parallax = 0.5

    def render(self, display):
        for obj in objects.getObjectsOfType(GameObject):
            #Excluded GameObjects
            if obj.__class__ in [Camera]: continue
            if obj.visible and obj.sprite and obj.z < self.z:
                #Reorient the position
                new_pos = Vector2(obj.position.x, display.get_height() - obj.position.y - obj.scale.y)

                #Offset based on parallax

                new_pos -= self.position * (obj.z * self.parallax)


                display.blit(obj.sprite, new_pos)
