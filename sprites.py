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

class SpriteList():
    
    def __init__(self,dictionary = None):
        
        self.spritelist = [] #Stored list of every sprite.
        self.filelist = [] #Stored list of every file already loaded.
        self.fileaddition = {
                None : 0
                } #This is an additive key to skip towards the sprites from a certain file.
        if type(dictionary) == dict: #Dictionary for indexes for sprites of a common animation.
            self.dictionary = dictionary 
        else:
            self.dictionary = {}
            
    def loadfile(self,path,size): #Should be self-explanitory, uses outside function
        if path in self.filelist == False:
            sprites = buildSprites(path,size)
            for sprite in sprites:
                self.spritelist.append(sprite)
            self.filelist.append(path)
            self.fileaddition[path] = len(self.spritelist) - len(sprites)
            
    def pullSprite(self,index,path=None): #Pullsprite gives a sprite from the total list
        return self.spritelist[index + self.fileaddition[path]]
    
    def pull(self,index,name): #Pull gives the frame of an animation
        return self.dictionary[name][index]
    
    def length(self,name): #Made for shorthand for checking length of animations
        return len(self.dictionary[name])
    
    """
    setAnimation sets indexes of currently loaded sprites to a single name, aimed to act
    as grouping frames of an animation. Indexes is a list of indexes for frames, giving the
    index of the total list (if you know which order the files have been loaded) or through
    it's index within its own file by also giving the file's path through the path variable.
    """
    def setAnimation(self,indexes,name,path=None):
        if name in self.dictionary == False:
            templist = []
            for index in indexes:
                templist.append(index + self.fileaddition[path])
            self.dictionary[name] = templist
            
class AnimationHandler():
    
    def __init__(self,name,spritelist,items=None):
        self.name = name
        self.spritelist = spritelist
        if type(items) == list:
            self.animations = items
            
        self.index = 0
        self.previousname = None
        
    def pull(self,name2): #Name2 is called such as wherein to reduce confusion with self.name
        if self.previousname != name2:
            self.index = 0
        if self.index >= self.spritelist.length(self.name+name2):
            self.index = 0
        return self.spritelist.pull(self.index,self.name+name2)
        self.index += 1
        self.previousname = name2
