import consts
from django.db import models
from backend.models import BaseBet, Card, Player, Table

class BlackJackTable(Table):
    low_bet = models.DecimalField(max_digits=8, decimal_places=2)
    high_bet = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.low_bet, self.high_bet)
        
    class Meta:
        abstract = False

     
    
class BlackJackHand(models.Model):
    cards = models.ManyToManyField(Card, symmetrical=False)
    type = models.CharField(max_length=16, choices=consts.HAND_TYPE_CHOICES)
    
    @property
    def score(self):
        return sum([c.value for c in self.cards.all()])
    
    
class BlackJackRound(models.Model):
    table = models.ForeignKey(BlackJackTable)
    dealers_hand = models.ForeignKey(BlackJackHand)

    
class BlackJackBet(BaseBet):
    game = models.ForeignKey(BlackJackRound)
    players_hand = models.ForeignKey(BlackJackHand)
    score = models.PositiveIntegerField()
        
    @property
    def busted(self):
        return self.score > 21


    
