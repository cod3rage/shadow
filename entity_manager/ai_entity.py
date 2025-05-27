import pygame
import math
from . import entities

class ground_ai(entities.PhysicsEntity):
    def __init__(self, hitbox=(60,90), pos=(0,0), range = 60, spd = 20,hp = 100, atk_int = .2, damage = 0):
        super().__init__(hitbox, pos)
        self.target = None
        self.range = range
        self.health = hp
        self.max_health = hp
        self.walkspeed = spd
        self.interval = atk_int
        self.spawn_chance = .3
        self.damage = damage

        self.timer = 0
        self.title = 'Entity'

    def conditions(self):
        return self.in_range(self.target.x, self.target.y) and self.hhx < self.x < 720-self.hqx
    
    def update(self, tick):
        super().update(tick)
        if (not self.target) or self.falling or self.dead or self.stunned: return
        if self.conditions():
            self.attack_request(tick)
        else:
            self.timer = 0
            self.forward = self.target.x <= self.x
            if self.forward:
                self.vx = max(-self.walkspeed,self.vx+(self.walkspeed/2)*tick)
            else:
                self.vx = min(self.walkspeed,self.vx-(self.walkspeed/2)*tick)
                


    def in_range(self, x, y):
        return (abs(self.x - x) <= self.range and abs(self.y - y) <= self.range)
    
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
        self.target.attacked(self.damage, self)
        if self.target.dead:
            self.target = None
            if self.team:
                self.team.single_retarget(self)
    
    def attacked(self, dmg, user = None):
        self.health -= dmg
        if self.health - dmg < 0:
            self.died()
        else:
            self.health -= dmg
    
    def died(self):
        self.dead = True
        self.delete()

class Transfigured(ground_ai):
    def __init__(self, pos = (0,0)):
        super().__init__((60,90), pos, 70, 22, 120, 2, 5)

class Vengful(ground_ai):
    def __init__(self, pos = (0,0)):
        super().__init__((60, 120), pos, 500, 12, 1, 200, 0)
    
    def attacked(self, dmg, attacker = None):
        if attacker:
            attacker.stun(4)
            attacker.attacked(12)
        if dmg >= 1:
            self.died()
    
    def attack(self): return

    def update(self, tick):
        if self.local_time >= 25: # lifetime of 25 seconds
            self.died()
        super().update(tick)

class Thunder(ground_ai):
    def __init__(self, pos = (0,0)):
        super().__init__((60, 90), pos, 0, 80, 50, 4, 30)

    def attack(self):
        if self.target.y+self.target.hqy > 530:
            self.target.attacked(self.damage, self)
            if self.target.dead:
                self.target = None
        self.vx += 200 if self.forward else -200
    
    def conditions(self):
        return self.hhx+30 < self.x < 720-self.hqx-30

class JoGoat(ground_ai):
    def __init__(self, pos = (0,0)):
        super().__init__((60, 90), pos, 250, 44, 60, 4, 30)
    
    def in_range(self, x, y):
        return abs(self.x - x) <= self.range
    
    def attack(self):
        super().attack()
        rot = math.atan2(self.y - self.target.y, self.x - self.target.x)
        self.target.vx -= math.cos(rot) * 20
        self.target.vy -= math.sin(rot) * 20


class BigRaga(ground_ai):
    def __init__(self, pos = (0,0)):
        super().__init__((120,180), pos, range = 100, spd = 50, hp=300, atk_int=1, damage=60)
        self.hr = self.range/2
    
    def attack(self):
        left, top = self.target.x - self.range, self.target.y - self.range
        right, bottom = left + self.range * 2, top + self.range * 2

        for enemy in self.enemies.cache:
            if left<enemy.x<=right and top<enemy.y<=bottom:
                enemy.attacked(self.damage, self)
                enemy.vx -= max(-50, min(50, self.range/(enemy.x-self.x) * 12))
                enemy.vy += 16

    



