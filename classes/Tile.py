import pygame as pg

class Tile:
    def __init__(self, sprite, rect):
        self.sprite = sprite
        self.rect = rect

    def draw_rect(self, screen):
        try:
            pg.draw.rect(screen, pg.Color(255, 0, 0), self.rect, 1)
        except Exception:
            pass