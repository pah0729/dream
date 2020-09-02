from django.contrib import admin
from .models import Project, ProjectTarget, Todo, TodoTarget, TodoComment
from accounts.models import Profile
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'condition', 'targets', 'sdate', 'edate')
    search_fields=('user__user__username', 'title','targets', 'content')
    fieldsets = [
        (None, {'fields': ['user']}),
        ('대상자', {'fields': ['targets']}),
        ('프로젝트 내용', {'fields': ['title', 'content']}),
        ('프로젝트 기간', {'fields': ['sdate', 'edate']}),
        ]
    readonly_fields = ['user']

class ProjectTargetAdmin(admin.ModelAdmin):
    list_display=('user', 'num')
    search_fields=('user__user__username', 'num__title')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('조회여부', {'fields': ['read']}),
        ]
    readonly_fields = ['user']

class TodoAdmin(admin.ModelAdmin):
    list_display = ('user', 'num', 'condition', 'targets', 'important','sdate', 'edate')
    search_fields=('user__user__username', 'targets', 'content', 'important', 'condition','sdate', 'edate')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('대상자', {'fields': ['targets']}),
        ('업무 내용', {'fields': ['important', 'content']}),
        ('업무 기간', {'fields': ['sdate', 'edate']}),
        ('업무 진행상태', {'fields': ['condition']}),
        ]
    readonly_fields = ['user']

class TodoTargetAdmin(admin.ModelAdmin):
    list_display=('user', 'num')
    search_fields=('user__user__username', 'num__user__user__username')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('조회여부', {'fields': ['read']}),
        ]
    readonly_fields = ['user']

class TodoCommentAdmin(admin.ModelAdmin):
    list_display=('user', 'content', 'date', 'num')
    search_fields=('user__user__username', 'content', 'date')
    fieldsets = [
        (None, {'fields': ['user', 'num']}),
        ('코멘트내용', {'fields': ['content', 'date']}),
        ]
    readonly_fields = ['user', 'date']


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTarget, ProjectTargetAdmin)
admin.site.register(Todo, TodoAdmin)
admin.site.register(TodoTarget, TodoTargetAdmin)
admin.site.register(TodoComment, TodoCommentAdmin)
