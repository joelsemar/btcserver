from backend.models import Player
from django import forms
from webservice_tools.apps.user.forms import ExtModelForm, BaseUserForm

class UserForm(BaseUserForm):
    def clean(self):
        email = self.cleaned_data.get('email')
        self.cleaned_data['username'] = email
        return self.cleaned_data

class UserProfileForm(ExtModelForm):
    
    class Meta:
        model = Player
        exclude = ('user', 'friends')
    
