import objects
import re
import sys
import json
import ast
import player


#Classes to generate Objects from in the scene
CLASSES = {
        "GameObject":objects.GameObject,
        "Entity":objects.Entity,
        "Player":player.Player
    }
#Ignore these keywords in the json
IGNORE_TYPES = ["version"]

LOADING_VERSION = 1

def load(filename):
    objects.unloadScene()

    try:
        file = open(filename + ".map", 'r')
    except:
        raise IOError('Invalid scene name:', str(filename))
        return False

    #Get text and quickly close; in case of a hang/crash, the map file isn't being held at gunpoint
    file_text = file.read()
    file.close()
    
    obj = json.loads(file_text)
    if not "version" in obj:
        raise IOError("The file '" + filename + "' cannot be loaded because it doesn't have a version number")
    if obj["version"] != LOADING_VERSION:
        raise IOError("The file '" + filename + "' cannot be loaded because it's using a different version (" + str(obj["version"]) + ", requiring " + str(LOADING_VERSION) + ")")

    for scene_object in obj.items():
        pass
        if scene_object[0] in IGNORE_TYPES: continue
        elif scene_object[0] in CLASSES:
            _classType = CLASSES[scene_object[0]]

            _obj = _classType()
            
            for _attrib in scene_object[1].items():
                setattr(_obj, _attrib[0], ast.literal_eval(_attrib[1]))

                #For debugging purposes! Remove and add sprite stuff here
                if _attrib[0] == "color":
                    _obj.colorize(_obj.color)
        else:
            print("Warning: Couldn't load type '" + scene_object[0] + "' (Not a valid type)")
    
    return True

def save():
    for obj in objects.getObjectsOfType():
        pass
