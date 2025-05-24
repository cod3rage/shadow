import pygame
import math
from . import entities

bullet_accuracy = 5

class Player(entities.PhysicsEntity):
    def __init__(self):
        super().__init__((60,90),(360,360))
        self.facing = 0

        self.dmg = 30
        self.health = 100
        self.regen_speed = 5 # per sec
        self.max_health = 100
        
        self.dmg_mul = 1
        self.dmg_bonus = 0
        self.speed = 1

        self.last_kill = 0
        self.kill_streak = 0
        self.rotation = 0

        self.score = 0
        self.score_bonus = 0
        self.score_mul = 1

        self.level = 0
        self.exp = 0

        self.jumps = 1
        self.last_jump = 0
    
    def update(self, tick):
        if self.y - self.vy> self.floor:
            self.y = self.floor
            self.vy = 0 
            self.falling = False
            self.jumps = 2
        elif self.y < self.floor :
            self.vy = max(-50,self.vy-30*tick)
            self.falling = True
        self.vx -= tick * 12 * self.vx
        self.y -= self.vy
        self.x -= self.vx

        #

        self.x = max(min(self.x, 720-self.hqx),self.hqx)
        
        if self.vx < -1:
            self.facing = 0
        elif self.vx > 1:
            self.facing = 1
        
        mouse_pos = pygame.mouse.get_pos()

        self.rotation = math.atan2(mouse_pos[1]-self.y, mouse_pos[0]-self.x)

    
    def render(self, surface):
        super().render(surface)
        xrot, yrot = math.cos(self.rotation) * 50 + self.x, math.sin(self.rotation) * 50 + self.y
        pygame.draw.circle(surface, (255,0,0), (xrot, yrot), 5)


    def attacked(self, dmg=0, knockback=0, knockback_strength=0):
        pass
    
    def jump(self, global_time):
        if (global_time-self.last_jump <= 0.25) or (self.jumps <= 0): return
        self.jumps -= 1
        self.vy = 12
        self.last_jump = global_time
    
    def dash(self):
        pass

    def shoot(self, angle = 20, pierce = 0):
        if not self.enemies: return
        
        degre, rads = math.degrees(self.rotation), math.radians(angle/2)
        most, least = ((math.degrees(self.rotation+rads)+180)%360)-180,((math.degrees(self.rotation-rads)+180)%360)-180

        harmed = 0
        
        for enemy in self.enemies.cache:
            hit = False
            for i in range(bullet_accuracy): # divisions along y axis
                agg = math.degrees(math.atan2((enemy.y-enemy.hqy) + enemy.hhy * (i/bullet_accuracy) - self.y, enemy.x - self.x))
                if self.bias_angle(least, most, agg):
                    hit = True
                    break
            print(hit)


    def bias_angle(self,start, end, angle):
        return (start <= angle <= end) if start <= end else (angle >= end or angle <= start)
    
    def block(self):
        pass

    def unblock(self):
        pass

    def charge(self):
        pass

    def end_charge(self):
        pass

    # shikigami

    def shadow(self):
        pass

    def rabbits(self):
        pass
    
    def frog(self):
        pass

    def nue(self):
        pass

    def mahoraga(self):
        pass

    # passives

    def divine_wheel(self):
        pass

    def simple_domain(self):
        pass



   