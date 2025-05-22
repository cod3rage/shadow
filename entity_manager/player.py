import pygame
from . import entities

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

    
    def render(self, surface):
        super().render(surface)
        scale = (120,120)
        left, top = self.x+self.hqx-(scale[0]+self.hhx)*self.facing, self.y-scale[1]/2
        pygame.draw.rect(surface, (255,0,0), pygame.rect.Rect(
            left,top,scale[0], scale[1]
        ))
        pygame.draw.circle(surface, (0,0,255),(self.x,self.y),12)


    def attacked(self, dmg=0, knockback=0, knockback_strength=0):
        print('attacked')
    # skills
    
    def jump(self, global_time):
        if (global_time-self.last_jump <= 0.25) or (self.jumps <= 0): return
        
        self.jumps -= 1
        self.vy = 12
        self.last_jump = global_time
    
    def dash(self):
        pass

    def basic_attack(self):
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

    def simple_domain(self):
        pass

    # passives

    def divine_wheel(self):
        pass


   