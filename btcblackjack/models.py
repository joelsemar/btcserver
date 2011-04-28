import consts
from django.db import models
from webservice_tools.apps.user.models import BaseProfile
from backend import bitcoinrpc
from backend.models import Card, Player, Table
class BlackJackTable(Table):
    low_bet = models.DecimalField(max_digits=8, decimal_places=2)
    high_bet = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.low_bet, self.high_bet)
        
    def save(self, *args, **kwargs):
        if not self.id:
            for p in range(consts.NUM_SEATS + 1):
                Seat.objects.create(position=p, table=self)
        super(Table, self).save(*args, **kwargs)
    
    class Meta:
        abstract = False

class Seat(models.Model):
    position = models.PositiveIntegerField()
    table = models.ForeignKey(BlackJackTable)
    player = models.ForeignKey(Player, null=True)
     
    
class Hand(models.Model):
    cards = models.ManyToManyField(Card, symmetrical=False)
    type = models.CharField(max_length=16, choices=consts.HAND_TYPE_CHOICES)
    
    @property
    def score(self):
        return sum([c.value for c in self.cards.all()])
    
    
class Round(models.Model):
    table = models.ForeignKey(BlackJackTable)
    dealers_hand = models.ForeignKey(Hand)


    
    
class Bet(models.Model):
    game = models.ForeignKey(Round)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    players_hand = models.ForeignKey(Hand)
    score = models.PositiveIntegerField()
    player = models.ForeignKey(Player)
        
    @property
    def busted(self):
        return self.score > 21


    
