import pygame

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
        # stats
        self.health = 200
        self.max_health = 200
        # misc
        self.falling = True
        self.id = 0
        self.tag = ''
        self.team = None
        self.enemies = None
    
    def update(self, tick):
        if self.y - self.vy> self.floor:
            self.y = self.floor
            self.vy = 0 
            self.falling = False
        elif self.y < self.floor :
            self.vy = max(-50,self.vy-30*tick)
            self.falling = True
        self.vx -= tick * 12 * self.vx
        self.y -= self.vy
        self.x -= self.vx
    
    def render(self, surface):
        pygame.draw.rect(surface,(255,255,255),pygame.rect.Rect(self.x-self.hqx,self.y-self.hqy,self.hhx,self.hhy))
    
    def attacked(self, dmg = 0, knockback = 0, knockback_strength = 0):
        pass

    def delete(self):
        if self.team:
            self.team.delete(self.id)
        del self

# --------------------------------------------------- #

class EntityGroup():
    def __init__(self, tag, entities = None, enemies = None):
        self.cache = []
        self.tag = tag
        self.enemies = enemies
        for unit in entities or []:
            self.new(unit)


    def new(self, unit):
        unit.id = len(self.cache)
        unit.tag = self.tag
        unit.team = self
        self.cache.append(unit)
        self.single_retarget(unit)

    def render(self, surface):
        for entity in self.cache:
            entity.render(surface)
    
    def update(self, tick):
        for entity in self.cache:
            entity.update(tick) 
    
    def delete(self, id = None):
        if not (id in self.cache): return
        del self.cache[id]
        for index in range(len(self.cache)):
            enitity = self.cache[index]
            enitity.id = index
    
    def retarget(self, targets = None):
        self.enemies = targets or self.enemies
        for entity in self.cache:
            self.single_retarget(entity)
    
    def single_retarget(self, entity):
        if (not self.enemies) or (not hasattr(entity,'target')): return
        closest = entity.target
        entity.enemies = self.enemies
        for target in self.enemies.cache or []:
            if abs(entity.x-target.x) <= abs(entity.x-closest.x):
                closest = target
        entity.target = closest
    
