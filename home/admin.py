from django.contrib import admin
from .models import UserLoginLog, AcesStts
# Register your models here.

@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'user_agent', 'created_at',)
    list_filter = ('user', 'ip_address', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ( 'user__username', 'user__email', 'ip_address')
    
class AcesSttsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('user', 'date')
    search_fields=('user__user__username', 'date')
        
        
admin.site.register(AcesStts, AcesSttsAdmin)