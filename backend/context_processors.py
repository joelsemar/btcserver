


def base(request):
    context = {'domain': 'bitcoinpalace.com'}
    if request.user.is_authenticated():
        player= request.user.get_profile()
        context['name'] = player.name 
        context['balance'] = player.balance
    return context