from django import forms
from .models import Annual, AnnualDate, Profile, Team, Position
from django.contrib.auth.models import User

class AnnualForm(forms.ModelForm):

    class Meta:
        model = Annual
        fields = ['division','divreason','sdate','fdate','datediff','reason','local','relationship','network','remark','file']
        labels = {
            'division':'휴가구분',
            'divreason':'기타사유',
            'sdate':'시작날짜',
            'fdate':'종료날짜',
            'datediff':'휴가기간',
            'reason':'사유',
            'local':'휴가예상지역',
            'relationship':'관계',
            'network':'연락처',
            'remark':'비고',
            'file':'첨부서류'
        }

class ConfirmForm(forms.ModelForm):

    class Meta:
        model = Annual
        fields = ['step','status']
        labels = {
            'step':'결재선',
            'status':'승인상태',
        }
        widgets = {
            
        }

class ManageForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='이름', queryset=Profile.objects.all().exclude(user__username='admin').exclude(user__is_active=False).order_by('user__username'), empty_label='선택하세요')
    class Meta:
        model = Annual
        fields = ['user','division','divreason','sdate','fdate','datediff','reason']
        labels = {
            'user':'이름',
            'division':'휴가구분',
            'divreason':'기타사유 (휴가구분이 기타일 경우)',
            'sdate':'휴가시작일',
            'fdate':'휴가종료일',
            'datediff':'휴가일수',
            'reason':'사유',
        }
        widgets = {
            'divreason': forms.TextInput(attrs={'placeholder': '무급휴가/예비군 등', 'autocomplete':'off'}),
            'sdate': forms.TextInput(attrs={'placeholder': '휴가 시작일을 선택하세요', 'autocomplete':'off'}),
            'fdate': forms.TextInput(attrs={'placeholder': '휴가 종료일을 선택하세요', 'autocomplete':'off'}),
            'datediff': forms.NumberInput(attrs={'placeholder': '0.5일 단위로 입력하세요', 'autocomplete':'off', 'step':'0.5', 'min':'0.5', 'max':'30.0'}),
            'reason': forms.TextInput(attrs={'placeholder': '사유를 입력하세요.', 'autocomplete':'off'}),
        }

class AnnualDateForm(forms.ModelForm):

    class Meta:
        model = AnnualDate
        fields = ['memo']
        labels = {
            'memo':'발생 사유',
        }
        widgets = {
            'memo': forms.TextInput(attrs={'placeholder': '발생 사유를 입력하세요.', 'autocomplete':'off', 'value':''}),
        }