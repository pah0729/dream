from django.contrib import admin
from .models import Commute


# Register your models here.
class CommuteAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_commute', 'condition')
    list_filter = ('user', 'date_commute', 'condition')
    search_fields=('user__user__username', 'date_commute','condition')

admin.site.register(Commute, CommuteAdmin)


