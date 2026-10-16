from copy import copy
from classes.Dashboard import Dashboard
from classes.Maths import Vec2D

class Item(Dashboard):
    def __init__(self, collection, screen, x, y):
        super().__init__("./img/font.png", 8, screen)

        self.item_pos = Vec2D(x, y)
        self.item_vel = Vec2D(0, 0)
        self.screen = screen
        self.coin_animation = copy(collection.get("coin-item").animation)
        self.sound_played = False

    def spawnCoin(self, cam, dashboard):
        if not self.sound_played:
            #TODO: Increment point counter
            self.sound_played = True

        self.coin_animation.update()

        if self.coin_animation.timer < 45:
            if self.coin_animation.timer < 15:
                self.item_vel.y -= 0.5
                self.item_pos.y += self.item_vel.y
            else:
                self.item_vel.y += 0.5
                self.item_pos.y += self.item_vel.y
                
            self.screen.blit(self.coin_animation.image, (self.item_pos.x + cam.x, self.item_pos.y))
        elif self.coin_animation.timer < 80:
            self.item_vel.y = -0.75
            self.item_pos.y += self.item_vel.y
            self.draw_text("100", self.item_pos.x + 3 + cam.x, self.item_pos.y, 8)