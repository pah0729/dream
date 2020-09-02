from django import forms
from .models import Commute

class CommuteForm(forms.ModelForm):
    
    class Meta:
        model = Commute
        fields = ('condition', 'reason', 'local', 'date_commute')
        label = {
            'condition':'상태',
            'reason':'사유',
            'local':'위치',
            'date_commute' : '날짜'
        }

class CommuteAdForm(forms.ModelForm):
    
    class Meta:
        model = Commute
        fields = ()
        label = {
            
        }