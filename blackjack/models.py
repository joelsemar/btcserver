import consts
from webservice_tools import utils
from django.db import models
from backend.models import BaseBet, Card, Player, Table
from webservice_tools.decorators import cached_property

class BlackJackTableType(models.Model):
    name = models.CharField(max_length=128)
    low_bet = models.DecimalField(max_digits=12, decimal_places=8)
    high_bet = models.DecimalField(max_digits=12, decimal_places=8)
    
    
    def __unicode__(self):
        return 'Low: %.8s, High: %s' % (self.low_bet, self.high_bet)

class BlackJackTable(Table):
    type = models.ForeignKey(BlackJackTableType)
    
    @property
    def game_state(self):
        ret = {'table_id': self.id}
        ret['data'] = self.dict()
        return ret
    
    @cached_property
    def high_bet(self):
        return self.type.high_bet
    
    @cached_property
    def low_bet(self):
        return self.type.low_bet
    
    def __unicode__(self):
        return '%s: %s - %s' % (self.name, self.type.low_bet, self.type.high_bet)
        
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

