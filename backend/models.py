from decimal import Decimal
import datetime
import simplejson
from webservice_tools import db_utils, utils
import consts
from django.db import models
from webservice_tools.apps.user.models import BaseProfile
from webservice_tools.decorators import cached_property
from backend import bitcoinrpc
from backend.client_connection import ClientConnection as Client
import random

# Create your models here.
class Table(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    deck = models.TextField(default='[]', editable=False)
    current_turn = models.ForeignKey('backend.Seat', related_name='playing_at', null=True)
    def dict(self):
        return {'name': self.name, 'id': self.id,
                'public': self.public, }
    
    def save(self, *args, **kwargs):
        need_seats = False
        if not self.id:
            need_seats = True
            self.shuffle_cards()
        super(Table, self).save(*args, **kwargs)
        if need_seats:
            for p in range(consts.NUM_SEATS):
                Seat.objects.create(position=p + 1, table=self)
                
    def get_game_data(self):
        ret = self.dict()
        ret['seats'] = []
        for seat in self.seats:
            ret['seats'].append({'seat_id': seat.id,
                                 'position': seat.position,
                                 'player_name': seat.player.name if seat.player else None,
                                 'player_id': seat.player.id if seat.player else None,
                                 'current_turn': self.current_turn_id == seat.id})
        return ret
    
    
    def shuffle_cards(self):
        deck = []
        for _ in range(self.num_decks):
            deck.append(consts.BLACKJACK_CARDS)
        deck = utils.flatten(deck)
        random.shuffle(deck)
        self.deck = simplejson.dumps(deck)
        
    
    def get_deck(self):
        return simplejson.loads(self.deck)
    
    def pull_cards(self, num_cards):
        deck = self.get_deck()
        if len(deck) < num_cards:
            self.shuffle_cards()
            deck = self.get_deck()
        cards = deck[-num_cards:]
        del deck[-num_cards:]
        self.deck = simplejson.dumps(deck)
        return cards
    
    def pull_card(self):
        return self.pull_cards(1)[0]
    
    @property
    def num_decks(self):
        return consts.NUM_DECKS_DEFAULT
    
    @cached_property
    def seats(self):
        return Seat.objects.filter(table=self).select_related('player')
    
    
    @property
    def players(self):
        return [s.player.name for s in self.seats if s.player]
    
    @property
    def num_seats(self):
        return len(self.seats)
    
    @property
    def num_players(self):
        return len(self.players)
    
    @property
    def available_seats(self):
        return [s for s in self.seats if s.player == None]
    
    @property
    def num_available_seats(self):
        return len(self.available_seats)
    
    
    

class Player(BaseProfile):
    handle = models.CharField(max_length=32, default='', blank=True)
    show_animations = models.BooleanField(default=True)
    payout_address = models.CharField(max_length=64)
    account_name = models.CharField(unique=True, max_length=512, default='', blank=True)
    
    def save(self, *args, **kwargs):
        if self.user.username != self.account_name:
            self.account_name = self.user.username
        super(Player, self).save(*args, **kwargs)
        
        
    def create_callback(self):
        bitcoinrpc.create_account(self.account_name)
    
    @property
    def name(self):
        return self.handle or self.user.username
    
    @property    
    def balance(self):
        return bitcoinrpc.get_balance(self.account_name)
    
    @property
    def address(self):
        return bitcoinrpc.get_address(self.account_name)
    
    def credit(self, amount):
        """
        raises InvalidOperation
        """
        assert isinstance(amount, Decimal)
        bitcoinrpc.credit(float(amount), self.account_name)
    
    def debit(self, amount):
        """
        raises InvalidOperation
        """
        assert isinstance(amount, Decimal)
        bitcoinrpc.debit(float(amount), self.account_name)
        
    
    def withdraw(self, amount):
        """
        raises InvaldOperation
        """
        amount = float(amount)
        if amount <= self.balance:
            bitcoinrpc.send(self.account_name, self.payout_address, amount)
    
    def update_balance(self, table_id, balance_change):
        data = {'balance': self.pretty_balance, 'balance_change': balance_change}
        client = Client(data=data, table_id=table_id,
                                player_id=self.id, action='update_balance')
        client.notify()
    
    @property
    def pretty_balance(self):
        bal = str(self.balance)
        temp = bal[::-1]
        for i in range(len(temp)):
            if temp[i] != '0':
                ret =  bal[:-1*i]
                break
        
        if ret.endswith('.'):
            ret += '00'
            
        return ret
            
class Card(models.Model):
    value = models.CharField(max_length=15, choices=consts.CARD_VALUE_CHOICES)
    suite = models.CharField(max_length=15, choices=consts.CARD_SUITE_CHOICES)
    card_dir = '/static/images/cards'
    @classmethod
    def get_face_down(cls):
        return {'id': None, 'value': None, 'suite': None,
                'name': None, 'image_url': "%s/%s" % (cls.card_dir, 'gray_back.png')}
    
    def dict(self):
        return {'id': self.id, 'value': self.value, 'suite': self.suite,
                'name': self.name, 'image_url':self.image_url}
    
    @property
    def name(self):
        return "%s of %s" % (self.value.title(), self.suite.title())
    
    @property
    def image_url(self):
        return '%s/%s_%s.png' % (self.card_dir, self.value, self.suite)
    
    
    class Meta:
        unique_together = ('value', 'suite')
        
    def admin_thumbnail(self):
        return u'<img src="%s" />' % (self.image_url)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    
    
class Seat(models.Model):
    position = models.PositiveIntegerField()
    table = models.ForeignKey(Table)
    player = models.ForeignKey(Player, null=True)
    
    class Meta:
        unique_together = ('table', 'player')
        ordering = ('position',)
        
        
class BaseHand(models.Model):
    cards = models.TextField(max_length=512, default='[]')
    bet = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    player = models.ForeignKey(Player, null=True)
    resolved = models.BooleanField(default=False)
    when_created = models.DateTimeField(default=datetime.datetime.utcnow)
    class Meta:
        abstract = True
    
    def get_cards(self):
        return simplejson.loads(self.cards)
    
    def set_cards(self, cards):
        self.cards = simplejson.dumps(cards)
        
    
    @property
    def num_cards(self):
        return len(self.get_cards())
    
    def resolve(self):
        self.resolved = True
        self.save()

def gen_key():
    L = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-'
    return reduce(lambda a,b:a+b, [random.choice(L) for _ in range(32)])

class Invitation(models.Model):
    key = models.CharField(max_length=32, blank=True, default=gen_key)
    player = models.ForeignKey(Player, null=True)
    


    
