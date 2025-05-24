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
            basic_ai = ai_entity.ground_ai((60,90), (random.randint(0,720),0), atk_int=2)
            basic_ai.target = self.player
            self.enemies_forces.new(basic_ai)
        
        self.player.enemies = self.enemies_forces
        self.allied_forces.enemies = self.enemies_forces
        self.enemies_forces.enemies = self.allied_forces


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
            self.cycle_tick = (self.cycle_tick+1)%120
            self.local_time+=self.tick

            pygame.display.set_caption(str(self.clock.get_fps()//1))



    # processes
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.jump(self.local_time)
                if event.key == pygame.K_q:
                    self.player.dash(self.local_time)
                if event.key == pygame.K_g:
                    self.player.charge()
                if event.key == pygame.K_r:
                    self.player.shadow()
                if event.key == pygame.K_1:
                    self.player.rabbits()
                if event.key == pygame.K_2:
                    self.player.frog()
                if event.key == pygame.K_3:
                    self.player.nue()
                if event.key == pygame.K_e:
                    self.player.mahoraga()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    self.player.end_charge()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.shoot()
                if event.button == 3:
                    self.player.block()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.player.unblock()
            
        
        pressed = pygame.key.get_pressed()
        movement = (pressed[pygame.K_a] - pressed[pygame.K_d])
        self.player.x -= movement * 12
        self.player.vx += movement

    def update(self):
        self.enemies_forces.update(self.tick)
        self.allied_forces.update(self.tick)
        if self.cycle_tick == 0:
            self.allied_forces.retarget()
            self.enemies_forces.retarget()

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