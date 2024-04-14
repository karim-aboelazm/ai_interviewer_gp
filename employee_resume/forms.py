from django import forms
from .models import *

# upload resume form
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'

class HRLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    userpassword = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            pass
        else:
            raise forms.ValidationError('hr with this username does not exists')
        return user_name