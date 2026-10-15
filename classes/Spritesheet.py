import pygame

class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image: ", filename)
            raise SystemExit

    def image_at(self, x, y, scaling_factor, color_key=None, ignore_tile_size=False,
        x_tile_size=16, y_tile_size=16):
        if ignore_tile_size:
            rect = pygame.Rect((x, y, x_tile_size, y_tile_size))
        else:
            rect = pygame.Rect((x*x_tile_size, y*y_tile_size, x_tile_size, y_tile_size))

        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return pygame.transform.scale(image, (x_tile_size*scaling_factor, y_tile_size*scaling_factor))