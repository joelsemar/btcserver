from backend.models import Player
from django import forms
from webservice_tools.apps.user.forms import ExtModelForm, BaseUserForm

class UserForm(BaseUserForm):
    pass
class UserProfileForm(ExtModelForm):
    
    class Meta:
        model = Player
        exclude = ('user')
    
