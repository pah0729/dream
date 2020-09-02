from django.contrib import admin
from .models import Notice, Comment, NoticeTarget, Tag, CaseManagement, CaseTag


# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'targets', 'date')
    search_fields=('user__user__username', 'title','targets', 'content')
    fieldsets = [
        (None, {'fields': ['user']}),
        ('대상자', {'fields': ['targets']}),
        ('공지내용', {'fields': ['important', 'title', 'content', 'date']}),
        ('태그', {'fields': ['hashtag', 'tag_set']}),
        ('첨부파일', {'fields': ['file1', 'file2', 'file3', 'file4', 'file5']}),
        ]
    readonly_fields = ['date']

class NoticeTargetAdmin(admin.ModelAdmin):
    list_display=('user', 'num', 'read')
    search_fields=('user__user__username', 'num__title')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('조회여부', {'fields': ['read']}),
        ]
    readonly_fields = []

class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'content', 'date', 'num')
    search_fields=('user__user__username', 'num__title', 'date')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('코멘트내용', {'fields': ['content', 'date']}),
        ]
    readonly_fields = ['date']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(CaseManagement)
class CaseManagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date')
    search_fields=('user__user__username', 'title', 'content')
    fieldsets = [
        (None, {'fields': ['user']}),
        ('내용', {'fields': ['title', 'content', 'date']}),
        ('태그', {'fields': ['hashtag', 'tag_set']}),
        ]
    readonly_fields = ['date']

@admin.register(CaseTag)
class CaseTagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Notice, NoticeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(NoticeTarget, NoticeTargetAdmin)

