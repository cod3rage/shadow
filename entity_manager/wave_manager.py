import random
from . import entities, ai_entity
from .waves import *


class Manager():
    def __init__(self, group):
        self.wave = -1 
        self.local_time = 0
        self.spawned = 0
        self.cached_wave = {}
        self.end = 0 
        self.start = 0
        self.group = group
        self.multiplier = 1
    
    def update(self, tick):
        start_tick = self.local_time
        self.local_time += tick
        local_spawns = self.end + self.start
        if self.spawned == 0 and local_spawns <= self.local_time:
            self.wave += 1
            self.cached_wave = self.compile_wave()
            self.start = self.local_time
        else:
            for local_tick, compiled in self.cached_wave.items():
                if start_tick < local_tick + self.start<= self.local_time:
                    for spawn_info in compiled: # idk any other way todo it
                        for _ in range(spawn_info[1]):
                            pos = (random.randint(0,1) * 620 + 50, 0)
                            spawned = None
                            if spawn_info[0] == 'Transfigured': self.group.new(ai_entity.Transfigured(pos))
                            elif spawn_info[0] == 'JoGoat': self.group.new(ai_entity.JoGoat(pos))
                            elif spawn_info[0] == 'Vengful': self.group.new(ai_entity.Vengful(pos))
                            elif spawn_info[0] == 'Thunder': self.group.new(ai_entity.Thunder(pos))
                            elif spawn_info[0] == 'BigRaga': self.group.new(ai_entity.BigRaga(pos))
                            if not spawned: continue
                            spawned.max_health *= self.multiplier
                            spawned.health *= self.multiplier
                            spawned.damage *= self.multiplier

            self.spawned = len(self.group.cache)
            
    
    def interval(self):
        pass

    def compile_wave(self):
        self.wave = max(0, round(self.wave))
        self.multiplier = max(self.wave / len(set_waves), 1)
        cycle = self.wave%len(set_waves)
        data = set_waves[cycle]

        compiled , endtime = {}, 12

        for set_data in data:
            for num in range(set_data[1]):
                comp_time = set_data[3] + set_data[2] * num
                endtime = endtime if endtime > comp_time else comp_time
                for lo_time , lo_data in compiled.items():
                    if abs(lo_time - comp_time) <= 1/60:
                        for lst in lo_data:
                            if set_data[0] == lst[0]:
                                lst[1] += 1
                                break
                        else:
                            lo_data.append([set_data[0], round(self.multiplier)])
                        break
                else:
                    compiled[comp_time] = [[set_data[0], round(self.multiplier)]]
        
        self.end = endtime
        
        return compiled
            
        

        
        

