from django import forms
from .models import Profile, AnnualApprovalLine
import datetime

class EditUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "userImg",
            "email_google",
            "email",
            "phone",
            "really_address",
            "address",
            "emergency_phone"
        )
        widgets = {
            # 'userImg': forms.TextInput(attrs={'class': 'src'}),
        }


class RegisterForm(forms.Form):
    TEAM_CHOICES = (
        ('교육운영기획실', '교육운영기획실'),
        ('경영지원팀', '경영지원팀'),
        ('교육지원실', '교육지원실'),
        ('과학팀', '과학팀'),
        ('코딩팀', '코딩팀'),
        ('공예팀', '공예팀'),
        ('요리팀', '요리팀'),
        ('SI팀', 'SI팀'),
    )
    
    username = forms.CharField(label='성명',max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'성명을 입력하세요.', 'autocomplete':'off'}))
    team = forms.ChoiceField(label='소속 팀', choices=TEAM_CHOICES, required=True)
    email_google = forms.EmailField(label='구글이메일 (로그인 아이디로 사용됩니다.)', max_length=256, required=True, widget=forms.TextInput(attrs={'placeholder':'형식: glocal@gmail.com', 'autocomplete':'off'}) )
    email = forms.EmailField(label='개인이메일', max_length=256, required=True, widget=forms.TextInput(attrs={'placeholder':'자주 사용하는 이메일을 입력하세요.', 'autocomplete':'off'}))
    phone = forms.CharField(label='연락처',max_length=20 ,required=True, widget=forms.TextInput(attrs={'placeholder':'휴대폰번호를 입력하세요.', 'autocomplete':'off'}))
    entry_date = forms.DateField(label='입사일 (근로계약서기준일)', required=True, widget=forms.TextInput(attrs={'placeholder': '날짜를 선택하세요.', 'autocomplete':'off'}))
    residentNumber = forms.CharField(label='주민등록번호',max_length=14, required=True, widget=forms.TextInput(attrs={'placeholder': '주민등록번호를 입력하세요.', 'autocomplete':'off'}))
    really_address = forms.CharField(label='실거주주소', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'실제 거주하고 계신 주소를 입력하세요.', 'autocomplete':'off'}) )
    address = forms.CharField(label='등본상주소', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'주민등록등본상 주소를 입력하세요.', 'autocomplete':'off'}))
    emergency_phone = forms.CharField(label='비상 연락처 및 관계', max_length=20, required=True,widget=forms.TextInput(attrs={'placeholder': 'ex) 010-0000-0000 (관계)', 'autocomplete':'off'}) )



class NotifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pushToken']
        label = {
            'pushToken':'Access Tokens'
        }

class manageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('userNum', 'residentNumber','team', 'position',  'belong', 'email_google', 'email', 'phone','emergency_phone', 'entry_date','really_address','address')
        label = {
            'userNum': '사번',
            'residentNumber' : '주민등록번호',
            'team' : '팀',
            'position' : '직급',
            'belong' : '소속회사',
            'email_google': '구글메일', 
            'email': '개인메일',
            'phone': '연락처',
            'emergency_phone' : '비상연락처',
            'entry_date' : '입사일',
            'really_address' : '실거주주소',
            'address' : '등본상주소',
            
        }

class AnnualApprovalLineForm(forms.ModelForm):
    manager = forms.ModelChoiceField(label='담당자', queryset=Profile.objects.all().exclude(user__username='admin').exclude(user__is_active=False).order_by('user__username'), empty_label='선택하세요')
    approval = forms.ModelChoiceField(label='상위결재자', queryset=Profile.objects.all().exclude(user__username='admin').exclude(user__is_active=False).order_by('user__username'), empty_label='선택하세요')
    class Meta:
        model = AnnualApprovalLine
        fields = ['manager', 'approval']
        label = {
            'manager':'담당자',
            'approval':'상위결재자',
        }