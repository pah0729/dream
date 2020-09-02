from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Profile

# Create your models here.


class UserLoginLog(models.Model):
    """ 로그인 시 기록을 남기기 위한 """
    user = models.ForeignKey(
        get_user_model(),
        verbose_name='User',
        related_name='+',  # 추후 퍼포먼스를 위해
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField(
        default='192.168.0.1',
        verbose_name='IP Address',
        null=True
    )
    user_agent = models.CharField(
        verbose_name='HTTP User Agent',
        default='',
        max_length=300,
    )
    created_at = models.DateTimeField('login time', auto_now_add=True)

    class Meta:
        verbose_name = '로그인 기록'
        verbose_name_plural = '로그인 기록 관리'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s %s' % (self.user, self.ip_address)

    @staticmethod
    def get_logs_by_user(sid):
        return UserLoginLog.objects.filter(user__pk=sid)


class AcesStts(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE,
                             blank=True, null=True, related_name='acesstts_set')
    date = models.DateTimeField(verbose_name='접속날짜', default=timezone.now)

    class Meta:
        verbose_name = '접속통계 데이터'
        verbose_name_plural = '접속통계 데이터 관리'

    def __str__(self):
        return str(self.user)

    @staticmethod
    def is_acesStts(user, sdate, edate):
        return AcesStts.objects.select_related('user__user').filter(user=user, date__date__range=(sdate, edate)).count()
