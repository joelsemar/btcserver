# Create your views here.
from blackjack.models import BlackJackTable
from django.views.generic.simple import direct_to_template

def table_list(request):
    tables = BlackJackTable.objects.filter(public=True)
    return direct_to_template(request, 'blackjack/table_list.html',
                               extra_context={'tables': tables})
    
