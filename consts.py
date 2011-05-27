CARD_VALUES = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
CARD_SUITES = ['spades', 'hearts', 'clubs', 'diamonds']


CARD_VALUE_CHOICES = [(c, c.title()) for c in CARD_VALUES]
CARD_SUITE_CHOICES = [(c, c.title()) for c in CARD_SUITES]


CARD_CHOICES = [('%s of %s' % (value, suite), '%s of %s' % (value.title(), suite.title())) \
                 for suite in CARD_SUITES for value in CARD_VALUES]



BLACK_JACK_CARD_VALUE_MAPPING = {'ace':11, 'two': 2, 'three': 3, 'four':4,
                                 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                                 'nine': 9}

ALT_BLACK_JACK_CARD_VALUE_MAPPING = {'ace':1, 'two': 2, 'three': 3, 'four':4,
                                     'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                                     'nine': 9}


GAME_STATE_BIDDING = 'bidding'
GAME_STATE_PLAYING = 'playing'

GAME_STATE_CHOICES = ((GAME_STATE_BIDDING, 'Bidding'), (GAME_STATE_PLAYING, 'Playing'))

NUM_SEATS = 5
HAND_TYPE_CHOICES = (('blackjack', 'Black Jack'), ('holdem', 'Texas Hold em'))
NUM_DECKS_BLACKJACK = 6
NUM_DECKS_DEFAULT = 1
NUM_CARDS_EACH_BLACKJACK = 2

CARD_DATA = [{'id': 1,
  'image_url': u'/static/images/cards/ace_spades.png',
  'name': u'Ace of Spades',
  'suite': u'spades',
  'value': u'ace'},
 {'id': 2,
  'image_url': u'/static/images/cards/two_spades.png',
  'name': u'Two of Spades',
  'suite': u'spades',
  'value': u'two'},
 {'id': 3,
  'image_url': u'/static/images/cards/three_spades.png',
  'name': u'Three of Spades',
  'suite': u'spades',
  'value': u'three'},
 {'id': 4,
  'image_url': u'/static/images/cards/four_spades.png',
  'name': u'Four of Spades',
  'suite': u'spades',
  'value': u'four'},
 {'id': 5,
  'image_url': u'/static/images/cards/five_spades.png',
  'name': u'Five of Spades',
  'suite': u'spades',
  'value': u'five'},
 {'id': 6,
  'image_url': u'/static/images/cards/six_spades.png',
  'name': u'Six of Spades',
  'suite': u'spades',
  'value': u'six'},
 {'id': 7,
  'image_url': u'/static/images/cards/seven_spades.png',
  'name': u'Seven of Spades',
  'suite': u'spades',
  'value': u'seven'},
 {'id': 8,
  'image_url': u'/static/images/cards/eight_spades.png',
  'name': u'Eight of Spades',
  'suite': u'spades',
  'value': u'eight'},
 {'id': 9,
  'image_url': u'/static/images/cards/nine_spades.png',
  'name': u'Nine of Spades',
  'suite': u'spades',
  'value': u'nine'},
 {'id': 10,
  'image_url': u'/static/images/cards/ten_spades.png',
  'name': u'Ten of Spades',
  'suite': u'spades',
  'value': u'ten'},
 {'id': 11,
  'image_url': u'/static/images/cards/jack_spades.png',
  'name': u'Jack of Spades',
  'suite': u'spades',
  'value': u'jack'},
 {'id': 12,
  'image_url': u'/static/images/cards/queen_spades.png',
  'name': u'Queen of Spades',
  'suite': u'spades',
  'value': u'queen'},
 {'id': 13,
  'image_url': u'/static/images/cards/king_spades.png',
  'name': u'King of Spades',
  'suite': u'spades',
  'value': u'king'},
 {'id': 14,
  'image_url': u'/static/images/cards/ace_hearts.png',
  'name': u'Ace of Hearts',
  'suite': u'hearts',
  'value': u'ace'},
 {'id': 15,
  'image_url': u'/static/images/cards/two_hearts.png',
  'name': u'Two of Hearts',
  'suite': u'hearts',
  'value': u'two'},
 {'id': 16,
  'image_url': u'/static/images/cards/three_hearts.png',
  'name': u'Three of Hearts',
  'suite': u'hearts',
  'value': u'three'},
 {'id': 17,
  'image_url': u'/static/images/cards/four_hearts.png',
  'name': u'Four of Hearts',
  'suite': u'hearts',
  'value': u'four'},
 {'id': 18,
  'image_url': u'/static/images/cards/five_hearts.png',
  'name': u'Five of Hearts',
  'suite': u'hearts',
  'value': u'five'},
 {'id': 19,
  'image_url': u'/static/images/cards/six_hearts.png',
  'name': u'Six of Hearts',
  'suite': u'hearts',
  'value': u'six'},
 {'id': 20,
  'image_url': u'/static/images/cards/seven_hearts.png',
  'name': u'Seven of Hearts',
  'suite': u'hearts',
  'value': u'seven'},
 {'id': 21,
  'image_url': u'/static/images/cards/eight_hearts.png',
  'name': u'Eight of Hearts',
  'suite': u'hearts',
  'value': u'eight'},
 {'id': 22,
  'image_url': u'/static/images/cards/nine_hearts.png',
  'name': u'Nine of Hearts',
  'suite': u'hearts',
  'value': u'nine'},
 {'id': 23,
  'image_url': u'/static/images/cards/ten_hearts.png',
  'name': u'Ten of Hearts',
  'suite': u'hearts',
  'value': u'ten'},
 {'id': 24,
  'image_url': u'/static/images/cards/jack_hearts.png',
  'name': u'Jack of Hearts',
  'suite': u'hearts',
  'value': u'jack'},
 {'id': 25,
  'image_url': u'/static/images/cards/queen_hearts.png',
  'name': u'Queen of Hearts',
  'suite': u'hearts',
  'value': u'queen'},
 {'id': 26,
  'image_url': u'/static/images/cards/king_hearts.png',
  'name': u'King of Hearts',
  'suite': u'hearts',
  'value': u'king'},
 {'id': 27,
  'image_url': u'/static/images/cards/ace_clubs.png',
  'name': u'Ace of Clubs',
  'suite': u'clubs',
  'value': u'ace'},
 {'id': 28,
  'image_url': u'/static/images/cards/two_clubs.png',
  'name': u'Two of Clubs',
  'suite': u'clubs',
  'value': u'two'},
 {'id': 29,
  'image_url': u'/static/images/cards/three_clubs.png',
  'name': u'Three of Clubs',
  'suite': u'clubs',
  'value': u'three'},
 {'id': 30,
  'image_url': u'/static/images/cards/four_clubs.png',
  'name': u'Four of Clubs',
  'suite': u'clubs',
  'value': u'four'},
 {'id': 31,
  'image_url': u'/static/images/cards/five_clubs.png',
  'name': u'Five of Clubs',
  'suite': u'clubs',
  'value': u'five'},
 {'id': 32,
  'image_url': u'/static/images/cards/six_clubs.png',
  'name': u'Six of Clubs',
  'suite': u'clubs',
  'value': u'six'},
 {'id': 33,
  'image_url': u'/static/images/cards/seven_clubs.png',
  'name': u'Seven of Clubs',
  'suite': u'clubs',
  'value': u'seven'},
 {'id': 34,
  'image_url': u'/static/images/cards/eight_clubs.png',
  'name': u'Eight of Clubs',
  'suite': u'clubs',
  'value': u'eight'},
 {'id': 35,
  'image_url': u'/static/images/cards/nine_clubs.png',
  'name': u'Nine of Clubs',
  'suite': u'clubs',
  'value': u'nine'},
 {'id': 36,
  'image_url': u'/static/images/cards/ten_clubs.png',
  'name': u'Ten of Clubs',
  'suite': u'clubs',
  'value': u'ten'},
 {'id': 37,
  'image_url': u'/static/images/cards/jack_clubs.png',
  'name': u'Jack of Clubs',
  'suite': u'clubs',
  'value': u'jack'},
 {'id': 38,
  'image_url': u'/static/images/cards/queen_clubs.png',
  'name': u'Queen of Clubs',
  'suite': u'clubs',
  'value': u'queen'},
 {'id': 39,
  'image_url': u'/static/images/cards/king_clubs.png',
  'name': u'King of Clubs',
  'suite': u'clubs',
  'value': u'king'},
 {'id': 40,
  'image_url': u'/static/images/cards/ace_diamonds.png',
  'name': u'Ace of Diamonds',
  'suite': u'diamonds',
  'value': u'ace'},
 {'id': 41,
  'image_url': u'/static/images/cards/two_diamonds.png',
  'name': u'Two of Diamonds',
  'suite': u'diamonds',
  'value': u'two'},
 {'id': 42,
  'image_url': u'/static/images/cards/three_diamonds.png',
  'name': u'Three of Diamonds',
  'suite': u'diamonds',
  'value': u'three'},
 {'id': 43,
  'image_url': u'/static/images/cards/four_diamonds.png',
  'name': u'Four of Diamonds',
  'suite': u'diamonds',
  'value': u'four'},
 {'id': 44,
  'image_url': u'/static/images/cards/five_diamonds.png',
  'name': u'Five of Diamonds',
  'suite': u'diamonds',
  'value': u'five'},
 {'id': 45,
  'image_url': u'/static/images/cards/six_diamonds.png',
  'name': u'Six of Diamonds',
  'suite': u'diamonds',
  'value': u'six'},
 {'id': 46,
  'image_url': u'/static/images/cards/seven_diamonds.png',
  'name': u'Seven of Diamonds',
  'suite': u'diamonds',
  'value': u'seven'},
 {'id': 47,
  'image_url': u'/static/images/cards/eight_diamonds.png',
  'name': u'Eight of Diamonds',
  'suite': u'diamonds',
  'value': u'eight'},
 {'id': 48,
  'image_url': u'/static/images/cards/nine_diamonds.png',
  'name': u'Nine of Diamonds',
  'suite': u'diamonds',
  'value': u'nine'},
 {'id': 49,
  'image_url': u'/static/images/cards/ten_diamonds.png',
  'name': u'Ten of Diamonds',
  'suite': u'diamonds',
  'value': u'ten'},
 {'id': 50,
  'image_url': u'/static/images/cards/jack_diamonds.png',
  'name': u'Jack of Diamonds',
  'suite': u'diamonds',
  'value': u'jack'},
 {'id': 51,
  'image_url': u'/static/images/cards/queen_diamonds.png',
  'name': u'Queen of Diamonds',
  'suite': u'diamonds',
  'value': u'queen'},
 {'id': 52,
  'image_url': u'/static/images/cards/king_diamonds.png',
  'name': u'King of Diamonds',
  'suite': u'diamonds',
  'value': u'king'}]

BLACKJACK_CARDS = [c for c in CARD_DATA if BLACK_JACK_CARD_VALUE_MAPPING.get(c['value'], 10) > 9]

CARD_IDS = [c['id'] for c in CARD_DATA]

BLACK_JACK_DEFAULT_AVAILABLE_ACTIONS = '["hit", "stand", "double", "surrender"]'