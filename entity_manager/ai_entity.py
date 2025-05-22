from . import entities

class ground_ai(entities.PhysicsEntity):
    def __init__(self, hitbox=(60,90), pos=(0,0), range = 200, spd = 12,hp = 100, atk_int = .2):
        super().__init__(hitbox, pos)
        self.target = None
        self.range = range
        self.health = hp
        self.max_health = hp
        self.walkspeed = spd
        self.interval = atk_int

        self.timer = 0
        self.dead = False
    
    def update(self, tick):
        super().update(tick)
        if (not self.target) or self.falling or self.dead: return
        if self.in_range(self.target.x, self.target.y):
            self.attack_request(tick)
        else:
            self.timer = 0

    def in_range(self, x, y):
        return abs(self.x - x) <= self.range and abs(self.y - y) <= self.range
    
    def render(self, surface):
        super().render(surface)
    
    def attack_request(self, tick):
        self.timer += tick
        if self.timer / self.interval >= 1:
            self.timer = 0
            self.attack()
    
    def attack(self):
        pass
    
    def attacked(self, dmg):
        self.health -= dmg
        if self.health - dmg < 0:
            self.died()
        else:
            self.health -= dmg
    
    def died(self):
        self.dead = True
