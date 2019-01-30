from pygame.locals import *

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
def evaluate(event):
    for item in inputScheme.values():
        if event.key == item.val and event.type == item.activation:
            item.action(item.args)
