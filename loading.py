import objects
from objects import *
import inspect
import pygame
import re
from pygame.math import Vector2

def load(filename):
    objects.unloadScene()

    try:
        file = open(filename + ".map", 'r')
    except:
        raise IOError('Invalid scene name:', str(filename))
        return False

    
    
    return True

#getattr, setattr
def save():
    out_str = ""
    for obj in objects.scene_gameobjects:
        out_str += "{\n\t" + str(obj.__class__) + "\n\t"
        for var in vars(obj):
            attrib = getattr(obj, var)
            if attrib.__class__ in [pygame.Surface]: continue
                
            out_str += var + ":" + str(attrib) + "\n\t"
        out_str += "}\n"

    print(out_str)

def load(filename):
    try:
        f_in = open(filename, 'r')
    except:
        return False

    text = f_in.read()
    pass
