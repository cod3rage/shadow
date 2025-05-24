class Gun():
    def __init__(self, rounds = 5, fire_rate = .2, auto = False ,angle = 20, pierce = 1, knockback= 20, recoil= 10, damage=12):
        self.rounds = rounds
        self.mag = rounds
        #
        self.auto = auto
        self.angle = angle
        self.pierce = pierce
        self.knockback = knockback
        self.recoil = recoil
        self.damage = damage
        #
        self.reload_time = 5
        self.reloading = False
        self.reload_g = 0 # time perameter
        #
        self.fire_rate_g = 0 # time perameter
        self.fire_rate = 1 

        self.firing = False

    

    def data(self):
        return self.angle, self.pierce, self.knockback, self.recoil, self.damage
    
    def update(self, g_time):
        if self.reloading and g_time-self.reload_g >= self.reload_time:
            self.rounds = self.mag
            self.reloading = False

    def reload(self, g_time):
        if not self.reloading and self.rounds < self.mag:  
            self.reloading = True
            self.reload_g = g_time
    
    def request_fire(self, g_time = 0):
        if self.reloading or (g_time - self.fire_rate_g < self.fire_rate): 
            return
        elif self.rounds <= 0: 
            self.reload(g_time) 
            return
        return True
    
    def fired(self, g_time = 0):
        self.fire_rate_g = g_time
        self.rounds -= 1
        
        
    
    def equiped(self):
        pass

    def unquiped(self):
        pass