import objects
import json

def load(filename):
    objects.scene_gameobjects.clear()
    inputcontrol.inputScheme.clear()

    try:
        file = open(filename + ".map", 'r')
    except:
        return False

    #Regex?
    
    return True

def save():
    for obj in objects.scene_gameobjects:
        print(obj.__dict__)
        print (json.dumps(obj.__dict__))
