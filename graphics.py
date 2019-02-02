import pygame
import objects
from pygame.math import Vector2
from objects import GameObject

class Camera(GameObject):

    def __init__(self, z):
        super().__init__(z)
        self.parallax = 0.25


        self.resolution = pygame.display.get_surface().get_size()
    
    def render(self, display):
        for obj in reversed(objects.getObjectsOfType(GameObject)):
            if obj.visible and obj.sprite and obj.z < self.z:
                #Reorient the position
                new_pos = Vector2(obj.position.x, self.resolution[1] - obj.position.y - obj.scale.y)

                #Offset based on parallax
                #new_pos *= (obj.z * self.parallax)
                
                display.blit(obj.sprite.get(), new_pos)
