from django import forms
from django.contrib.auth.models import User
from .models import AcesStts

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class AcesSttsForm(forms.ModelForm):

    class Meta:
        model = AcesStts
        fields =[]
       
