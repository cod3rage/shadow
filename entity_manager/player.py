import pygame
import math
from . import entities, weapon

bullet_accuracy = 5

class Player(entities.PhysicsEntity):
    def __init__(self):
        super().__init__((60,90),(360,360))
        self.facing = 0

        self.dmg = 30
        self.health = 150
        self.regen_speed = 5 # per sec
        self.max_health = 150
        
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
        self.gaurding = 0

        self.Primary = weapon.Gun(30,.2, True)
        self.Secondary = weapon.Gun()

        self.Primary_Equiped = True
        self.firing = False

        # gunshot, dash, jump, parry
        self.cd_lst = [0,0,0,0]
    
    def update(self, tick):
        self.local_time += tick
        if self.stunned:
            self.stun_cache = max(0, self.stun_cache - tick)
            self.stunned = (self.stun_cache == 0)
        if self.y - self.vy> self.floor:
            self.y = self.floor
            if self.vy <= -22:
                hurt_amt = abs(self.vy)/22
                slam_scale = 200*hurt_amt
                self.basic_attack((slam_scale,slam_scale), 0, (slam_scale/2,slam_scale/2), 3*hurt_amt)
            self.vy = 0 
            self.falling = False
            self.jumps = 2
        elif self.y < self.floor :
            self.vy = max(-50,self.vy - 50 * tick) # gravity
            self.falling = True
        
        if (self.hqx<(self.x - tick * 12 * self.vx)<720-self.hqx):
            self.vx -= tick * 12 * self.vx
        else:
            self.vx = -self.vx
        
        if self.y - self.vy < 0:
            self.vy = - self.vy * .5
        
        self.y -= self.vy
        self.x -= self.vx

        self.x = max(min(self.x, 720-self.hqx),self.hqx)
        self.y = max(self.y,0-self.hqy)
        
        if self.vx < -1:
            self.facing = 0
        elif self.vx > 1:
            self.facing = 1
        
        mouse_pos = pygame.mouse.get_pos()

        self.rotation = math.atan2(mouse_pos[1]-self.y, mouse_pos[0]-self.x)

        self.current().update(self.local_time)
        if self.firing and self.current().auto:
            self.shoot()

    
    def render(self, surface):
        super().render(surface)
        xrot, yrot = math.cos(self.rotation) * 50 + self.x, math.sin(self.rotation) * 50 + self.y
        pygame.draw.circle(surface, (255,0,0), (xrot, yrot), 5)
    
    # utilities 

    def current(self):
        return self.Primary if self.Primary_Equiped else self.Secondary

    def bias_angle(self,start, end, angle):
        return (start <= angle <= end) if start <= end else (angle >= start or angle <= end)
    
    def div_sort(self, lst:list, item):
        pos = 0 

        for i in lst:
            if i[1] < item[1]: pos+=1
            else: break
            
        lst.insert(pos, item)
    
    def damage(self, target, amt = 0):
        if not (target): return
        target.attacked( amt * self.dmg_mul + self.dmg_bonus, self)
        if target.dead:
            self.score += target.max_health * self.score_mul + self.score_bonus
            if self.local_time - self.last_kill <= 3:
                self.kill_streak += 1
            self.last_kill = self.local_time
            self.score_bonus = self.kill_streak * 100
            self.score_mul = max(self.kill_streak / 6, 1)
            self.dmg_bonus = max(self.kill_streak * 2, 1)
            self.dmg_mul = max((self.kill_streak//3) * 2, 1)
            if self.kill_streak % 4:
                self.current().rounds += 1

        

    # abilitites


    def attacked(self, dmg=0, attacker = None):
        if self.local_time - self.gaurding <= .5:
            self.gaurding = 0
            if attacker:
                attacker.attacked(dmg/2)
            return
        self.health -= dmg
    
    def jump(self):
        if (self.local_time-self.cd_lst[2] <= 0.25) or (self.jumps <= 0): return
        self.jumps -= 1
        self.vy = 16
        self.cd_lst[2] = self.local_time
    
    def dash(self):
        if (self.local_time - self.cd_lst[1] <= 2): return
        self.vx = -math.cos(self.rotation) * 40
        self.vy = -math.sin(self.rotation) * 28
        self.cd_lst[1] = self.local_time

    def bullet(self, angle = 20, pierce = 0, knock_back = 20, recoil = 25, damage = 20):
        if not self.enemies: return

        self.vx += math.cos(self.rotation) * recoil
        self.vy += math.sin(self.rotation) * recoil
        
        rads = math.radians(angle/2)
        most, least = ((math.degrees(self.rotation+rads)+180)%360)-180,((math.degrees(self.rotation-rads)+180)%360)-180

        canidates = []
        
        for enemy in self.enemies.cache:
            for i in range(bullet_accuracy): # divisions along y axis
                agg = math.degrees(math.atan2((enemy.y-enemy.hqy) + enemy.hhy * (i/bullet_accuracy) - self.y, enemy.x - self.x))
                if self.bias_angle(least, most, agg):
                    self.div_sort(canidates,[
                        enemy ,
                        math.sqrt((self.x - enemy.x)**2 + (self.y-enemy.y)**2)
                    ])
                    break

        if len(canidates) > pierce > 0:
            canidates = canidates[:pierce]
        
        for canidate_data in canidates:
            unit, _ = canidate_data
            self.damage(unit,damage)
            unit.vx -= math.cos(self.rotation) * knock_back
            self.vy -= math.sin(self.rotation) * knock_back
                        


    def basic_attack(self, box = (120,120), pierce = 0, offset = (0,0), dmg = 20):
        if not self.enemies: return
        left, top = self.x - offset[0], self.y - offset[1]
        right, bottom = left + box[0], top + box[1]

        harmed = 0
        
        for enemy in self.enemies.cache:
            if left<enemy.x<=right and top<enemy.y<=bottom:
                if harmed >= pierce and pierce > 0: continue
                harmed+=1
                self.damage(enemy,dmg)
                enemy.vx -= max(-50, min(50, box[0]/(enemy.x-self.x) * 12))
                enemy.vy += 16
    
    def begin_shoot(self):
        self.shoot()
        self.firing = True
    
    def shoot(self):
        blicky = self.current()
        if blicky.request_fire(self.local_time):
            self.bullet(*blicky.data())
            blicky.fired(self.local_time)
     
    def end_shoot(self):
        self.firing = False

    def parry(self):
        if self.local_time - self.cd_lst[3] > 1:
            return
        self.cd_lst[3] = self.local_time
        self.gaurding = self.local_time

    def reload(self):
        current = self.Primary if self.Primary_Equiped else self.Secondary
        current.reload(self.local_time)

    def swap_primary(self):
        self.Primary_Equiped = not self.Primary_Equiped
        if self.Primary_Equiped:
            self.Primary.equiped(self.local_time)
            self.Secondary.unquiped()
        else:
            self.Secondary.equiped(self.local_time)
            self.Primary.unquiped()
        


    # shikigami


    def mahoraga(self):
        self.vx += math.cos(self.rotation) * 50
        self.vy += math.sin(self.rotation) * 20

    # passives



   