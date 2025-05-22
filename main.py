import pygame
import random
from services import entities

class App:
    def __init__(self):
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode((720, 720))

        self.local_time = 0
        self.tick = 0
        self.clock = pygame.time.Clock()

        self.scroll = []

        self.player = entities.Player()

        for _ in range(200):
            entities.Enemy((random.randint(40,120),random.randint(40,120)),spd=random.randint(15, 120))


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
            self.local_time+=self.tick


    # processes
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.vy = max(12,self.player.vy+12)
        
        pressed = pygame.key.get_pressed()
        self.player.vx = (pressed[pygame.K_a] - pressed[pygame.K_d]) * 12

    def update(self):
        entities.Update(self.tick)
        # self.wave.update(self.tick)

    def render(self):
        self.screen.fill((0,0,0))
        entities.Render(self.screen)

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