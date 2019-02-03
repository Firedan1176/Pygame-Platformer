import pygame

#{spritename : Surface}}
sprite_database = {}

def loadSpritesheet(filename):
    if filename in sprite_database:
        return 


class Sprite:
    def __init__(self, filename):
        self.sprite_table = {}

        empty = pygame.Surface((32, 32))
        empty.fill((255, 0, 255))
        self.sprite_table["None"] = [empty]
        self.sprite_index = 0
        self.playback_speed = 1
        self.target_sprite = "None"

        global sprite_database
        if filename in sprite_database:
            self.surf = sprite_database[filename]
        else:
            try:
                self.surf = pygame.image.load(filename).convert_alpha()
                self.sprite_filename = filename
            except Exception as e:
                #TODO: Throw an error? What should happen?
                pass
            sprite_database[filename] = self
            
