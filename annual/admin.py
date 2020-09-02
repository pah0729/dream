from django.contrib import admin
from annual.models import Annual, AnnualDate, MinusData


# Register your models here.

class AnnualAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'division', 'sdate', 'fdate', 'datediff', 'reason', 'local', 'network','create','step','status','finalApproval')
    search_fields = ('user__user__username', 'user__team__name', 'division')
    fieldsets = [
        (None, {'fields': ['user', 'team', 'position']}),
        ('연차 신청 내용', {'fields': ['division', 'divreason', 'sdate', 'fdate', 'datediff', 'reason', 'local', 'relationship', 'network', 'remark', 'create']}),
        ('서류제출', {'fields': ['file']}),
        ('연차 결재 상태', {'fields': ['step', 'status','return_reason','finalApproval']}),
        ('연차 결재 서명', {'fields': ['teamleader', 'chief', 'director_office', 'director_center']}),
        ('연차 결재 코멘트', {'fields': ['teamleader_comment', 'chief_comment', 'director_office_comment', 'director_center_comment']}),
        ]

class AnnualDateAdmin(admin.ModelAdmin):
    list_display = ('user', 'ocrncDate', 'extncDate', 'is_active', 'is_delete', 'memo', 'finalUpdtd','annualcal')
    list_filter = ('user', 'ocrncDate', 'extncDate', 'is_active', 'is_delete')
    search_fields = ('user__user__username', )
    fieldsets = [
        (None, {'fields': ['user', 'ocrncDate', 'extncDate', 'memo', 'finalUpdtd']}),
        ('사용 및 소멸여부 ( 반드시 둘 중 하나만 선택하세요 )', {'fields': ['is_active', 'is_delete']})
    ]

    actions = ['make_active_true', 'make_active_false', 'make_delete_true', 'make_delete_false', 'usedate_remove', 'extdate_remove']

    def make_active_true(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(request, '{}건의 연차를 사용 상태로 변경하였습니다.'.format(updated_count))
    make_active_true.short_description = '선택된 연차를 사용 상태로 변경합니다.'

    def make_active_false(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(request, '{}건의 연차를 미사용 상태로 변경하였습니다.'.format(updated_count))
    make_active_false.short_description = '선택된 연차를 미사용 상태로 변경합니다.'

    def make_delete_true(self, request, queryset):
        updated_count = queryset.update(is_delete=True)
        self.message_user(request, '{}건의 연차를 소멸 상태로 변경하였습니다.'.format(updated_count))
    make_delete_true.short_description = '선택된 연차를 소멸 상태로 변경합니다.'

    def make_delete_false(self, request, queryset):
        updated_count = queryset.update(is_delete=False)
        self.message_user(request, '{}건의 연차를 소멸 상태로 변경하였습니다.'.format(updated_count))
    make_delete_false.short_description = '선택된 연차를 미소멸 상태로 변경합니다.'

    def usedate_remove(self, request, queryset):
        updated_count = queryset.update(finalUpdtd=None)
        self.message_user(request, '{}건의 연차 사용일을 제거하였습니다.'.format(updated_count))
    usedate_remove.short_description = '선택된 연차의 사용일을 제거합니다.'

    def extdate_remove(self, request, queryset):
        updated_count = queryset.update(extncDate=None)
        self.message_user(request, '{}건의 연차 소멸일을 제거하였습니다.'.format(updated_count))
    extdate_remove.short_description = '선택된 연차의 소멸일을 제거합니다.'

class MinusAdmin(admin.ModelAdmin):
    list_display = ('user', 'ocrncDate', 'payback', 'finalUpdtd','minuscal')
    list_filter = ('user', 'ocrncDate', 'payback', 'finalUpdtd')
    search_fields = ('user__user__username', )
    fieldsets = [
        (None, {'fields': ['user', 'ocrncDate', 'finalUpdtd']}),
        ('삭감 여부 ( 임의 설정 시 자동 삭감처리되지 않습니다 )', {'fields': ['payback']})
        ]
    readonly_fields = ['finalUpdtd']

admin.site.register(Annual, AnnualAdmin)
admin.site.register(AnnualDate, AnnualDateAdmin)
admin.site.register(MinusData, MinusAdmin)