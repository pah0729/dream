from django.contrib import admin
from .models import JobReport


# Register your models here.
class JobReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_data', 'sdate', 'edate')
    list_filter = ('user', 'sdate', 'edate')
    search_fields=('user__user__username', 'sdate','edate')

admin.site.register(JobReport, JobReportAdmin)


