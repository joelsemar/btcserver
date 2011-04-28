CARD_VALUES = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
CARD_SUITES = ['spades', 'hearts', 'clubs', 'diamonds']

CARD_CHOICES = [('%s of %s' % (value, suite), '%s of %s' % (value.title(), suite.title())) \
                 for suite in CARD_SUITES for value in CARD_VALUES]




NUM_SEATS = 5
HAND_TYPE_CHOICES = (('blackjack', 'Black Jack'), ('holdem', 'Texas Hold em'))