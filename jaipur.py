import pygame
import logging
import sys
from random import shuffle

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (800, 600)

PLAYFIELDCOLOR = [pygame.Color('#000000'), pygame.Color('#75646A')]

SHAPESCOLOR = {1: pygame.Color('#A36D7F'),
               2: pygame.Color('#A37F6D'),
               3: pygame.Color('#7FA36D'),}

class Controller():

    INIT = 1
    RUNNING = 2

    def __init__(self):
        self.events = {}
        self.keymap = {}

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('jaipur')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("fonts/roboto/Roboto-Regular.ttf", 14)


        self.register_eventhandler(pygame.QUIT, self.quit)
        self.register_key(pygame.K_ESCAPE, self.quit)
        self.game_state = Controller.INIT

        #draw 5 cards to both players

    def run(self):
        self.game_state = Controller.INIT

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

            # Update state ----------------------------------------
            if self.game_state == Controller.INIT:
#                //PRELOADEBLE STUFF
                self.playfield = Playfield(self.screen)
                self.game_state = Controller.RUNNING
                # self.matrix = self.playfield.reset()

            if self.game_state == Controller.RUNNING:
                self.playfield.tick()


            # Draw everything on screen ------------------------
            if self.game_state == Controller.INIT:
                pass

            if self.game_state == Controller.RUNNING:
                self.playfield.draw()
#                self.geoforms.draw()
#                self.geoforms.update()

            pygame.display.flip()
            self.clock.tick(5)


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


class Geoforms():

    def __init__(self, screen):
        self.screen = screen
        self.yspeed = -1
        self.x = self.screen.get_width() / 2

    def hit(self, screen):
        # Check if geoforms is hitting the floor or the edge
        pass


    def update(self):
        pass

    def draw(self):
        surface = pygame.Surface((self.x, self.screen.get_height()))
        pygame.draw.rect(surface, SHAPESCOLOR[1], (0, 0, self.x, 10))
        self.screen.blit(surface, (self.x, 0))
    #Make KEYARROW events

    def mouseup(self, event):
        logger.debug('Mouse up on card {}'.format(self))

class Playfield():
    def __init__(self, screen):
        self.screen = screen
        self.winx = SCREEN_SIZE[0] / 2 - 150
        self.winy = SCREEN_SIZE[1] / 2 - 300

        self.reset()

        self.rectangle()
    def longShape(self):

        self.matrix[19][3] = 2
        self.matrix[19][4] = 2
        self.matrix[19][5] = 2
        self.matrix[19][6] = 2

    def rectangle(self):
        self.matrix[18][3] = 1
        self.matrix[18][4] = 1
        self.matrix[18][5] = 1
        self.matrix[19][4] = 1

    def reset(self):
        self.matrix = [[0 for x in range(10)] for y in range(20)]

    def tick(self):
        for row in range(20):
            for column in range(10):
                if self.matrix[row][column] > 0:
                    if row == 0 or self.matrix[row - 1][column] == 1:
                        self.longShape()
                        break
                    else:
                        self.matrix[row - 1][column] = 1
                        self.matrix[row][column] = 0
    def draw(self):
        surface = pygame.Surface((300, 600))
        surface.fill(PLAYFIELDCOLOR[1])

        for row in range(20):
            for column in range(10):
                logger.debug('({}, {}): {}'.format(row, column, self.matrix[row][column]))
                if self.matrix[row][column] > 0:
                    rect = (column * 30, -1 * (row - 19) * 30, 29, 29)
                    logger.debug(rect)
                    pygame.draw.rect(surface, SHAPESCOLOR[self.matrix[row][column]], rect)

        self.screen.blit(surface, (self.winx, self.winy))


if __name__ == "__main__":
    c = Controller()
    c.run()
