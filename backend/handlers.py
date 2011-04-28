from webservice_tools.apps.user.handlers import GenericUserHandler
from btcserver.models import Player


class UserHandler(GenericUserHandler):
    extra_fields = ('balance',)
    model = Player
        