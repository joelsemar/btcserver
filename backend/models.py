import consts
from django.db import models
from webservice_tools.apps.user.models import BaseProfile
from backend import bitcoinrpc
# Create your models here.
class Table(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=32)
    description = models.TextField()
    
    class Meta:
        abstract = True

class Player(BaseProfile):
    show_animations = models.BooleanField(default=True)
    payout_address = models.CharField(max_length=64, default='', blank=True)
    account_name = models.CharField(unique=True, max_length=512, default='', blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.user.username != self.account_name:
            self.account_name = self.user.username
        super(Player, self).save(*args, **kwargs)
        
        
    def create_callback(self):
        bitcoinrpc.create_account(self.account_name)
        
    
    @property    
    def balance(self):
        return bitcoinrpc.get_balance(self.account_name)
    
    @property
    def address(self):
        return bitcoinrpc.get_address(self.account_name)
    
    
class Card(models.Model):
    name = models.CharField(max_length=15,choices=consts.CARD_CHOICES)
    value = models.PositiveIntegerField()