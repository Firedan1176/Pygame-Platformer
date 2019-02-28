import pygame

loadedSprites = {}

"""Load a sprite. Mode can be None, 'stretch', or 'tile', where scale is the size of the object."""
def loadSprite(filename, mode = None, scale = None):
    if filename in loadedSprites:
        return loadedSprites[filename]
    
    try:
        _surf = pygame.image.load(filename).convert_alpha()
        if mode == "tile" and scale:
            trueSize = (int(scale[0]) // _surf.get_width(), int(scale[1]) // _surf.get_height())
            print(scale, trueSize)
            _scaledSurf = pygame.Surface(scale)
            for y in range(trueSize[1]):
                for x in range(trueSize[0]):
                    _scaledSurf.blit(_surf, (x * _surf.get_width(), y * _surf.get_height()))
            _surf = _scaledSurf

        elif mode == "stretch" and scale:
            raise NotImplementedError()
    except Exception as e:
        raise IOError('There was an error loading sprite \'' + filename + '\':\n' + str(e))
    else:
        new_name = filename + ("_" + str(mode) if mode else "") + ("_" + str(scale) if scale else "")
        loadedSprites[new_name] = _surf
        return _surf
