import consts
from webservice_tools import utils
from django.db import models
from django.db.models import Q
from backend.models import  BaseHand, Card, Player, Table, Seat
from backend.client_connection import ClientConnection
from backend import bitcoinrpc
from webservice_tools.decorators import cached_property
from decimal import *
class BlackJackTableType(models.Model):
    name = models.CharField(max_length=128)
    low_bet = models.DecimalField(max_digits=12, decimal_places=8)
    high_bet = models.DecimalField(max_digits=12, decimal_places=8)
    
    
    def __unicode__(self):
        return 'Low: %.8s, High: %s' % (self.low_bet, self.high_bet)

class BlackJackTable(Table):
    type = models.ForeignKey(BlackJackTableType)
    
        
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.type.low_bet, self.type.high_bet)
        
    class Meta:
        abstract = False
    
    
    def get_game_state(self):
        ret = super(BlackJackTable, self).get_game_state()
        dealer_cards = self.current_round.dealers_hand.get_cards()
        dealer_up_cards = [Card.get_face_down()]
        for card in dealer_cards[1:]:
            dealer_up_cards.append(card)
        ret['dealer_up_cards'] = dealer_up_cards
        all_hands = BlackJackHand.objects.filter(round__table=self)
        for hand in all_hands:
            player = [p for p in ret['players'] if p['player_id'] == hand.player_id][0]
            player['cards'] = hand.get_cards()
            
         
        return ret
    
    @cached_property
    def high_bet(self):
        return self.type.high_bet
    
    @cached_property
    def low_bet(self):
        return self.type.low_bet
    
    @property
    def num_decks(self):
        return consts.NUM_DECKS_BLACKJACK
    
    
    def update_game(self):
        data = self.get_game_state()
        conn = ClientConnection(data=data, table_id=self.id, action='update_game')
        conn.send()
        
    def initial_deal(self):
        hands = BlackJackHand.objects.filter(round=self.current_round)
        self.current_turn = [s for s in self.seats if s.player][0]

        for _ in range(consts.NUM_CARDS_EACH_BLACKJACK):
            for hand in hands:
                hand.add_card(self.pull_card())
        
        self.save()
        self.update_game()
    
    
        
    @cached_property
    def current_round(self):
        try:
            return BlackJackRound.objects.get(table=self, closed=False)
        except BlackJackRound.DoesNotExist:
            return None
     
    
    def save(self, *args, **kwargs):
        needs_init = False
        if not self.id:
            needs_init = True
            self.shuffle_cards()
        super(BlackJackTable, self).save(*args, **kwargs)
        if needs_init:
            self.start_new_round()
            
    def start_new_round(self):
        if self.current_round:
            self.current_round.close()
        round = BlackJackRound.objects.create(table=self)
        BlackJackHand.objects.create(round=round, dealers_hand=True, bet=None, player=None)
                
                
    def next_turn(self):
        current_seat = self.current_turn
        try:
            self.current_turn = Seat.objects.filter(Q(position__gt=current_seat.position) & 
                                                     Q(table=self) & ~Q(player=None))[0]
            self.save()
            self.update_game()
        except IndexError:
            self.deal_dealer_cards()
        
    
    def deal_dealer_cards(self):
        dealer_hand = self.current_round.dealers_hand
        while (dealer_hand.score < 17) and (not dealer_hand.busted):
            new_card = self.pull_card()
            dealer_hand.add_card(new_card)
        self.save()
        data = dealer_hand.get_cards() 
        conn = ClientConnection(data=data, table_id=self.id, action='show_dealer_cards')
        conn.send()
        
        self.resolve_bets()
        
    def resolve_bets(self):
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
    
    def close(self):
        self.closed = True
        self.save()
    
    @property
    def dealers_hand(self):
        return BlackJackHand.objects.get(round=self, bet=None, player=None)
    
    
class BlackJackHand(BaseHand):
    round = models.ForeignKey(BlackJackRound)
    dealers_hand = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        check_hand_count = False
        if not self.id:
            check_hand_count = True
        super(BlackJackHand, self).save(*args, **kwargs)
        if check_hand_count:
            round = self.round
            table = round.table
            hand_count = BlackJackHand.objects.filter(round=self.round, dealers_hand=False).count()
            if hand_count == table.num_players and table.num_players:
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
    
    def add_card(self, card):
        card_ids = self.get_card_ids()
        card_ids.append(card['id'])
        self.set_card_ids(card_ids)
        self.save()
        
        if self.dealers_hand:
            card['dealt_to'] = 'dealer'
        else:
            player_id = self.player_id
            card['dealt_to'] = player_id
            if self.busted:
                self.lost()
                self.round.table.next_turn()
                
        if not (self.dealers_hand and self.num_cards == 1):
            conn = ClientConnection(data=card, table_id=self.round.table_id, action='deal_card')
            conn.send()
            
            
            

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
        conn = ClientConnection(data=data, table_id=self.round.table_id, action='blackjack')
        conn.send()
        
    def push(self):
        self.resolve()
    
    @property
    def has_blackjack(self):
        return (len(self.get_cards()) == 2) and (self.score == 21)
