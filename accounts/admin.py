from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Team, Position, Belong, TeamRelationship, AnnualApprovalLine
from django.utils.safestring import mark_safe


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'position', 'belong', 'entry_date', 'userNum', 'email_google', 'phone', 'emergency_phone')
    search_fields = ('user__username', 'team__name', 'position__name')
    fieldsets = [
        (None, {'fields': ['user', 'team', 'position', 'belong', 'entry_date', 'userNum', 'userImg_image', 'userImg']}),
        ('개인정보', {'fields': ['email_google', 'email', 'phone', 'emergency_phone', 'residentNumber', 'address', 'really_address']}),
        ('알림설정', {'fields': ['pushToken', 'notifySettings']})
    ]
    readonly_fields = ['userImg_image']

    def userImg_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.userImg.url,
                width = 113,
                height = 151,
                )
            )
    userImg_image.short_description = '사진 미리보기'

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'memo')

class TeamRelationshipAdmin(admin.ModelAdmin):
    list_display = ('source', 'parent', 'display')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class BelongAdmin(admin.ModelAdmin):
    list_display = ['name']

class AnnualApprovalLineAdmin(admin.ModelAdmin):
    list_display = ('manager', 'approval')
    search_fields = ('manager__user__username', 'approval__user__username')
    fieldsets = [
        ('담당자 (중복해서 등록하시면 절대 안됩니다!!)', {'fields': ['manager']}),
        ('상위결재자', {'fields': ['approval']})
    ]

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    

admin.site.register(Team, TeamAdmin)
admin.site.register(TeamRelationship, TeamRelationshipAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Belong, BelongAdmin)
admin.site.register(AnnualApprovalLine, AnnualApprovalLineAdmin)
admin.site.unregister(User,)
admin.site.register(User, UserAdmin)

