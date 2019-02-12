import objects
import re
import sys
import json
import ast
import player

from pygame.math import Vector2


#Classes to generate Objects from in the scene
CLASSES = {
        "GameObject":objects.GameObject,
        "Entity":objects.Entity,
        "Player":player.Player
    }
#Ignore these keywords in the json
IGNORE_TYPES = ["version"]

IGNORE_VALUES = ["class"]

#Pairs of values and their corresponding complex class.
#Example from a file:
#>"position":(32, 32)
#Literally evaluated as a tuple, but since 'position' is in the table
#below as a Vector2, the tuple will be converted to a Vector2.
#Optionally, use a lambda expression instead of the init() of the class
TYPE_TABLE = {
        "position":Vector2,
        "scale":Vector2
    }

LOADING_VERSION = 1
DEBUGGING = False

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

    #Returns value [1] for each item in the json that is a dict
    for scene_object in [x for x in obj.items() if type(x[1]) == dict]:
        _name = scene_object[0]
        _objSource = scene_object[1]
        _class = _objSource["class"]
        
        if _class in IGNORE_TYPES: continue
        elif _class in CLASSES:
            _classType = CLASSES[_class]

            if DEBUGGING: print("Loading", _classType, "...")
            
            _obj = _classType()
            _obj.name = _name
            
            for _attrib in _objSource.items():
                if _attrib[0] in IGNORE_VALUES: continue

                _val = ast.literal_eval(_attrib[1])

                #If there's a format that's paired up (ie. tuple and Vector2), convert it from the table (dictionary)
                if _attrib[0] in TYPE_TABLE:
                    _val = TYPE_TABLE[_attrib[0]](_val)
                    if DEBUGGING: print("\tValue '" + _attrib[0] + "' converted to", type(_val))
                elif DEBUGGING: print("\tValue '" + _attrib[0] + "'")
                
                setattr(_obj, _attrib[0], _val)

                #For debugging purposes! Remove and add sprite stuff here
                if _attrib[0] == "color":
                    _obj.colorize(_obj.color)

        else:
            print("Warning: Couldn't load type '" + scene_object[0] + "' (Not a valid type)")

    return True

def save():
    for obj in objects.getObjectsOfType():
        pass
