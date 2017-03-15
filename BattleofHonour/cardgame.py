import pygame
import logging
import sys
pygame.init()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = pygame.display.set_mode((800, 600))

class Controller():

    PRESTART = 1
    RUNNING = 2
    PLAYER1 = 3
    PLAYER2 = 4

    def __init__(self):
        self.events = {}
        self.keymap = {}

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE))
        pygame.display.set_caption('Battle of Honour')
        self.clock = pygame.time.Clock()
        self.world = World(self)
        self.card = Card(self)

        self.game_state = Controller.PRESTART

        #draw 5 cards to both players

    def run(self):
        self.game_state = Controller.RUNNING

        while True:
            pygame.display.flip()
            #Handling all events
            for event in pygame.event.get():
                logger.debug('handling event {}'.format(event))

                if event_type == pygame_

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

    def quit(self, event):
        logger.info('Quitting... Good bye!')
        pygame.quit()
        sys.exit()

    def register_eventhandler(self, event_type, callback):
        logger.debug('Registrering event handler ({}, {})'.format(event_type, callback))
        if self.events.get(event_type):
            self.events[event_type].append(callback)
        else:
            self.events[event_type] = [callback]

    def register_key(self, key, callback):
        logger.debug('Binding key {} to {}.'.format(key, callback))
        if self.keymap.get(key):
            self.keymap[key].append(callback)
        else:
            self.keymap[key] = [callback]

class Card():
    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.screen

        self.controller.register_eventhandler(pygame.KEYDOWN, self.keydown)
        self.controller.register_eventhandler(pygame.KEYUP, self.keyup)

        self.colors = {'background': pygame.Color(''),
                       'text': pygame.Color('')}

    def draw(self):
        surface = pygame.Surface((200,150), flags=pygame.SRCALPHA)
        surface.fill(self.colors['background'], (100, 100, 75, 75 ))
