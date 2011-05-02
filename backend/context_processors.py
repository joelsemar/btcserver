

def base(request):
    context = {'domain': '127.0.0.1'}
    if request.user.is_authenticated():
        player= request.user.get_profile()
        context['name'] = player.name 
        context['balance'] = player.balance
    return context