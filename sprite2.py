import pygame

loadedSprites = {}

"""Load a sprite. Mode can be None, 'stretch', 'tile', or '9slice',
where scale is the size of the object. Set exclude to True to exclude it from the
sprite list. Use this when scaling sprites every frame, etc."""
def loadSprite(filename, mode = None, scale = None, exclude = False):
    if filename in loadedSprites:
        return loadedSprites[filename]
    
    try:
        _surf = pygame.image.load(filename + ".png").convert_alpha()
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
        elif mode == "9slice" and scale:
            sourceSize = _surf.get_size()
            cellSize = tuple(x // 3 for x in sourceSize)
            #Clamp the size to be >= minimum cellSize
            scale = (scale[0] if scale[0] > cellSize[0] * 2 else cellSize[0] * 2, scale[1] if scale[1] > cellSize[1] * 2 else cellSize[1] * 2)

            #Final result
            joint = pygame.Surface(scale, flags = pygame.SRCALPHA)

            #Top, Bottom, Left, Right
            horzSurf = pygame.Surface((cellSize[0], sourceSize[1]), flags = pygame.SRCALPHA)
            vertSurf = pygame.Surface((sourceSize[0], cellSize[0]), flags = pygame.SRCALPHA)

            #Topleft, Topright, Bottomleft, Bottomright
            joint.blit(_surf, (0, 0), area = pygame.Rect((0, 0), tuple(x // 3 for x in sourceSize)))
            joint.blit(_surf, (scale[0] - cellSize[0], 0), area = pygame.Rect((cellSize[0] * 2, 0), tuple(x // 3 for x in sourceSize)))
            joint.blit(_surf, (0, scale[1] - cellSize[1]), area = pygame.Rect((0, (cellSize[1] * 2)), tuple(x // 3 for x in sourceSize)))
            joint.blit(_surf, (scale[0] - cellSize[0], scale[1] - cellSize[1]), area = pygame.Rect((cellSize[0] * 2, cellSize[1] * 2), tuple(x // 3 for x in sourceSize)))

            horzSurf.blit(_surf, (0, 0), area = pygame.Rect((cellSize[0], 0), (cellSize[0], sourceSize[1])))
            vertSurf.blit(_surf, (0, 0), area = pygame.Rect((0, cellSize[1]), (sourceSize[0], cellSize[1])))

            horzSurf = pygame.transform.scale(horzSurf, (scale[0], sourceSize[1]))
            vertSurf = pygame.transform.scale(vertSurf, (sourceSize[0], scale[1]))

            midSurf = pygame.transform.scale(_surf, scale)
            
            joint.blit(horzSurf, (cellSize[0], 0), area = pygame.Rect((cellSize[0], 0), (scale[0] - (cellSize[0] * 2), cellSize[1])))
            joint.blit(horzSurf, (cellSize[0], scale[1] - cellSize[1]), area = pygame.Rect((cellSize[0], cellSize[1] * 2), (scale[0] - (cellSize[0] * 2), cellSize[1])))
            joint.blit(vertSurf, (0, cellSize[1]), area = pygame.Rect((0, cellSize[1]), (cellSize[0], scale[1] - (cellSize[1] * 2))))
            joint.blit(vertSurf, (scale[0] - cellSize[1], cellSize[1]), area = pygame.Rect((cellSize[0] * 2, cellSize[1]), (cellSize[0], scale[1] - (cellSize[1] * 2))))

            #Center
            joint.blit(midSurf, cellSize, area = pygame.Rect(cellSize, (scale[0] - cellSize[0] * 2, scale[1] - cellSize[1] * 2)))
            _surf = joint
    except Exception as e:
        raise IOError('There was an error loading sprite \'' + filename + '\':\n' + str(e))
    else:
        #Add to master sprite list if it's wanted
        if not exclude:
            new_name = filename + ("_" + str(mode) if mode else "") + ("_" + str(scale) if scale else "")
            loadedSprites[new_name] = _surf
        return _surf

"""
Loads a series of sprites from a file into a List. Sprites should be left -> right.
cellSize:    Size of each sprite to load from file.
count:       Total sprites to load. Will discard any after this number.
"""
def loadSpriteAnimation(filename, cellSize = (32, 32), count = 0):
    if filename in loadedSprites:
        return loadedSprites[filename]
    try:
        _surf = pygame.image.load(filename + ".png").convert_alpha()

        _list = []
        for row in range(_surf.get_height() // cellSize[1]):
            for col in range(_surf.get_width() // cellSize[0]):
                x = pygame.Surface(cellSize, flags = pygame.SRCALPHA)
                x.blit(_surf, (0, 0), area = pygame.Rect((col * cellSize[0], row * cellSize[1]), cellSize))
                _list.append(x)

        if count > 0:
            for x in range(len(_list) - count):
                _list.pop()

    except Exception as e:
        raise IOError('There was an error loading sprite animation \'' + filename + '\':\n' + str(e))
    else:
        new_name = filename + "_anim"
        loadedSprites[new_name] = _list
        return _list
