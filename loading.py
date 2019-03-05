import os
import pygame
import objects
import re
import sys
import json
import ast
import player
import sprite2

from pygame.math import Vector2


"""Dictionary that pairs an ID to an intermediate class for object configurations"""
object_database = {}

#Classes to generate Objects from in the scene
CLASSES = {
        "GameObject":objects.GameObject,
        "Entity":objects.Entity,
        "Player":player.Player,
        "Chest":objects.Chest
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
        "size":Vector2,
        "collisions":bool,
        "tex":str
    }

VERSION = 1
DEBUGGING = True

"""Intermediate class for generating objects"""
class ObjConfig:

    loadedObjs = {}
    databaseFile = None
    databaseText = None
    
    def __init__(self, sourceStr):
        self._attribs = {}
        _id, _name = sourceStr.split('\n')[0].split(':')
        for line in sourceStr.split('\n')[1:]:
            _key, _value = line.split(':')
            if _key == "class":
                if _value in CLASSES:
                    self._class = CLASSES[_value] #Do not generate object here. Just store which Class it is
                else: print("Warning: type '" + _value + "' couldn't be loaded from the database.")
            elif _key in TYPE_TABLE:
                _trueVal = ast.literal_eval(_value) #Eval string to builtin
                _trueVal = TYPE_TABLE[_key](_trueVal) #Init pygame/custom object from builtin (i.e. tuple -> vector2)
                self._attribs[_key] = _trueVal #Set all other vals

    """Generates and returns a new object from this config"""
    def objectFrom(self, z = 0, position = Vector2(0, 0), scale = Vector2(0, 0), texmode = "none"):
        _obj = self._class(z)
        _obj.position = position
        _obj.scale = scale

        #Set tex to straight magenta to indicate errors if not loaded
        _obj.sprite = pygame.Surface(_obj.scale)
        _obj.sprite.fill((255, 0, 255))
        for _key, _value in self._attribs.items():
            if _key == "tex":
                _obj.sprite = sprite2.loadSprite(_value, texmode, scale)
            else: setattr(_obj, _key, _value)

        return _obj

    def get(obj_id):
        if obj_id in ObjConfig.loadedObjs:
            return ObjConfig.loadedObjs[obj_id]
        else:
            if ObjConfig.databaseText == None:
                databaseFile = open("database.dat", 'r')
                ObjConfig.databaseText = databaseFile.read()
                databaseFile.close()

            lines = ObjConfig.databaseText.split('\n')
            for i in range(len(lines)):
                _key, _value = lines[i].split(":")
                if not lines[i][0] == "\t" and lines[i + 1][0] == "\t":
                    _objValue = lines[i] + "\n"
                    while lines[i + 1][0] == "\t":
                        if i + 2 == len(lines) or not lines[i + 2][0] == "\t":
                            _objValue += lines[i + 1]
                            break
                        else:
                            _objValue += lines[i + 1] + "\n"
                            i += 1
                    _objValue = _objValue.replace('\t', '')
                    if int(_key) == obj_id:
                        if DEBUGGING: print("Found matching ID:", _key)
                        _obj = ObjConfig(_objValue)
                        x = ObjConfig.loadedObjs[obj_id] = _obj
                        return x
            
            print("Not found")

    """Note you may not want to really ever do this"""
    def purge():
        ObjConfig.loadedObjs.clear()
        ObjConfig.databaseText = None
        
        
    

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
    
    #Meat of the loading
    for line in file_text.split('\n'):
        #Skip comments and empty lines
        if len(line) == 0 or line[0] == "#": continue
        #Properties are separated by semicolon in map file.
        #Property order: [ID];[Z];[POS];[SCALE];[TEXMODE]
        props = line.split(';')
        prop_id = int(props[0])
        prop_z = int(props[1])
        prop_pos = Vector2(ast.literal_eval(props[2]))
        prop_scale = Vector2(ast.literal_eval(props[3]))
        prop_texmode = props[4]

        config_obj = ObjConfig.get(prop_id)
        obj = config_obj.objectFrom(z = prop_z, position = prop_pos, scale = prop_scale, texmode = prop_texmode)
    
    return True

def save(filename, name, overwrite = False):
    if os.path.isfile(filename) and not overwrite:
        raise IOError('Cannot save level: The file \'' + filename + '\' already exists')

    try:
        file_out = open(filename + ".map", 'w')
    except:
        raise IOError('Cannot save level: There was an IO Error')


    file_out.write("{\n\t\"version\": \"" + str(VERSION) + "\"\n")
    for obj in objects.getObjectsOfType():
        _prop = "\t" + objects.formattedPropertyString(obj)
        file_out.write(_prop)
    file_out.write("\t\"name\": " + name + "\\n}")
    file_out.close()
