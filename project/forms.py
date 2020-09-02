from django import forms
from .models import Project,ProjectTarget, Todo, TodoTarget, TodoComment
from accounts.models import Profile

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('title','content', 'targets', 'sdate', 'edate')
        label = {
            'title':'제목',
            'content':'내용',
            'targets':'타깃',
            'sdate':'시작일',
            'edate':'종료일'
           
        }
'''
    def __init__(self, user, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.fields['userName'].queryset = Profile.objects.filter(pk=user.pk)
'''
class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = {'targets', 'content', 'important', 'sdate', 'edate'}
        label = {
            'targets' : '타깃',
            'content' : '내용',
            'important' : '중요도',
            'sdate': '시작일',
            'edate': '종료일'
            
        }
class ProjectTargetForm(forms.ModelForm):

    class Meta:
        model = ProjectTarget
        fields = {}
        label = {
           
            
        }

class TodoTargetForm(forms.ModelForm):

    class Meta:
        model = TodoTarget
        fields = {}
        label = {
           
            
        }

class TodoCommentForm(forms.ModelForm):

    class Meta:
        model = TodoComment
        fields = {'content'}
        label = {
            'content': '내용'
           
            
        }
class ConditionForm(forms.ModelForm):

    class Meta:
        model= Todo
        fields={'condition', 'complate'}
        label={
            'condition':'상태',
            'complate':'완료일'
        }

