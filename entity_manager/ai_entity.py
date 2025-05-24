import pygame
from . import entities

class ground_ai(entities.PhysicsEntity):
    def __init__(self, hitbox=(60,90), pos=(0,0), range = 60, spd = 20,hp = 100, atk_int = .2):
        super().__init__(hitbox, pos)
        self.target = None
        self.range = range
        self.health = hp
        self.max_health = hp
        self.walkspeed = spd
        self.interval = atk_int

        self.timer = 0
        self.title = 'Entity'
    
    def update(self, tick):
        super().update(tick)
        if (not self.target) or self.falling or self.dead or self.soft_locked: return
        if self.in_range(self.target.x, self.target.y) and  0 < self.x < 720:
            self.attack_request(tick)
        else:
            self.timer = 0
            self.forward = self.target.x <= self.x
            if self.forward:
                self.vx = max(-self.walkspeed,self.vx+(self.walkspeed/2)*tick)
            else:
                self.vx = min(self.walkspeed,self.vx-(self.walkspeed/2)*tick)
                


    def in_range(self, x, y):
        return abs(self.x - x) <= self.range and abs(self.y - y) <= self.range
    
    def render(self, surface):
        if self.dead: 
            pygame.draw.rect(surface,(100,100,100),pygame.rect.Rect(self.x-self.hqx,self.y-self.hqy,self.hhx,self.hhy))
        else:
            super().render(surface)
    
    def attack_request(self, tick):
        self.timer += tick
        if self.timer / self.interval >= 1:
            self.timer = 0
            self.attack()
    
    def attack(self):
        self.target.attacked(5)
    
    def attacked(self, dmg):
        self.health -= dmg
        if self.health - dmg < 0:
            self.died()
        else:
            self.health -= dmg
    
    def died(self):
        self.dead = True
        self.delete()
