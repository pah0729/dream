from django import forms
from .models import Notice, Comment, NoticeTarget, CaseManagement
from accounts.models import Profile
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class NoticeForm(forms.ModelForm):
    
    class Meta:
        model = Notice
        fields = ('important', 'title', 'content', 'file1', 'file2', 'file3', 'file4', 'file5', 'targets', 'hashtag')
        label = {
            'important' : '중요도',
            'title':'제목',
            'content':'내용',
            'file1':'파일',
            'file2':'파일',
            'file3':'파일',
            'file4':'파일',
            'file5':'파일',
            'targets':'타깃',
            'hashtag':'해시태그',
           
        }
        widgets = {
            'content': forms.CharField(widget=CKEditorUploadingWidget()),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = {'content'}
        label = {
            'content' : '내용',
            
        }
class NoticeTargetForm(forms.ModelForm):

    class Meta:
        model = NoticeTarget
        fields = {}
        label = {
           
            
        }

class CaseManagementForm(forms.ModelForm):
    
    class Meta:
        model = CaseManagement
        fields = ('title', 'content', 'hashtag')
        label = {
            'title':'제목',
            'content':'내용',
            'hashtag':'해시태그',
           
        }
        widgets = {
            'content': forms.CharField(widget=CKEditorUploadingWidget()),
        }