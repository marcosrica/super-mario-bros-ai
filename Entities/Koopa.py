import pygame as pg

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.Dashboard import Dashboard
from classes.EntityCollider import CollisionState, EntityCollider
#from classes.Level import Level
from classes.Maths import Vec2D
from Entities.EntityBase import EntityBase
from traits.LeftRightWalk import LeftRightWalkTrait

class Koopa(EntityBase):
    def __init__(self, screen, sprite_coll, x, y, level):
        super().__init__(y-1, x, 1.25)
        self.sprite_collection = sprite_coll
        self.animation:Animation = Animation(
            [
                self.sprite_collection.get("koopa-1").image,
                self.sprite_collection.get("koopa-2").image,
            ]
        )
        self.screen = screen
        self.left_right_trait = LeftRightWalkTrait(self, level)
        self.timer = 0
        self.time_after_death = 35
        self.type = "Mob"
        self.dashboard:Dashboard = level.dashboard
        self.collision:Collider = Collider(self, level)
        self.entity_collider:EntityCollider = EntityCollider(self)
        self.level_obj:Level = level

    def update(self, camera:Camera):
        if self.alive and self.active:
            self.update_alive(camera)
            self.check_entity_collision()
        elif self.alive and not self.active and not self.bouncing:
            self.sleeping_in_shell(camera)
            self.check_entity_collision()
        elif self.bouncing:
            self.shell_bouncing(camera)

    def update_alive(self, camera:Camera):
        self.apply_gravity()
        self.draw_koopa(camera)
        self.animation.update()
        self.left_right_trait.update()

    def shell_bouncing(self, camera:Camera):
        self.left_right_trait.speed = 4
        self.apply_gravity()
        self.animation.image = self.sprite_collection.get("koopa-hiding").image
        self.draw_koopa(camera)
        self.left_right_trait.update()

    def draw_koopa(self, camera:Camera):
        if self.left_right_trait.direction == -1:
            self.screen.blit(
                self.animation.image, (self.rect.x + camera.x, self.rect.y - 32)
            )
        else:
            self.screen.blit(
                pg.transform.flip(self.animation.image, True, False),
                (self.rect.x + camera.x, self.rect.y - 32),
            )

    def sleeping_in_shell(self, camera):
        if self.timer < self.time_after_death:
            self.screen.blit(
                self.sprite_collection.get("koopa-hiding").image,
                (self.rect.x + camera.x, self.rect.y - 32)
            )
        else:
            self.active = True
            self.alive = True
            self.bouncing = False
            self.timer = 0

        self.timer += 0.1

    def check_entity_collision(self):
        for ent in self.level_obj.entity_list:
            if ent is not self:
                collision_state:CollisionState = self.entity_collider.check(ent)
                if collision_state.is_colliding and ent.bouncing:
                    self.alive = False
