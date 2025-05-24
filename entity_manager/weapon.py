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
        self.reload_g = 0
        
        self.fire_rate = .2

        self.firing = False

    

    def data(self):
        return self.angle, self.pierce, self.knockback, self.recoil, self.damage
    
    def equiped(self):
        pass

    def unquiped(self):
        pass