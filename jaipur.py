import pygame
import logging
import sys
from random import shuffle

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (800, 600)


class Controller():

    INIT = 1
    RUNNING = 2
    PLAYER1 = 3
    PLAYER2 = 4

    def __init__(self):
        self.events = {}
        self.keymap = {}

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('jaipur')
        self.clock = pygame.time.Clock()

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

            # INIT game ----------------------------------------
            if self.game_state == Controller.INIT:
                self.cards = [Card(self, 'diamond')]
                self.game_state = Controller.RUNNING



            # Draw everything on screen ------------------------
            if self.game_state == Controller.RUNNING:
                for card in self.cards:
                    card.draw(200, 400)


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


class Card():
    VALID_CARD_TYPES = ['diamond', 'gold', 'silver','spice', 'cloth', 'leather', 'camel']

    def __init__(self, controller, card_type):

        self.card_type = ''  # We want to handle this later...
        self.controller = controller
        self.screen = controller.screen

        self.controller.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.mousedown)
        self.controller.register_eventhandler(pygame.MOUSEBUTTONUP, self.mouseup)

        if not card_type in Card.VALID_CARD_TYPES:
            raise ValueError('Invalid card type')  # Not that Pythonic but helpful (this time at least).

        self.card_type = card_type

        self.surface = pygame.Surface((57, 81))
        self.surface.fill(pygame.Color('#FFFFFF'), (0, 0, 57, 8))

        IMAGEDICT = {'diamond': pygame.image.load('JaipurImages/diamond.png'),
                    'gold': pygame.image.load('JaipurImages/gold.png'),
                    'silver': pygame.image.load('JaipurImages/silver.png'),
                    'spice': pygame.image.load('JaipurImages/spice.png'),
                    'cloth': pygame.image.load('JaipurImages/cloth.png'),
                    'leather': pygame.image.load('JaipurImages/leather.png'),
                    'camel': pygame.image.load('JaipurImages/camel.png')}


    def update(self):
        pass

    def draw(self, x, y):
        surface = pygame.Surface(SCREEN_SIZE)
        self.latest_known_position = (x, y)
        self.screen.blit(surface, (0,0))


    def mousedown(self, event):
        logger.debug('Mouse down on card {}'.format(self))

    def mouseup(self, event):
        logger.debug('Mouse up on card {}'.format(self))


    def __eq__(self, other):
        return self.card_type == other.card_type


    def __repr__(self):
        return '<Card: {} (0x{:x})>'.format(self.card_type, id(self))


#Rita upp kort!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Deck():
    DEFAULT_CARD_LIST = ['diamond'] * 6 + \
                        ['gold'] * 6 + \
                        ['silver'] * 6 + \
                        ['cloth'] * 8 + \
                        ['spice'] * 8 + \
                        ['leather'] * 10 + \
                        ['camel'] * 11

    def __init__(self, controller, card_list = ''):
        self.controller = controller
        self.screen = controller.screen

        self._cards = [Card(self.controller, t) for t in Deck.DEFAULT_CARD_LIST]
        shuffle(self._cards)


    def draw(self):
        surface = pygame.Surface(SCREEN_SIZE)
        surface.fill(pygame.color('#000000'), (150,150,50,100))
        self.screen.blit(surface, (0,0))
        return self._cards.pop()

    def __repr__(self):
        return '<Deck: 0x{:x}>'.format(id(self))


if __name__ == "__main__":
    c = Controller()
    c.run()
