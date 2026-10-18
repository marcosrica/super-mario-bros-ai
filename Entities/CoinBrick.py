from copy import copy
from Entities.EntityBase import EntityBase
from Entities.Item import Item

class CoinBrick(EntityBase):
    def __init__(self, screen, sprite_collection, x, y, dashboard, draw:bool, gravity=0):
        super(CoinBrick, self).__init__(x, y, gravity)
        self.screen = screen
        self.sprite_collection = sprite_collection
        self.image = self.sprite_collection.get("bricks").image
        self.type = "Block"
        self.triggered = False
        self.dashboard = dashboard
        self.item = Item(sprite_collection, screen, self.rect.x, self.rect.y, draw)

    def update(self, draw:bool, cam):
        if not self.alive or self.triggered:
            self.image = self.sprite_collection.get("empty").image
            self.item.spawnCoin(cam, self.dashboard)

        if draw:
            self.screen.blit(
                self.sprite_collection.get("sky").image,
                (self.rect.x + cam.x, self.rect.y - 1)
            )