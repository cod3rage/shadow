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

        self.jumps = 1
    
    def update(self, tick):
        super().update(tick)
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