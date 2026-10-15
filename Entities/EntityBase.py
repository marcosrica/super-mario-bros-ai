import pygame as pg
from classes.Maths import Vec2D

class EntityBase(object):
    def __init__(self, x, y, gravity):
        self.vel = Vec2D()
        self.rect = pg.Rect(x*32, y*32, 32, 32)
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.active = True
        self.bouncing = False
        self.time_after_death = 5
        self.timer = 0
        self.type = ""
        self.on_ground = False
        self.obey_gravity = True

    def apply_gravity(self):
        if self.obey_gravity:
            self.vel.y += self.gravity

    def update_traits(self):
        for trait in self.traits.values():
            try:
                trait.update()
            except AttributeError:
                pass

    def get_pos_index(self):
        return Vec2D(self.rect.x // 32, self.rect.y // 32)

    def get_pos_index_as_float(self):
        return Vec2D(self.rect.x / 32.0, self.rect.y / 32.0)