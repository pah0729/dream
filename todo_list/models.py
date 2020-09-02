from django.db import models
from django.utils import timezone
from accounts.models import Profile, Team


# Create your models here.

class TodoList(models.Model):
    userName = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)


    # t_code = models.Team.t_code()
    date = models.DateField(verbose_name='등록일', default=timezone.now)
    content = models.TextField(verbose_name='내용')
    cmpltDate = models.DateField(verbose_name='완료일', null=True, blank=True)
    cmplt = models.BooleanField(verbose_name='체크', default=False)
    disp = models.IntegerField(verbose_name='순서', default=0)

    IMPORT_CHOICE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    important = models.CharField(
        verbose_name='중요도',
        max_length=2,
        choices=IMPORT_CHOICE,
        default='보통',
    )

    class Meta:
        verbose_name = 'To Do List'
        verbose_name_plural = 'To Do List 관리'

    def checkday(self):
        return (timezone.now().date() - self.date).days
