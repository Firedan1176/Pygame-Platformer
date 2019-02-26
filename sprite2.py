import pygame

loadedSpritesheets = {}
loadedSprites = {}

def loadSpritesheet(filename, useColorkey = True):
    try:
        if useColorkey:
            _surf = pygame.image.load(filename).convert()
            _surf.set_colorkey((255, 0, 255))
        else:
            _surf = pygame.image.load(filename).convert_alpha()
    except:
        raise IOError('There was an error loading spritesheet \'' + filename + '\'')
    else:
        loadedSpritesheets[filename] = _surf


"""Load a sprite. Index can be either an integer, list, or a range()"""
def loadSprite(filename, name, index, scale = (32, 32)):
    if type(index) == list or type(index) == range:
        if not filename in loadedSpritesheets:
            loadSpritesheet(filename)
        lst = []
        size = loadedSpritesheets[filename].get_size()
        for i in index:
            coords = (i % (size[0] // scale[0]), i // (size[1] // scale[1]))

            surf = pygame.Surface(scale)
            surf.blit(loadedSpritesheets[filename], coords)

            lst.append(surf)

        loadedSprites[filename + "_" + name] = lst
        return lst
    
    elif type(index) == int:
        if not filename in loadedSpritesheets:
            loadSpritesheet(filename)
        size = loadedSpritesheets[filename].get_size()
        coords = (index % (size[0] // scale[0]), index // (size[1] // scale[1]))

        surf = pygame.Surface(scale)
        surf.blit(loadedSpritesheets[filename], coords)

        loadedSprites[filename + "_" + name] = surf
        return surf
    else:
        raise TypeError('Failed to load sprite: index must be an int, list, or range() (got ' + str(type(index)) + ')')
