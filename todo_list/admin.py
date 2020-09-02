from django.contrib import admin
from .models import TodoList
from accounts.models import Profile
# Register your models here.
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('userName', 'team', 'date', 'content', 'cmpltDate', 'cmplt', 'important')
    search_fields=('userName__user__username', 'content', 'important', 'team__name')
admin.site.register(TodoList, TodoListAdmin)
#admin.site.register(Profile)