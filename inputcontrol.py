import pygame
import sys
from pygame.locals import *
from utils import friendlyName

inputScheme = {}

#Defines input for a button, and what happens when it's pressed
#Activation evaluates same as pygame's 'event.type'
class userinput:

    def __init__(self, name, val, activation, action, *args):
        self.name = name
        self.val = val
        self.activation = activation
        self.action = action
        self.args = args or None

class useraxis:

    def __init__(self, name, positive, negative, action, *args):
        self.value = 0
        self.name = name
        self.positive = positive
        self.negative = negative
        self.action = action
        self.args = args or None

#Generates a new Axis object that will call lambda function
def createAxis(name = "New axis", positive = None, negative = None, action = None, *args):
    name = friendlyName(name, inputScheme)
    _axis = useraxis(name, positive, negative, action, args)
    inputScheme[name] = _axis

def createInput(name = "New input", val = None, activation = 0, action = None, *args):
    #Name check, tacks on a number to avoid overwriting
    i = 0
    newName = name
    while newName in inputScheme:
        i += 1
        newName = name + " " + str(i)
    name = newName
    
    _input = userinput(name, val, activation, action, args)
    inputScheme[name] = _input

#Evaluates a single keyboard event. Evaluating 'action' passes the instance to the lambda function.
#Example: action = lambda obj: print(obj.id)
def evaluate(events):
    for event in events:
        if event.type == QUIT:
            print("Closing game...")
            pygame.quit()
            sys.exit(0)
            
        elif event.type == KEYDOWN or event.type == KEYUP:
            for item in inputScheme.values():
                if item.__class__ == userinput and event.key == item.val and event.type == item.activation:
                    item.action(item.args)
                    
                elif item.__class__ == useraxis:
                    if event.key == item.positive:
                        if event.type == KEYDOWN: item.value = 1
                        elif event.type == KEYUP: item.value = 0
                    elif event.key == item.negative:
                        if event.type == KEYDOWN: item.value = -1
                        elif event.type == KEYUP: item.value = 0

    #TODO: This may be laggy. This evaluates EVERY axis if it's non-zero, and if there's a ton, then may be laggy
    for item in [axis for axis in inputScheme.values() if axis.__class__ == useraxis]:
        if item.value != 0: item.action(item.value)

