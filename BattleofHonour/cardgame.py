import pygame
import logging
import sys
pygame.init()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (800, 600)

class Controller():

    PRESTART = 1
    RUNNING = 2
    PLAYER1 = 3
    PLAYER2 = 4

    def __init__(self):
        self.events = {}
        self.keymap = {}

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Battle of Honour')
        self.clock = pygame.time.Clock()

        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit)

        self.world = World(self)


        self.game_state = Controller.PRESTART

        #draw 5 cards to both players

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
                #Draw everything on screen -------------------------
            if self.game_state == Controller.RUNNING:
                self.world.draw()

            pygame.display.flip()
            self.clock.tick(15)


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



class World():
    def __init__(self,controller):
        self.controller = controller
        self.screen = controller.screen

    def draw(self):
        surface = pygame.Surface(SCREEN_SIZE)
        surface.fill(pygame.Color('#FFB948'), (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

        self.screen.blit(surface, (0, 0))



if __name__ == "__main__":
    c = Controller()
    c.run()
