from decimal import *
from webservice_tools import uuid
import consts
from django.db import models
from webservice_tools.apps.user.models import BaseProfile
from webservice_tools.decorators import cached_property
from backend import bitcoinrpc
# Create your models here.
class Table(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        need_seats = False
        if not self.id:
            need_seats = True
        super(Table, self).save(*args, **kwargs)
        if need_seats:
            for p in range(consts.NUM_SEATS + 1):
                Seat.objects.create(position=p, table=self)
    
    
    @cached_property
    def seats(self):
        return Seat.objects.filter(table=self).select_related('player')
    
    @property
    def players(self):
        return [s.player.username for s in self.seats if s.player]
    
    @property
    def num_seats(self):
        return len(self.seats)

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
    def username(self):
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
        bitcoinrpc.credit(str(amount), self.account_name)
    
    def debit(self, amount):
        """
        raises InvalidOperation
        """
        assert isinstance(amount, Decimal)
        bitcoinrpc.debit(str(amount), self.account_name)
        
    
    def withdraw(self, amount):
        """
        raises InvaldOperation
        """
        amount = float(amount)
        if amount <= self.balance:
            bitcoinrpc.send(self.account_name, self.payout_address, amount)
            
            
class Card(models.Model):
    name = models.CharField(max_length=15, choices=consts.CARD_CHOICES)
    value = models.PositiveIntegerField()



class Seat(models.Model):
    position = models.PositiveIntegerField()
    table = models.ForeignKey(Table)
    player = models.ForeignKey(Player, null=True)
    
class BaseBet(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=8)
    player = models.ForeignKey(Player)
        
    class Meta:
        abstract = True
