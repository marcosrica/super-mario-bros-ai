from Entities.EntityBase import EntityBase
from copy import copy

from Entities.Item import Item
from classes.Animation import Animation
from classes.Camera import Camera
from classes.Dashboard import Dashboard
#from classes.Level import Level

class RandomBox(EntityBase):
    def __init__(self, screen, sprite_collection, x, y, item:Item, dashboard:Dashboard, level:Level, gravity=0):
        super().__init__(x, y, gravity)
        self.screen = screen
        self.sprite_collection = sprite_collection
        self.animation:Animation = copy(self.sprite_collection.get("CoinBox").animation)
        self.type = "Block"
        self.triggered = False
        self.time = 0
        self.max_time = 10
        self.dashboard:Dashboard = dashboard
        self.vel = 1
        self.item = item
        self.level = level

    def update(self, camera:Camera):
        if self.alive and not self.triggered:
            self.animation.update()
        else:
            self.animation.image = self.sprite_collection.get("empty").image
            if self.item == 'RedMushroom':
                self.level.add_red_mushroom(self.rect.x//32, self.rect.y//32 - 1)
            self.item = None

            if self.time < self.max_time:
                self.time += 1
                self.rect.y -= self.vel
            elif self.time < self.max_time * 2:
                self.time += 1
                self.rect.y += self.vel

        self.screen.blit(self.sprite_collection.get("sky").image, (self.rect.x + camera.x, self.rect.y + 2))
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y - 1))
                