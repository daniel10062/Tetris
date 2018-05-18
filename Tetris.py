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
               4: pygame.Color('#FFFFFF'),
               5: pygame.Color('#009898'),
               6: pygame.Color('#0C9837'),
               7: pygame.Color('#FFFFFF')}

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

                if self.game_state == Controller.RUNNING:
                    #self.playfield.tick()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    x, y = geoform.x, geoform.y
                    for i in range(18):
                        for xo, yo in geoform:
                            if self.playfield.matrix[y + yo - i][x + xo] != 0 or y + yo == 0
                                self.playfield.matrix[y + yo][x + xo] = geoform.color 

                    if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                        self.geoforms.y = self.geoforms.y - 1
                        if self.geoforms.N_formY != None:
                            self.geoforms.N_formY -= 1

                    if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                        if not self.geoforms.x == 8:
                            self.geoforms.x += 1
                            if self.geoforms.N_formY != None:
                                self.geoforms.N_formY -= 1

                    if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                         if not self.geoforms.x == 1:
                             self.geoforms.x -= 1
                             if self.geoforms.N_formY != None:
                                 self.geoforms.N_formY -= 1

                    if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                        self.playfield.valid_form = self.playfield.valid_form + 1
                        if self.playfield.valid_form > 4:
                            self.playfield.valid_form = 1
                        self.update_form()
                        logger.debug('Number {}'.format(self.playfield.valid_form))


            # Update state ----------------------------------------
            if self.game_state == Controller.INIT:
#                //PRELOADEBLE STUFF
                self.playfield = Playfield(self)
                self.geoforms = Geoforms(self)
                self.game_state = Controller.RUNNING
                # self.matrix = self.playfield.reset()

            if self.game_state == Controller.RUNNING:

                self.geoforms.tick()


            # Draw everything on screen ------------------------
            if self.game_state == Controller.INIT:
                pass

            if self.game_state == Controller.RUNNING:
                self.playfield.draw()
#                self.playfield.stopped_shapes()
                self.geoforms.draw()
#                self.geoforms.update()

            pygame.display.flip()
            self.clock.tick(10)


    def quit(self, event):
        logger.info('Quitting... Good bye!')
        pygame.quit()
        sys.exit()

    def register_eventhandler(self, event_type, callback):
        #logger.debug('Registrering event handler ({}, {})'.format(event_type, callback))
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

    def update_form(self):
        self.geoforms.formupdate(self.geoforms)

    def next_geoform(self):
        self.playfield.add_shape(self.geoforms)
        self.geoforms = Geoforms(self)


class Geoforms():
    #1 #
       # #
       #

    #2 #
       #
       #
       #

    #3  # #
      # #

    #4 # #
       # #

    #5 # #
         # #

    #6 #
       # # #

    #7    #
      # # #

    SHAPES_D = [[[0, 1], [-1, 0], [0, 0], [1, 0]],
              [[1, 0], [0, 0], [2, 0], [-1, 0]],
              [[-1, 0], [1, 1], [0, 1], [0, 0]],
              [[0, 1], [0, 0], [1, 1], [1, 0]],
              [[0, 0], [0, 1], [-1, 1], [1, 0]],
              [[0,0], [0,1], [1,0], [2,0]],
              [[0,0], [1,0], [-1,0], [1, 1]]]

    SHAPES_L = [[[0, 0], [1, 0], [0, -1], [0, 1]],
              [[0, 2], [0, 0], [0, -1], [0, 1]],
              [[0, 0], [1, 0], [0, 1], [1, -1]],
              [[0, 1], [0, 0], [1, 1], [1, 0]],
              [[0, 0], [1, 0], [0, -1], [1, 1]],
              [[0,0], [1,0], [0,-1], [0,-2]],
              [[0,0], [0,1], [0,2], [1,0]]]


    SHAPES_U = [[[0, 0], [-1, 0], [1, 0], [0, -1]],
              [[1, 0], [0, 0], [2, 0], [-1, 0]],
              [[-1, 0], [1, 1], [0, 1], [0, 0]],
              [[0, 1], [0, 0], [1, 1], [1, 0]],
              [[0, 0], [0, 1], [-1, 1], [1, 0]],
              [[0,0], [-1, 0], [1,0], [1,-1]],
              [[0,0], [-1,0], [1,0], [-1,-1]]]

    SHAPES_R = [[[0, 0], [-1, 0], [0, 1], [0, -1]],
              [[0, 2], [0, 0], [0, -1], [0, 1]],
              [[0, 0], [1, 0], [0, 1], [1, -1]],
              [[0, 1], [0, 0], [1, 1], [1, 0]],
              [[0, 0], [1, 0], [0, -1], [1, 1]],
              [[0,0], [-1, 0], [0,1], [0,2]],
              [[0,0], [0,1], [0,-1], [-1,-1]]]

    SHAPES = {1: SHAPES_D,
              2: SHAPES_L,
              3: SHAPES_U,
              4: SHAPES_R}

    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.screen
        self.x = 4
        self.y = 19
        self.N_formX = None
        self.N_formY = None
        self.playfield_position = (SCREEN_SIZE[0] / 2  - 300 / 2,
                                   SCREEN_SIZE[1] / 2 - 600 / 2)
        self.num_ticks = 0
        self.geoform, self.color = Geoforms._generate_shape(self.controller, None)
        logger.debug('Generate geoform with shape: {}'.format(self.geoform))


    @staticmethod
    def _generate_shape(controller, num):
        # if controller.playfield.index == None:
        #     i = randint(1, len(Geoforms.SHAPES[controller.playfield.valid_form]))
        #     controller.playfield.index = i
        # else:
        #     i = controller.playfield.index

        if num:
            i = num
        else:
            i = randint(1, len(Geoforms.SHAPES[controller.playfield.valid_form]))
        logger.debug(controller.playfield.valid_form)
        return Geoforms.SHAPES[controller.playfield.valid_form][i - 1], i  # Shape and color

    def formupdate(self, geoform):
        self.N_formX, self.N_formY = geoform.x, geoform.y
        color = geoform.color
        self.geoform, self.color = Geoforms._generate_shape(self.controller, color)

    def draw(self):
        #logger.debug(('color: 'self.color, 'valid_form: 'self.controller.playfield.valid_form, 'index: 'self.controller.playfield.index, self.N_formX, self.N_formY))
        logger.debug('Color: {}'.format(self.color))
        logger.debug((self.x, self.y))
        if self.N_formX and self.N_formY != None:
            self.x, self.y = self.N_formX, self.N_formY
        surface = pygame.Surface((300, 600), pygame.SRCALPHA)

        for xo, yo in self.geoform:
            pygame.draw.rect(surface,
                             SHAPESCOLOR[self.color],
                             (30 * (self.x + xo) + 2, 30 * (19 - (self.y + yo)) + 2, 26, 26))


        self.screen.blit(surface, self.playfield_position)


    def tick(self):
        self.num_ticks = self.num_ticks + 1 if self.num_ticks < 10 else 0

        if self.num_ticks == 0:
            if self.valid_move():
                self.y -= 1
                if (self.N_formY != None):
                    self.N_formY -= 1
            else:
                logger.debug(self.controller.playfield.shape)
                self.controller.playfield.index = None
                self.controller.next_geoform()

    def valid_move(self):
        for xo, yo in self.geoform:
            if self.controller.playfield.matrix[self.y + yo - 1][self.x + xo] != 0 or self.y + yo == 0:
                if self.check_end():
                    logger.info('You lost!')
                    pygame.quit()
                    sys.exit()
                return False
        return True

    def check_end(self):
        for xo, yo in self.geoform:
            if yo + self.y == 19:
                return True
        return False

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
        self.matrix = [[0 for x in range(10)] for y in range(22)]
        self.shape = 0
        self.shapes_S = {}
        self.valid_form = 1
        self.color = None
        self.index = None

        #Test shape ---->
        # self.matrix[0][3] = 1
        # self.matrix[0][4] = 1
        # self.matrix[0][5] = 1
        # self.matrix[1][4] = 1

        logger.debug(self.matrix)


    def draw(self):
        surface = pygame.Surface((300, 600))
        surface.fill(PLAYFIELDCOLOR[1])

        for row in range(20):
            for column in range(10):
                #unknown error after first shape
                if self.matrix[row][column] > 0:
                    pygame.draw.rect(surface,
                    SHAPESCOLOR[self.matrix[row][column]],
                    (30 * (column) + 2, 30 * (19 - (row)) + 2, 26, 26))
#                    self.screen.blit(surface, (self.playfield_position))

        self.screen.blit(surface, (self.playfield_position))


    def tick(self):
        pass


    def add_shape(self, geoform):
        x, y = geoform.x, geoform.y
        color = geoform.color
        for xo, yo in geoform.geoform:
            self.matrix[y + yo][x + xo] = color

#    def stopped_shapes(self):
#        surface = pygame.Surface((300, 600), pygame.SRCALPHA)

if __name__ == "__main__":
    c = Controller()
    c.run()
