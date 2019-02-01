import pygame

def buildSprites(path,size):
    
    img = pygame.image.load(path)
    img.convert_alpha()
    
    width = img.get_width()
    height = img.get_height()
    
    xcount = width//size[0]
    ycount = height//size[1]
    
    spritelist = []
    
    for y in range(ycount):
        for x in range(xcount):
            temp = pygame.Surface(size)
            temp.blit(img,(0,0),((x*16),(y*16),size[0],size[1]))
            spritelist.append(temp)
            
    return spritelist