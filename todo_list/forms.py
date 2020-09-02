from django import forms
from .models import TodoList

class NewForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['content','important']
