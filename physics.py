from pygame.math import Vector2

#Returns if an intersection occurs between two Entities
def intersect(a, b):
    if (a.position.x + a.scale.x < b.position.x or a.position.x > b.position.x + b.scale.x):
        return False
    if (a.position.y + a.scale.y < b.position.y or a.position.y > b.position.y + b.scale.y):
        return False
    return True



#a and b are intersecting, resolve and apply velocities
def resolveCollision(a, b):
    rv = b.velocity - a.velocity
    normal = Vector2((b.position.x - a.position.x), -(b.position.y - a.position.y))
    velAlongNormal = Vector2.dot(rv, normal)

    if velAlongNormal > 0:
        print("velAlongNormal > 0")
        return

    e = min(a.restitution, b.restitution)
    j = -(1 + e) * velAlongNormal
    j /= a.mass + 1 / b.mass

    impulse = j * normal

    print(rv, normal, velAlongNormal, e, j, impulse)
    
    a.velocity -= 1 / a.mass * impulse
    b.velocity += 1 / b.mass * impulse
    

gravity = Vector2(0, -1)

def solve(objs):
    for obja in objs:
        for objb in objs:
            if obja != objb and obja.collisions and objb.collisions and intersect(obja, objb):
                resolveCollision(obja, objb)
        
        if not obja.static:
            obja.velocity += gravity
            obja.position += obja.velocity
