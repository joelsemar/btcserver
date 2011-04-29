from webservice_tools.apps.user.handlers import GenericUserHandler
from webservice_tools.utils import BaseHandler
from webservice_tools.decorators import login_required
from decimal import InvalidOperation
from backend.models import Player


class UserHandler(GenericUserHandler):
    model = Player
    allowed_methods = ('POST', 'GET', 'PUT')
    extra_fields = ('balance', 'address')
    
    
class AccountWithdrawalHandler(BaseHandler):
    allowed_methods = ('POST',)
    
    @login_required
    def create(self, request, response):
        """
        Creates an account withdrawal for the logged in user
        API Handler: /account/withdrawal
        Params:
            @amount [float] amount for the withdrawal, can be divisible as far as the current
                bitcoind implementation allows.  (.00000001 at the time of writing) 
        """
        player = request.user.get_profile()
        amount = request.POST.get('amount')
        try:
            player.withdraw(amount)
        except InvalidOperation:
            return response.send(errors='Invalid withdrawal amount', status=500)
        return response.send()
            
    
    
       
    
    