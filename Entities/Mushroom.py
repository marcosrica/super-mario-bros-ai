from turtle import Vec2D

from Entities.EntityBase import EntityBase
from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.Dashboard import Dashboard
from classes.EntityCollider import EntityCollider
from classes.Level import Level
from traits.LeftRightWalk import LeftRightWalkTrait


class RedMushroom(EntityBase):
    def __init__(self, screen, sprite_coll, x, y, level:Level):
        super().__init__(y, x - 1, 1.25)
        self.sprite_collection = sprite_coll
        self.animation:Animation = Animation(
            [
                self.sprite_collection.get("mushroom").image
            ]
        )
        self.screen = screen
        self.left_right_trait:LeftRightWalkTrait = LeftRightWalkTrait(self, level)
        self.type = "Mob"
        self.dashboard:Dashboard = level.dashboard
        self.collision:Collider = Collider(self, level)
        self.entity_collideer:EntityCollider = EntityCollider(self)
        self.level_obj:Level = level
        self.text_pos:Vec2D = Vec2D(0, 0)

    def update(self, camera:Camera):
        if self.alive:
            self.apply_gravity()
            self.draw_red_mushroom(camera)
            self.left_right_trait.update()
            self.check_entity_collision()
        else:
            self.on_dead(camera)

    def on_dead(self, camera:Camera):
        if self.timer == 0:
            self.set_points_text_start_position(self.rect.x + 3, self.rect.y)
        if self.timer < self.time_after_death:
            self.move_points_text_up_and_draw(camera)
        else:
            self.alive = None
        self.timer += 0.1

    def draw_red_mushroom(self, camera:Camera):
        self.screen.blit(self.animation.image, 
            self.rect.x + 3, self.rect.y)
        self.animation.update()

    def set_points_text_start_position(self, x:float, y:float):
        self.text_pos = Vec2D(x, y)

    def move_points_text_up_and_draw(self, camera:Camera):
        self.text_pos.y += -0.5
        self.dashboard.draw_text("100", self.text_pos.x + camera.x, self.text_pos.y, 8)
        
    def check_entity_collision(self):
        pass