import pygame

entities = []

tagged = [[],[]]

def Render(surface = None):
    if not surface: return
    for group in tagged:
        for entity in group:
            entity.render(surface)
                

def Update(tick = 0):
    for group in tagged:
        for entity in group:
            entity.update(tick)



class PhysicsEntity:
    def __init__(self, hitbox = (5,5), pos = (0,0)):
        #hitbox
        self.hx = hitbox[0]
        self.hy = hitbox[1]
        #hitbox mathematicals
        self.hhx = self.hx/2
        self.hhy = self.hy/2
        self.hqx = self.hhx/2
        self.hqy = self.hhy/2
        self.floor = 720-120-self.hqy # floor y = base - padding - hitbox
        #position
        self.x = pos[0]
        self.y = pos[1]
        # velocity
        self.vx = 0
        self.vy = 0
        # misc
        self.falling = True
    
    def update(self, tick):
        if self.y - self.vy> self.floor:
            self.y = self.floor
            self.vy = 0 
            self.falling = False
        elif self.y < self.floor :
            self.vy = max(-50,self.vy-30*tick)
            self.falling = True
        self.y -= self.vy
        self.x -= self.vx
    
    def render(self, surface):
        pygame.draw.rect(surface,(255,255,255),pygame.rect.Rect(self.x-self.hqx,self.y-self.hqy,self.hhx,self.hhy))
    
    def hurt(self):
        pass

    def die(self):
        pass




class Player(PhysicsEntity):
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

        last_kill = 0
        kill_streak = 0
        score = 0
        score_bonus = 0
        score_mul = 1


        tagged[0].append(self)
    
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
        
        
    
'''
scale = (120,120)
left, top = self.x + self.hqx - (scale[0]+self.hhx)*self.facing , self.y-scale[1]/2
right, bottom = left + scale[0], top + scale[1]
'''



class Enemy(PhysicsEntity):
    def __init__(self, hitbox = (60,90), hp = 80, dmg = 0, spd = 32, range = 200):
        super().__init__(hitbox,(0,0))
        self.health = hp
        self.max_health = hp
        self.dmg = dmg
        self.wlk_speed = spd
        self.atk_range = range
        self.hrange = range/2

        self.attacking = False
        self.last_attack = 0
        self.record = 0

        tagged[1].append(self)
    
    def update(self, tick):
        super().update(tick)
        plr = tagged[0][0]
        if not plr: return

        ylocked = (self.y - self.hrange < plr.y <= self.y + self.hrange)
        xlocked = (self.x - self.hrange < plr.x <= self.x + self.hrange)

        self.attacking = (xlocked and ylocked)

        if not (self.attacking or self.falling) and (abs(plr.x-self.x) > 1):
            dir = 0
            if self.x > plr.x:
                dir = -self.wlk_speed
            elif self.x < plr.x:
                dir = self.wlk_speed

            self.x += dir * tick