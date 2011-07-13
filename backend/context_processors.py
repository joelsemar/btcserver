

from socket import gethostname
hostname = gethostname()

def base(request):
    if hostname == 'bitcoinpalace':
        context = {'domain': 'bitcoinpalace.com'}
    else:
        context = {'domain': 'localhost'}
    if request.user.is_authenticated():
        player= request.user.get_profile()
        context['name'] = player.name 
        context['balance'] = player.pretty_balance
        context['player_id'] = player.id
    return context