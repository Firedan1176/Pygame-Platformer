import pygame

class Sprite:
    def __init__(self, filename):
        self.sprite_table = {}

        a = pygame.Surface((32, 32))
        a.fill((255, 0, 255))
        self.sprite_table["None"] = [a]
        self.sprite_index = 0
        self.playback_speed = 1
        self.target_sprite = "None"

        try:
            self.surf = pygame.image.load(filename).convert_alpha()
        except Exception as e:
            #TODO: Throw an error? What should happen?
            pass

    #Partition this Spritesheet into individual Surfaces
    #Returns the list of Surfaces
    def partition(self, name = "Sprite list", rect = pygame.Rect(0, 0, 32, 32), size = (32, 32)):
        lst = []
        if ((rect.h - rect.y) % size[1] != 0 or (rect.w - rect.x) % size[0] != 0):
            print("Sprite loading error: Partition dimensions are not divisible by the size given")
            return None
        
        for y in range(rect.h - rect.y // size[0]):
            for x in range(rect.w - rect.x // size[1]):
                a = pygame.Surface(size)
                a.blit(self.surf, rect, rect)
                lst.append(a)
                
        #Add the list, with name, into the dictionary
        #While loop will avoid overwriting
        count = 0
        temp_name = name
        while temp_name in self.sprite_table:
            count += 1
            temp_name = name + " " + str(count)

        #Set the "default" sprite from None to this partition IF this is the first partition
        if len(self.sprite_table) == 1: self.target_sprite = name
        
        self.sprite_table[temp_name] = lst
        return lst

    #Returns a Surface of the current sprite to draw.
    def get(self, name = None):
        if name == None:
            if self.target_sprite == "None":
                return self.sprite_table["None"][0]
            else:
                return self.sprite_table[self.target_sprite][self.sprite_index]
        else:
            return self.sprite_table[name][self.sprite_index]

    #Plays a sprite animation from the sprite_table
    def play(self, name, looping = True):
        self.target_sprite = name
        self.sprite_index = 0
        pass

    def stop(self, name):
        pass
