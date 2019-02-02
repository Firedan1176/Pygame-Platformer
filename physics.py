from pygame.math import Vector2
import math

#Returns if an intersection occurs between two Entities
def intersect(a, b):
    if (a.position.x + a.scale.x < b.position.x or a.position.x > b.position.x + b.scale.x):
        return False
    if (a.position.y + a.scale.y < b.position.y or a.position.y > b.position.y + b.scale.y):
        return False
    return True

#Returns the normal of b if an intersection occurs; else, None
def intersectNormal(a, b):
    amin = a.position
    bmin = b.position
    amax = a.position + a.scale
    bmax = b.position + b.scale
    amid = a.position + (a.scale / 2)
    bmid = b.position + (b.scale / 2)

    if not intersect(a, b): return None

    normal = Vector2(0, 0)
    
    if (amax.x > bmin.x and amid.x < bmid.x):
        normal.x = -1
    elif (amin.x < bmax.x and amid.x > bmid.x):
        normal.x = 1
        
    if (amin.y < bmax.y and amid.y > bmid.y):
        normal.y = 1
    elif (amax.y > bmin.y and amid.y < bmid.y):
        normal.y = -1

    if (abs(amax.x - bmin.x) > abs(amax.y - bmin.y)):
        normal.x = 0
    else: normal.y = 0
        
    return normal
    
    
def resolveCollision4(a, b):
    norm = intersectNormal(a, b)
    if norm.x != 0:
        a.velocity.y *= -1
        b.velocity.y *= -1
    else:
        a.velocity.x *= -1
        b.velocity.x *= -1

def resolveCollision3(a, b):
    normal = intersectNormal(a, b)
    if normal == None:
        print("Error: overlapping objects detected:", a, "and", b)
        return
    if normal.y == 0:
        a.velocity.x *= -1
        b.velocity.x *= -1
        a.position += a.velocity
    else:
        a.velocity.y *= -1
        b.velocity.y *= -1
        a.position += a.velocity
        

def resolveCollision2(a, b):
    rv = b.velocity - a.velocity
    normal = Vector2(-(b.position.x - a.position.x), (b.position.y - a.position.y))

    velAlongNormal = Vector2.dot(rv, normal)
    if velAlongNormal > 0: return #No collision has occured, this should rarely happen

    a.velocity = (a.velocity * (a.mass - b.mass) + (2 * b.mass * b.velocity)) / (a.mass + b.mass)
    b.velocity = (b.velocity * (b.mass - a.mass) + (2 * a.mass * a.velocity)) / (a.mass + b.mass)
    if not a.static: a.position += a.velocity
    if not b.static: b.position += b.velocity

#a and b are intersecting, resolve and apply velocities
def resolveCollision(a, b):
    rv = b.velocity - a.velocity
    normal = Vector2((b.position.x - a.position.x), -(b.position.y - a.position.y))
    normal = normal.normalize()
    velAlongNormal = Vector2.dot(rv, normal)

    if velAlongNormal > 0: return

    e = min(a.restitution, b.restitution)
    j = -(1 + e) * velAlongNormal
    j /= a.mass + 1 / b.mass

    impulse = j * normal

    a.velocity -= 1 / a.mass * impulse
    b.velocity += 1 / b.mass * impulse

gravity = Vector2(0, 0)

def solve(objs):

    for obja in objs:
        if not obja.static:
            obja.velocity += gravity
        for objb in objs:
            if obja != objb and obja.collisions and objb.collisions and intersect(obja, objb):
                resolveCollision4(obja, objb)
                
        if not obja.static:
            obja.position += obja.velocity

