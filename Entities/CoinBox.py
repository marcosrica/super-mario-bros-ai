from copy import copy
from Entities.EntityBase import EntityBase
from Entities.Item import Item

class CoinBox(EntityBase):
    def __init__(self, screen, sprite_collection, x, y, dashboard, draw:bool, gravity=0):
        super(CoinBox, self).__init__(x, y, gravity)
        self.screen = screen
        self.sprite_collection = sprite_collection
        self.animation = copy(self.sprite_collection.get("CoinBox").animation)
        self.type = "Block"
        self.triggered = False
        self.time = 0
        self.max_time = 10
        self.dashboard = dashboard
        self.vel = 1
        self.item = Item(sprite_collection, screen, self.rect.x, self.rect.y, draw)

    def update(self, draw:bool, cam):
        if self.alive and not self.triggered:
            self.animation.update()
        else:
            self.animation.image = self.sprite_collection.get("empty").image
            self.item.spawnCoin(cam, self.dashboard)
            if self.time < self.max_time:
                self.time += 1
                self.rect.y -= self.vel
            else:
                if self.time < self.max_time * 2:
                    self.time += 1
                    self.rect.y += self.vel

        if draw:
            self.screen.blit(
                self.sprite_collection.get("sky").image,
                (self.rect.x + cam.x, self.rect.y + 2),
            )

            self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y - 1))