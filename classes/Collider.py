#Class for checking the collisions
class Collider:
    def __init__(self, entity, level):
        self.entity = entity
        self.level = level.level
        self.level_obj = level
        self.result = []

    def check_x(self):
        if self.left_level_border_reached() or self.right_level_border_reached():
            return

        try:
            rows = [
                self.level[self.entity.get_pos_index().y],
                self.level[self.entity.get_pos_index().y + 1],
                self.level[self.entity.get_pos_index().y + 2],
            ]
        except Exception:
            return

        for row in rows:
            tiles = row[self.entity.get_pos_index().x: self.entity.get_pos_index().x + 2]
            for tile in tiles:
                if (tile.rect is not None) and (self.entity.rect.colliderrect(tile.rect)):
                    if self.entity.vel.x > 0:
                        self.entity.rect.right = tile.rect.left
                        self.entity.vel.x = 0
                    elif self.entity.vel.x < 0:
                        self.entity.rect.left = tile.rect.right
                        self.entity.vel.x = 0

    def check_y(self):
        self.entity.on_ground = False

        try:
            rows = [
                self.level[self.entity.get_pos_index().y],
                self.level[self.entity.get_pos_index().y + 1],
                self.level[self.entity.get_pos_index().y + 2],
            ]
        except Exception:
            try:
                self.entity.game_over()
            except Exception:
                self.entity.alive = None
            return

        for row in rows:
            tiles = row[self.entity.get_pos_index().x : self.entity.get_pos_index().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                   if self.entity.vel.y > 0:
                        self.entity.on_ground = True
                        self.entity.rect.bottom = tile.rect.top
                        self.entity.vel.y = 0
                       
                        # reset jump on bottom
                        if self.entity.traits is not None:
                            if "JumpTrait" in self.entity.traits:
                               self.entity.traits["JumpTrait"].reset()
                            if "bounceTrait" in self.entity.traits:
                                self.entity.traits["bounceTrait"].reset()

                        if self.entity.vel.y < 0:
                            self.entity.rect.top = tile.rect.bottom
                            self.entity.vel.y = 0

                            
    def right_level_border_reached(self):
        if self.entity.get_pos_index_as_float().x > self.level_obj.level_length - 1:
            self.entity.rect.x = (self.level_obj.level_length - 1) * 32
            self.entity.vel.x = 0
            return True

    def left_level_border_reached(self):
        if self.entity.rect.x < 0:
            self.entity.rect.x = 0
            self.entity.vel.x = 0
            return True