from backend.models import Player
from django import forms
from webservice_tools.apps.user.forms import ExtModelForm, BaseUserForm

class UserForm(BaseUserForm):
    email = forms.EmailField(required=True, error_messages={'required': "Email is required"})
    username = forms.CharField(max_length=255, required=False)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        self.cleaned_data['username'] = email
        return self.cleaned_data

class UserProfileForm(ExtModelForm):
    
    class Meta:
        model = Player
        exclude = ('user', 'friends')
    
