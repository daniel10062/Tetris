import pygame
import logging
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (800, 600)

class Controller():

    PRESTART = 1
    RUNNING = 2

    def __init__(self):
        self.events = {}
        self.keymap = {}

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE))
        pygame.display.set_caption('Battle of Honour')
        self.clock = pygame.time-Clock()

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit)


        self.world = World(self)
        self.clock = pygame.time.Clock()
        self.game_state = Controller.PRESTART


    def run(self):
        self.game_state = Controller.RUNNING

        while True:
            #Handling all events
            for event in pygame.event.get():
                logger.debug('handling event {}'.format(event))

                for event_type, callbacks in self.events.items():
                    if event.type == event_type:
                        for callback in callbacks:
                            callback(event)

                if event.type == pygame.KEYDOWN:
                    for key in self.keymap.keys():
                        if event.key == key:
                            for callback in self.keymap[key]:
                                callback(event)

                self.clock.tick = 15

                #Draw everything on screen -------------------------
                if self.game_state == Controller.RUNNING:
                    self.world.draw()

class World():
    def __init__(self,controller):
        self.controller = controller
        self.screen = controller.screen

    def draw(self):
        surface = pygame.Surface(SCREEN_SIZE)
        surface.fill(pygame.Color('#FFB948'), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1] - 100))

        self.screen.blit(surface, (0, 0))
