import pygame
import logging
import sys
from random import shuffle

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCREEN_SIZE = (1920, 1080)


class Controller():

    INIT = 1
    PRESTART = 2
    RUNNING = 3
    PLAYER1 = 4
    PLAYER2 = 5

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

            # INIT game ----------------------------------------
            if self.game_state == Controller.INIT:
#                self.cards = [Card(self, 'diamond')]
                self.deck = Deck(self)
                self.board = Board(self, self.deck)

                # Create new players

                self.game_state = Controller.RUNNING



            # Draw everything on screen ------------------------
            if self.game_state == Controller.RUNNING:
                self.board.draw()
                # Draw player hands

                #for card in self.market:
                #    board.draw()
#                for card in self.cards:
#                    card.draw(200, 400)


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
    VALID_CARD_TYPES = ('diamond', 'gold', 'silver','spice', 'cloth', 'leather', 'camel',)
    IMAGEScard = {
        'diamond': pygame.image.load('JaipurImages/diamond.png'),
        'gold': pygame.image.load('JaipurImages/gold.png'),
        'silver': pygame.image.load('JaipurImages/silver.png'),
        'spice': pygame.image.load('JaipurImages/spice.png'),
        'cloth': pygame.image.load('JaipurImages/cloth.png'),
        'leather': pygame.image.load('JaipurImages/leather.png'),
        'camel': pygame.image.load('JaipurImages/camel.png'),
        'backside': pygame.image.load('JaipurImages/backside.png')
        }

    def __init__(self, controller, card_type):

        self.card_type = ''  # We want to handle this later...
        self.controller = controller
        self.screen = controller.screen

        self.controller.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.mousedown)
        self.controller.register_eventhandler(pygame.MOUSEBUTTONUP, self.mouseup)

        self.latest_known_position = None

        if not card_type in Card.VALID_CARD_TYPES:
            raise ValueError('Invalid card type')  # Not that Pythonic but helpful (this time at least).

        self.card_type = card_type

        # Generate card image
        surface = pygame.Surface((174, 241), flags=pygame.SRCALPHA)
#        self.surface.fill(pygame.Color('#FFFFFF'), (0, 0, 174, 241))

#        text = self.controller.font.render(self.card_type, 1, pygame.Color('#000000'))
#        self.surface.blit(text, ((self.surface.get_width() - text.get_width()) / 2, 34))
        surface.blit(Card.IMAGEScard[self.card_type].convert_alpha(), (0, 0))
        self.surface = surface



    def update(self):
        pass


    def draw(self, x, y):
        self.latest_known_position = (x, y)
        logger.debug('setting value {}, {}'.format(x,y))
        logger.debug('object id: {} -- draw'.format(id(self)))
        self.screen.blit(self.surface, (x, y))


    def mousedown(self, event):

        if not self.latest_known_position is None:
            if event.button == 1:
                logger.debug('object id: {} -- mousedown'.format(id(self)))
                x, y = self.latest_known_position

                if event.pos[0] > x and event.pos[0] < x + 57 and \
                        event.pos[1] > y and event.pos[1] < y + 81:
                    # Click on us.
                    logger.debug('Clicked on card!')

    def mouseup(self, event):
        logger.debug('Mouse up on card {}'.format(self))


    def __eq__(self, other):
        return self.card_type == other.card_type


    def __repr__(self):
        return '<Card: {} (0x{:x})>'.format(self.card_type, id(self))


#Rita upp kort!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class Coin():
        VALID_COIN_TYPES = ('diamond', 'gold', 'silver','spice', 'cloth', 'leather', 'camel',)
        IMAGEScoin = {
            'gold': pygame.image.load('JaipurImages/goldcoin.png'),
            'silver': pygame.image.load('JaipurImages/silvercoin.png'),
            'spice': pygame.image.load('JaipurImages/spicecoin.png'),
            'cloth': pygame.image.load('JaipurImages/clothcoin.png'),
            'leather': pygame.image.load('JaipurImages/leathercoin.png'),
            'camel': pygame.image.load('JaipurImages/camelcoin.png'),
            'diamond': pygame.image.load('JaipurImages/diamondcoin.png'),
            'backside': pygame.image.load('JaipurImages/backsidecoin.png')

            }

        def __init__(self, controller, card_type):

            self.coin_type = ''  # We want to handle this later...
            self.controller = controller
            self.screen = controller.screen

            self.controller.register_eventhandler(pygame.MOUSEBUTTONDOWN, self.mousedown)
            self.controller.register_eventhandler(pygame.MOUSEBUTTONUP, self.mouseup)

            if not coin_type in Coin.VALID_COIN_TYPES:
                raise ValueError('Invalid card type')  # Not that Pythonic but helpful (this time at least).

            self.coin_type = coin_type

            # Generate card image
            surface = pygame.Surface((116, 116), flags=pygame.SRCALPHA)
    #        self.surface.fill(pygame.Color('#FFFFFF'), (0, 0, 174, 241))

    #        text = self.controller.font.render(self.card_type, 1, pygame.Color('#000000'))
    #        self.surface.blit(text, ((self.surface.get_width() - text.get_width()) / 2, 34))
            surface.blit(Coin.IMAGEScoin[self.coin_type].convert_alpha(), (0, 0))
            self.surface = surface


        def update(self):
            pass


        def draw(self, x, y):
            self.latest_known_position = (x, y)
            self.screen.blit(self.surface, (x, y))


        @staticmethod
        def draw_specific_coin(coin_type, screen, x, y):
            screen.blit(Coin.IMAGEScoin[coin_type], (x, y))


        def mousedown(self, event):
            if event.button == 1:
                x, y = self.latest_known_position

                if event.pos[0] > x and event.pos[0] < x + 57 and \
                        event.pos[1] > y and event.pos[1] < y + 81:
                    # Click on us.
                    logger.debug('Clicked on card!')

        def mouseup(self, event):
            logger.debug('Mouse up on card {}'.format(self))


        def __eq__(self, other):
            return self.coin_type == other.coin_type


        def __repr__(self):
            return '<Card: {} (0x{:x})>'.format(self.card_type, id(self))

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
        self.reverse = pygame.Surface((174, 241))

        self._cards = [Card(self.controller, t) for t in Deck.DEFAULT_CARD_LIST]
        shuffle(self._cards)


    def draw(self):
        self.card.draw(x ,y)

    @staticmethod
    def draw_reverseside(screen, x, y):
        screen.blit(Card.IMAGEScard['backside'], (x, y))

    def draw_backside(possx, possy, self):
        self.reverse.blit(Card.IMAGEScard['backside'], (0,0))


    def draw_card(self):
        return self._cards.pop()


    def draw_card_of_type(self, card_type):
        index = 0
        for c in self._cards:
            if c.card_type == card_type:
                return self._cards.pop(index)
            index += 1
        return None

    def __repr__(self):
        return '<Deck: 0x{:x}>'.format(id(self))



class Board():
    def __init__(self, controller, deck):
        self.controller = controller
        self.screen = controller.screen

        self.deck = deck

        self.market = []
        self.market.append(self.deck.draw_card_of_type('camel'))
        self.market.append(self.deck.draw_card_of_type('camel'))
        self.market.append(self.deck.draw_card_of_type('camel'))
        self.market.append(self.deck.draw_card())
        self.market.append(self.deck.draw_card())

        self.pointbrick = []
        self.pointbrick.append(self.deck.draw_card_of_type('diamond'))
        self.pointbrick.append(self.deck.draw_card_of_type('gold'))
        self.pointbrick.append(self.deck.draw_card_of_type('silver'))
        self.pointbrick.append(self.deck.draw_card_of_type('cloth'))
        self.pointbrick.append(self.deck.draw_card_of_type('spice'))
        self.pointbrick.append(self.deck.draw_card_of_type('leather'))
        self.pointbrick.append(self.deck.draw_card_of_type('camel'))

        self.reversebackside = []
        self.reversebackside.append(self.deck.draw_card())
        self.reversebackside.append(self.deck.draw_card())
        self.reversebackside.append(self.deck.draw_card())


    def start_draw(self, card):
    #    player1.c = 0
    #    player2.c = 0
    #    if player.turn = 0:
        pass


    def take_from_market(self, market):
        while turn == PLAYER1:
            pass

    def trade_from_market(self, market):
        pass

    def draw(self):

    #    pygame.draw.circle(self.screen, (255,255,255), (posx, posy), 50)
    #    self.screen.blit(pygame.Surface(posx, posy), (0, 0))
        posy, posx = 20, 70
        for coin_type in Coin.VALID_COIN_TYPES:
            Coin.draw_specific_coin(coin_type, self.screen, posx, posy)
            posy += 115

        possx, possy = 1530, 340
        for card in self.reversebackside:
            Deck.draw_reverseside(self.screen, possx, possy)
        #    self.deck.draw_backside(possx, possy)
            possx += 15

        x, y = 300, 340
        for card in self.market:
            card.draw(x, y)
            x += 240


    # Vad behöver representeras?
    # - håll reda på en instans av Deck.
    # - ett antal kort som spelarna kan ta av (market), initieras med tre kameler och två slumpade kort. lista?
    # - poängpott, representation?
    # - två spelare?

    # - draw-metod
    # - take_from_market-metod?
    # - draw_from_deck-metod?
    # - trade_cards-metod?
    # Poängräkning i Board eller Player?


if __name__ == "__main__":
    c = Controller()
    c.run()
