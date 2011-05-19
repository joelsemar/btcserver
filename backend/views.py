# Create your views here.
from backend.models import Invitation
from blackjack.models import BlackJackTable, BlackJackTableType
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def login(request, key):
    return direct_to_template(request, 'login.html',
                               extra_context={})
    