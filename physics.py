from pygame.math import Vector2
import math
import utils

gravity = Vector2(0, -0.66)
terminal_velocity = 12

"""Checks for intersections on GameObjects a and b. Objects that are edge-to-edge/touching are not considered intersecting."""
def intersect(a, b):
    if (a.position.x + a.scale.x <= b.position.x or a.position.x >= b.position.x + b.scale.x):
        return False
    if (a.position.y + a.scale.y <= b.position.y or a.position.y >= b.position.y + b.scale.y):
        return False
    return True


"""Returns a list of objects collided with obj in all objs"""
def getCollisions(obj, objs):
    colliders = []
    for col in objs:
        if not obj == col and intersect(obj, col):
            colliders.append(col)
    return colliders

"""Solves physics for all non-static objects"""
def solve(phys_objs):
    for obj in [nonstatic for nonstatic in phys_objs if not nonstatic.static]:
        obj.velocity += gravity
        obj.velocity.y = utils.clamp(-terminal_velocity, terminal_velocity, obj.velocity.y)
        obj.position.x += obj.velocity.x
        collisionData = []
        for col in getCollisions(obj, phys_objs):
            data = (col, Vector2(0, 0))
            collisionData.append(data)
            #Moving right? obj's right side = collider's left side
            if obj.velocity.x > 0:
                if col.collisions:
                    obj.velocity.x = 0
                    obj.position.x = col.position.x - obj.scale.x
                data[1].x = 1
            elif obj.velocity.x < 0:
                if col.collisions:
                    obj.velocity.x = 0
                    obj.position.x = col.position.x + col.scale.x
                data[1].x = -1
        obj.position.y += obj.velocity.y

        for col in getCollisions(obj, phys_objs):         
            data = None
            for x in collisionData:
                if col == x[0]:
                    data = x
                    break
            if not data:
                data = (col, Vector2(0, 0))
                collisionData.append(data)
                
            if obj.velocity.y > 0:
                if col.collisions:
                    obj.velocity.y = 0
                    obj.position.y = col.position.y - obj.scale.y
                data[1].y = 1
            elif obj.velocity.y < 0:
                if col.collisions:
                    obj.velocity.y = 0
                    obj.position.y = col.position.y + col.scale.y
                data[1].y = -1

        obj.collisionData = collisionData
        #Call functions
        for callback in obj.collisionCallbacks:
            callback(collisionData)

