

def base(request):
    player= request.user.get_profile()
    context = {'domain': '127.0.0.1'}
    context['name'] = player.name 
    context['balance'] = player.balance
    return context