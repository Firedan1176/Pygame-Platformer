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

    def __init__(self, name, positiveKey, negativeKey, action, *args):
        self.name = name
        self.positiveKey = positiveKey
        self.negativeKey = negativeKey
        self.action = action
        self.args = args or None
        self.positive = False
        self.negative = False

    def getValue(self):
        if self.positive == self.negative: return 0
        if self.positive: return 1
        if self.negative: return -1

#Generates a new Axis object that will call lambda function
def createAxis(name = "New axis", positiveKey = None, negativeKey = None, action = None, *args):
    name = friendlyName(name, inputScheme)
    _axis = useraxis(name, positiveKey, negativeKey, action, args)
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
                    if event.key == item.positiveKey:
                        if event.type == KEYDOWN: item.positive = True
                        elif event.type == KEYUP: item.positive = False
                    elif event.key == item.negativeKey:
                        if event.type == KEYDOWN: item.negative = True
                        elif event.type == KEYUP: item.negative = False

    #Evaluate changed axes after all events have been evaluated
    for axis in [axes for axes in inputScheme.values() if axes.__class__ == useraxis]:
        #Dict = {<type 'useraxis'> : int}, so indexing axes_totals at item (key) gives int (value)
        axis.action(axis.getValue())
