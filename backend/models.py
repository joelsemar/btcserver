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
    payout_address = models.CharField(max_length=64)
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
    
    
class Card(models.Model):
    name = models.CharField(max_length=15,choices=consts.CARD_CHOICES)
    value = models.PositiveIntegerField()