import pygame
import random
from entity_manager import ai_entity, entities, player

class App:
    def __init__(self):
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode((720, 720))

        self.local_time = 0
        self.tick = 0
        self.cycle_tick = 0
        self.clock = pygame.time.Clock()

        self.scroll = []

        self.player = player.Player()
        self.allied_forces = entities.EntityGroup('ally', [self.player])
        self.enemies_forces = entities.EntityGroup('enemy')

        # test allied units
        for i in range(1):
            basic_ai = ai_entity.ground_ai((60,90), (random.randint(0,720),0))
            basic_ai.target = self.player
            self.enemies_forces.new(basic_ai)


    # process organizer
    def start(self):
        self.running = True   # activates run6
        while self.running:           # runner
            if self.inputs():     # user inputs
                self.quit()
                break             # quits game if tab closed
            self.update()         # update / tick
            self.render()             # rendering objects
            pygame.display.update()   # adding render to screen
            self.tick = self.clock.tick(60)/1000
            self.cycle_tick = (self.cycle_tick+1)%60
            self.local_time+=self.tick


    # processes
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.jump(self.local_time)
        
        pressed = pygame.key.get_pressed()
        self.player.vx = (pressed[pygame.K_a] - pressed[pygame.K_d]) * 12

    def update(self):
        self.enemies_forces.update(self.tick)
        self.allied_forces.update(self.tick)

    def render(self):
        self.screen.fill((0,0,0))
        self.enemies_forces.render(self.screen)
        self.allied_forces.render(self.screen)

    # game commands
    def restart(self):
        pass
    
    def next_wave(self):
        pass

    def quit(self):
        self.running = False
        pygame.quit()


if __name__ == '__main__':
    app = App()
    app.start()