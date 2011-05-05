

from socket import gethostname
hostname = gethostname()

def base(request):
    if hostname == 'bitcoinpalace':
        context = {'domain': '127.0.0.1'}
    else:
        context = {'domain': '127.0.0.1'}
    if request.user.is_authenticated():
        player= request.user.get_profile()
        context['name'] = player.name 
        context['balance'] = player.balance
        context['player_id'] = player.id
    return context