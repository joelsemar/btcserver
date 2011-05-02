# Create your views here.
from blackjack.models import BlackJackTable, BlackJackTableType
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def table_list(request):
    context = {}
    context['tables'] = BlackJackTable.objects.filter(public=True)
    if context['tables']:
        return direct_to_template(request, 'blackjack/table/list.html', extra_context=context)
    else:
        return HttpResponseRedirect('/blackjack/table')
     
@login_required
def table(request):
    profile = request.user.get_profile()
    context = {}
    try:
        table = BlackJackTable.objects.get(seat__player=profile)
    except BlackJackTable.DoesNotExist:
        context['table_types'] = BlackJackTableType.objects.all()
        
    else:
        context['table'] = table.get_game_state()
        
    return direct_to_template(request, 'blackjack/table/table.html',
                               extra_context=context)
                                   
