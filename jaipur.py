import pygame
import logging
import sys
from random import shuffle, randint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (800, 600)

PLAYFIELDCOLOR = [pygame.Color('#000000'), pygame.Color('#75646A')]

SHAPESCOLOR = {1: pygame.Color('#A36D7F'),
               2: pygame.Color('#A37F6D'),
               3: pygame.Color('#7FA36D'),
               10: pygame.Color('#FFFFFF')}

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
                self.playfield = Playfield(self)
                self.geoforms = Geoforms(self)
                self.game_state = Controller.RUNNING
                # self.matrix = self.playfield.reset()

            if self.game_state == Controller.RUNNING:
                self.playfield.tick()
                self.geoforms.tick()


            # Draw everything on screen ------------------------
            if self.game_state == Controller.INIT:
                pass

            if self.game_state == Controller.RUNNING:
                self.playfield.draw()
                self.playfield.stopped_shapes()
                self.geoforms.draw()
#                self.geoforms.update()

            pygame.display.flip()
            self.clock.tick(10)


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

    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.screen
        self.x = 4
        self.y = 10

        self.playfield_position = (SCREEN_SIZE[0] / 2  - 300 / 2,
                                   SCREEN_SIZE[1] / 2 - 600 / 2)
        self.num_ticks = 0
        self.geoform = Geoforms._generate_shape()

    @staticmethod
    def _generate_shape():
        forms = {'T': [[0, 1], [-1, 0], [0, 0], [1, 0]],
                      'I': [[1, 0], [0, 0], [2, 0], [-1, 0]],
                      'H': [[1, 0], [0, 1], [1, 1], [0, 0]],
                      'Z': [[0, 1], [0, 0], [1, 0], [1, -1]],
                      'L': [[0, 0], [1, 0], [0, 1], [0, 2]]}
        dic = {1: 'T',
               2: 'I',
               3: 'H',
               4: 'Z',
               5: 'L'}
        num = randint(1,5)
        return forms[dic[num]]

    def draw(self):
        surface = pygame.Surface((300, 600), pygame.SRCALPHA)

        for xo, yo in self.geoform:
            pygame.draw.rect(surface,
                             SHAPESCOLOR[2],
                             (30 * (self.x + xo) + 2, 30 * (19 - (self.y + yo)) + 2, 26, 26))


        self.screen.blit(surface, self.playfield_position)

    def tick(self):
        self.num_ticks = self.num_ticks + 1 if self.num_ticks < 10 else 0

        if self.num_ticks == 0:
            if self.valid_move():
                self.y -= 1
            else:
                self.controller.playfield.shape = self.geoform
                logger.debug(self.controller.playfield.shape)
                self.controller.playfield.shapes_S[(self.x, self.y)] = self.geoform
                self.geoform = Geoforms._generate_shape()
                #logger.debug('X Value: ' '{}', 'Y Value: ' '{}'.format(self.x, self.y))
                self.y = 19
                self.x = 4


    def valid_move(self):
        for xo, yo in self.geoform:
            if self.controller.playfield.matrix[self.y + yo - 1][self.x + xo - 1] != 0:
                return False
        return True

    def mouseup(self, event):
        logger.debug('Mouse up on card {}'.format(self))

class Playfield():
    def __init__(self, controller):
        self.playfield_position = (SCREEN_SIZE[0] / 2  - 300 / 2,
                                   SCREEN_SIZE[1] / 2 - 600 / 2)
        self.controller = controller
        self.shapex = 0
        self.shapey = 0
        self.screen = self.controller.screen
        self.matrix = [[0 for x in range(10)] for y in range(20)]
        self.shape = 0
        self.shapes_S = {}

        #Test shape ---->
        self.matrix[0][3] = 3
        self.matrix[0][4] = 3
        self.matrix[0][5] = 3
        self.matrix[1][4] = 3

        logger.debug(self.matrix)
    def draw(self):
        surface = pygame.Surface((300, 600))
        surface.fill(PLAYFIELDCOLOR[1])

        self.screen.blit(surface, (self.playfield_position))


    def tick(self):
        if bool(self.shapes_S):
            logger.debug('self.shapes is not empty')
            for key, value in self.shapes_S.items():
                self.shapey = key[1]
                self.shapex = key[0]
                for xo, yo in value:
                    self.matrix[key[0] + xo][key[1] + yo] = 1
                    logger.debug((xo, yo))
                logger.debug((key[0], key[1]))
            logger.debug(self.matrix)
            self.shapes_S = {}

    def stopped_shapes(self):
        surface = pygame.Surface((300, 600), pygame.SRCALPHA)
        for row in range(20):
            for column in range(10):
                #unknown error after first shape
                if self.matrix[row][column] > 0:
                    pygame.draw.rect(surface,
                    SHAPESCOLOR[1],
                    (30 * (column) + 2, 30 * (19 - (row)) + 2, 26, 26))
                    self.screen.blit(surface, (self.playfield_position))

if __name__ == "__main__":
    c = Controller()
    c.run()
