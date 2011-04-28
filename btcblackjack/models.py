import consts
from django.db import models
from webservice_tools.apps.user.models import BaseProfile
from backend import bitcoinrpc
class Table(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    description = models.TextField()
    low_bet = models.DecimalField(max_digits=8, decimal_places=2)
    high_bet = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.low_bet, self.high_bet)
        
    def save(self, *args, **kwargs):
        if not self.id:
            for p in range(consts.NUM_SEATS + 1):
                Seat.objects.create(position=p, table=self)
        super(Table, self).save(*args, **kwargs)

class Seat(models.Model):
    position = models.PositiveIntegerField()
    table = models.ForeignKey(Table)
    
    
class Card(models.Model):
    name = models.CharField(choices=consts.CARD_CHOICES)
    value = models.PositiveIntegerField()
    
class Hand(models.Model):
    cards = models.ManyToManyField(Card, symmetrical=False)
    
    @property
    def score(self):
        return sum([c.value for c in self.cards.all()])
    
    
class Round(models.Model):
    table = models.ForeignKey(Table)
    dealers_hand = models.ForeignKey(Hand)


class Player(BaseProfile):
    show_animations = models.BooleanField(default=True)
    payout_address = models.CharField(max_length=64)
    seat = models.ForeignKey(Seat, null=True)
    username = models.CharField(unique=True, max_length=512)
    
    
    def save(self, *args, **kwargs):
        if self.user.username != self.username:
            self.username = self.user.username
        super(Player, self).save(*args, **kwargs)
        
        
    def create_callback(self):
        bitcoinrpc.create_account(self.user.username)
        
    
    @property    
    def balance(self):
        return bitcoinrpc.get_balance(self.username)
    
    @property
    def address(self):
        return bitcoinrpc.get_address(self.username)
    
    
class Bet(models.Model):
    game = models.ForeignKey(Round)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    players_hand = models.ForeignKey(Hand)
    score = models.PositiveIntegerField()
    player = models.ForeignKey(Player)
        
    @property
    def busted(self):
        return self.score > 21


    
