from django.db import models
from django.utils import timezone
from accounts.models import Profile


# Create your models here.
class Commute(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)

    date_commute = models.DateTimeField(verbose_name='날짜 및 시간', default=timezone.now ,null=True, blank=True)

    CONDITION_CHOICE = (
        ('출근', '출근'),
        ('퇴근', '퇴근'),
        ('외근', '외근'),
        ('연차', '연차'),
        ('오전반차', '오전반차'),
        ('오후반차', '오후반차'),
        ('결근', '결근'),
        ('복귀', '복귀'),
    )

    condition = models.CharField(verbose_name='상태', choices=CONDITION_CHOICE, default='출근', max_length=10)
    reason = models.CharField(verbose_name='사유', max_length=30, blank=True)
    local = models.CharField(verbose_name='위치', max_length=100)

    class Meta:
        verbose_name = '출퇴근'
        verbose_name_plural = '출퇴근 관리'

    def __str__(self):
        return str(self.user)

   
    @staticmethod
    def is_absenteeism(user, sdate, edate):
        return Commute.objects.filter(user=user, condition="결근", date_commute__date__range=(sdate, edate)).count()