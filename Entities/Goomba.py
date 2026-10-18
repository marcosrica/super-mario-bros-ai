from tokenize import String

from classes.Animation import Animation

from Entities.EntityBase import EntityBase
from classes.Camera import Camera, Vec2D
from classes.Collider import Collider
from classes.Dashboard import Dashboard
#from classes.Level import Level
from traits.LeftRightWalk import LeftRightWalkTrait
from classes.EntityCollider import EntityCollider

class Goomba(EntityBase):
    def __init__(self, screen, sprite_coll, x, y, level):
        super().__init__(y, x-1, 1.25)
        self.sprite_collection = sprite_coll

        self.animation = Animation(
            [
                self.sprite_collection.get("goomba-1").image,
                self.sprite_collection.get("goomba-2").image
            ]
        )

        self.screen = screen
        self.left_right_trait = LeftRightWalkTrait(self, level)
        self.type = "Mob"
        self.dashboard:Dashboard = level.dashboard
        self.collision:Collider = Collider(self, level)
        self.entity_collider:EntityCollider = EntityCollider(self)
        self.level_obj:Level = level
        self.text_pos:Vec2D = Vec2D(0, 0)

    def update(self, draw:bool, camera:Camera):
        if self.alive:
            self.apply_gravity()
            if draw:
                self.draw_goomba(camera)
            self.left_right_trait.update()
            self.check_entity_collision()
        else:
            self.on_dead(camera)

    def on_dead(self, camera:Camera):
        if self.timer == 0:
            self.set_points_text_start_position(self.rect.x + 3, self.rect.y)
        elif self.timer < self.time_after_death:
            self.move_points_text_up_and_draw(camera)
            self.draw_flat_goomba(camera)
        else:
            self.alive = None
        self.timer += 0.1
        
    def draw_goomba(self, camera:Camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y))
        self.animation.update()

    def draw_flat_goomba(self, camera:Camera):
        self.screen.blit(
            self.sprite_collection.get("goomba-flat").image,
            (self.rect.x + camera.x, self.rect.y)
        )

    def check_entity_collision(self):
        for ent in self.level_obj.entity_list:
            collision_state = self.entity_collider.check(ent)
            if collision_state.is_colliding and ent.type == "Mob":
                self.on_collision_with_mob(ent, collision_state)

    def on_collision_with_mob(self, mob:EntityBase, collision_state):
        if collision_state.is_colliding and mob.bouncing:
            self.alive = False

    def set_points_text_start_position(self, x, y):
        self.text_pos = Vec2D(x, y)

    def move_points_text_up_and_draw(self, camera:Camera):
        self.text_pos.y += -0.5
        self.dashboard.draw_text("100", self.text_pos.x + camera.x, self.text_pos.y, 8)