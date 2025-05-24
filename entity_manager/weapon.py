class Gun():
    def __init__(self):
        self.angle = 20
        self.pierce = 1
        self.knockback = 20
        self.recoil = 8
        self.damage = 12

    def data(self):
        #angle, pierce , knockback, recoil, damage
        return self.angle, self.pierce, self.knockback, self.recoil, self.damage