from webservice_tools.apps.user.handlers import GenericUserHandler
from backend.models import Player


class UserHandler(GenericUserHandler):
    extra_fields = ('balance', 'address')
    model = Player
        