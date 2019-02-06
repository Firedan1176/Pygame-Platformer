import objects
import json

def load(filename):
    objects.unloadScene()

    try:
        file = open(filename + ".map", 'r')
    except:
        raise IOError('Invalid scene name:', str(filename))
        return False

    
    
    return True

def save():
    for obj in objects.scene_gameobjects:
        print(json.dumps(obj))
