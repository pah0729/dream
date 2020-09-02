from django import forms
from .models import JobReport

class JobReportForm(forms.ModelForm):
    
    class Meta:
        model = JobReport
        fields = ('sdate', 'edate', 'bsnsD', 'annual', 'late', 'important', 'incmp','etc', 'data')
        label = {
            'sdate':'시작일',
            'edate':'종료일',
            'bsnsD':'업무일수',
            'annual':'연차',
            'late':'지각',
            'important':'중요사항',
            'incmp':'차주계획',
            'etc':'기타사항',
            'data':'일일 일지'
           
        }


