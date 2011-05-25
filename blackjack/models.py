import consts
import datetime
import time
import simplejson
from webservice_tools import utils
from django.db import models
from django.db.models import Q
from backend.models import  BaseHand, Card, Player, Table, Seat
from backend.client_connection import ClientConnection as Client
from backend import bitcoinrpc
from webservice_tools.decorators import cached_property
from decimal import *

DEFAULT_BET_TIMEOUT = 60 #in seconds
class BlackJackTableType(models.Model):
    name = models.CharField(max_length=128)
    low_bet = models.DecimalField(max_digits=12, decimal_places=8)
    high_bet = models.DecimalField(max_digits=12, decimal_places=8)
    
    
    def __unicode__(self):
        return 'Low: %.8s, High: %s' % (self.low_bet, self.high_bet)

class BlackJackTable(Table):
    type = models.ForeignKey(BlackJackTableType)
    game_state = models.CharField(max_length=32, choices=consts.GAME_STATE_CHOICES, default=consts.GAME_STATE_BIDDING)
        
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.type.low_bet, self.type.high_bet)
        
    class Meta:
        abstract = False
    
    
    def get_game_data(self):
        ret = super(BlackJackTable, self).get_game_data()
        ret['game_state'] = self.game_state
        dealer_cards = self.current_round.dealers_hand.get_cards()
        dealer_up_cards = []
        
        if self.game_state == consts.GAME_STATE_PLAYING:
            dealer_up_cards.append(Card.get_face_down())
            for card in dealer_cards[1:]:
                dealer_up_cards.append(card)
            ret['dealer_up_cards'] = dealer_up_cards
            all_hands = BlackJackHand.objects.filter(round=self.current_round, dealers_hand=False)
            for hand in all_hands:
                player = [s for s in ret['seats'] if s['player_id'] == hand.player_id][0]
                player['cards'] = hand.get_cards()
                player['available_actions'] = hand.get_available_actions()
         
        return ret
    
    @property
    def high_bet(self):
        return self.type.high_bet
    
    @property
    def low_bet(self):
        return self.type.low_bet
    
    @property
    def num_decks(self):
        return consts.NUM_DECKS_BLACKJACK
    
    
    def update_game(self):
        data = self.get_game_data()
        client = Client(data=data, table_id=self.id, action='update_game')
        client.notify()
        
    def initial_deal(self):
        hands = BlackJackHand.objects.filter(round=self.current_round).order_by('player__seat__position')
        seats = list(self.seats)
        self.current_turn = [s for s in seats if s.player_id == hands[0].player_id][0]
        for _ in range(consts.NUM_CARDS_EACH_BLACKJACK):
            for hand in hands:
                hand.add_card(self.pull_card())
                time.sleep(.3)
        
        dealer_hand = self.current_round.dealers_hand
        if dealer_hand.has_blackjack:
            self.deal_dealer_cards()
        else:
            self.game_state = consts.GAME_STATE_PLAYING
            self.save()
            self.update_game()
        
    
        
    @property
    def current_round(self):
        try:
            return BlackJackRound.objects.filter(table=self, closed=False)[0]
        except IndexError:
            None
     
    
    def save(self, *args, **kwargs):
        needs_init = False
        if not self.id:
            needs_init = True
        super(BlackJackTable, self).save(*args, **kwargs)
        if needs_init:
            self.start_new_round()
        
    def start_new_round(self):
        if self.current_round:
            self.current_round.close()
            
        round = BlackJackRound.objects.create(table=self)
        BlackJackHand.objects.create(round=round, dealers_hand=True)
                
                
    def next_turn(self):
        current_seat = self.current_turn
        try:
            self.current_turn = Seat.objects.filter(Q(position__gt=current_seat.position),
                                                    Q(table=self), ~Q(player=None),
                                                    Q(player__blackjackhand__round__id=self.current_round.id))[0]
            self.save()
            self.update_game()
        except IndexError:
            self.deal_dealer_cards()
        
    
    def deal_dealer_cards(self):
        """
        Hand is over, deal dealer cards,
        Send the client data for the dealers down card, and call 'flip_down_card()' there
        
        """
        dealer_hand = self.current_round.dealers_hand
        data = dealer_hand.get_cards() 
        client = Client(data=data[0], table_id=self.id, action='flip_down_card')
        client.notify()
        while (dealer_hand.score < 17) and (not dealer_hand.busted):
            time.sleep(.7)
            new_card = self.pull_card()
            dealer_hand.add_card(new_card)
            
        self.game_state = consts.GAME_STATE_BIDDING
        self.save()
        self.update_game()
        self.resolve_bets()
        
    def resolve_bets(self):
        """
        We should be dealing with nonbusted, nonsurrendered hands only
        """
        dealer = self.current_round.dealers_hand
        hands = BlackJackHand.objects.filter(round=self.current_round, resolved=False)
        for hand in hands:
            if hand.has_blackjack and not dealer.has_blackjack:
                hand.blackjack()
                continue
            
            elif (hand.score == dealer.score):
                hand.push()
                continue
            
            elif dealer.busted:
                hand.won()
                continue
            
            elif hand.score > dealer.score:
                hand.won()
                continue
            
            else:
                hand.lost()
                continue
        
        self.start_new_round()
    
    
class BlackJackRound(models.Model):
    table = models.ForeignKey(BlackJackTable)
    taking_bets = models.BooleanField(default=True)
    closed = models.BooleanField(default=False)
    started = models.DateTimeField(default=datetime.datetime.utcnow)
    
    def close(self):
        self.closed = True
        self.save()
    
    @property
    def dealers_hand(self):
        return BlackJackHand.objects.get(round=self, dealers_hand=True)
    
    class Meta:
        ordering = ('-started',)
    
    def save(self, *args, **kwargs):
        super(BlackJackRound, self).save(*args, **kwargs)
        
    
class BlackJackHand(BaseHand):
    round = models.ForeignKey(BlackJackRound)
    dealers_hand = models.BooleanField(default=False)
    doubled = models.BooleanField(default=False)
    stood = models.BooleanField(default=False)
    split = models.ForeignKey('self', related_name='split_from', null=True)
    available_actions = models.CharField(max_length=256, default=consts.BLACK_JACK_DEFAULT_AVAILABLE_ACTIONS)
    
    
    def save(self, *args, **kwargs):
        """
        When a new hand is created, we look to see if it is time to deal
        """
        check_for_round_start = False
        if not self.id:
            #TODO:should maybe use a post_create signal here, would be less ugly
            check_for_round_start = True
        elif (not self.resolved) and (not self.stood) and (not self.dealers_hand):
            advance_turn = False
            if self.busted:
                self.lost()
                advance_turn = True
                
            if self.score == 21:
                self.stood = True
                advance_turn = True
            
            if advance_turn:
                table = self.round.table
                if table.current_turn.player_id == self.player_id:
                    try:
                        BlackJackHand.objects.get(player=self.player, round=self.round, stood=False, resolved=False)
                        table.next_turn()
                    except BlackJackHand.DoesNotExist:
                        pass
                    
        super(BlackJackHand, self).save(*args, **kwargs)
        if check_for_round_start:
            round = self.round 
            table = round.table
            hand_count = BlackJackHand.objects.filter(round=self.round, dealers_hand=False).count()
            all_bets_in = (hand_count == table.num_players and table.num_players) 
            if  all_bets_in:
                round.taking_bets = False
                round.save()
                table.initial_deal()
        
    @property
    def score(self):
        cards = self.get_cards()
        total = sum([consts.BLACK_JACK_CARD_VALUE_MAPPING.get(c['value'], 10) for c in cards])
        if total > 21:
            total = sum([consts.ALT_BLACK_JACK_CARD_VALUE_MAPPING.get(c['value'], 10) for c in cards])
        
        return total
    
    @property
    def busted(self):
        return self.score > 21
    
    @property
    def can_split(self):
        cards = self.get_cards()
        if (len(self.get_cards()) == 2) and not self.split_from.all().count():
            if consts.BLACK_JACK_CARD_VALUE_MAPPING.get(cards[0]['value'], 10)  \
                == consts.BLACK_JACK_CARD_VALUE_MAPPING.get(cards[1]['value'], 10):
                return True
        
        return False
            
            
    
    def add_card(self, card):
        cards = self.get_cards()
        cards.append(card)
        self.set_cards(cards)
        if self.can_split:
            actions = self.get_available_actions()
            actions.append('split')
            self.set_available_actions(actions)
        self.save()
        
        if self.dealers_hand:
            card['dealt_to'] = 'dealer'
        else:
            if self.split_from.all().count():
                card['split_card'] = True
            player_id = self.player_id
            card['dealt_to'] = player_id
                
        if (self.dealers_hand and self.num_cards == 1):
            card.update(Card.get_face_down())
            
        client = Client(data=card, table_id=self.round.table_id, action='deal_card')
        client.notify()
            

    def won(self):
        player = self.player
        player.credit(self.bet)
        player.update_balance(self.round.table_id, str(self.bet))
        self.resolve()
        
        
    def lost(self):
        player = self.player
        player.debit(self.bet)
        player.update_balance(self.round.table_id, str(self.bet))
        self.resolve()
        
        
    def blackjack(self):
        player = self.player
        amount = Decimal('1.5') * self.bet
        player.credit(amount)
        player.update_balance(self.round.table_id, str(amount))
        self.resolve()
        data = {'player_id': self.player_id, 'name': player.name }
        client = Client(data=data, table_id=self.round.table_id, action='blackjack')
        client.notify()
        
    def push(self):
        self.resolve()
    
    @property
    def has_blackjack(self):
        return (len(self.get_cards()) == 2) and (self.score == 21)

    def get_available_actions(self):
        return simplejson.loads(self.available_actions)
    
    def set_available_actions(self, available_actions):
        self.available_actions = simplejson.dumps(available_actions)
        self.save()

