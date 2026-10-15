from classes.Spritesheet import Spritesheet
import pygame as pg

class Font(Spritesheet):
    def __init__(self, file_path, size):
        Spritesheet.__init__(self, filename=file_path)
        self.chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.char_sprites = self.load_font()

    def load_font(self):
        font = {}
        row = 0
        char_at = 0

        for char in self.chars:
            if char_at == 16:
                char_at = 0
                row += 1

            font.update(
                {
                    char: self.image_at(
                        char_at,
                        row,
                        2,
                        color_key=pg.color.Color(0, 0, 0),
                        x_tile_size=8,
                        y_tile_size=8
                    )
                }
            )
            char_at += 1

        return font