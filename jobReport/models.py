from django.db import models
from datetime import *
from accounts.models import Profile, Team
# Create your models here.

class JobReport(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
    sdate = models.DateField(verbose_name='시작일')
    edate = models.DateField(verbose_name='종료일')
    bsnsD = models.DecimalField(verbose_name='업무일수', max_digits=3, decimal_places=1, null=True, blank=True)
    annual = models.DecimalField(verbose_name='연차', max_digits=3, decimal_places=1, null=True, blank=True)
    late = models.DecimalField(verbose_name='지각', max_digits=3, decimal_places=1, null=True, blank=True)
    important = models.TextField(verbose_name='중요사항', blank=True)
    incmp = models.TextField(verbose_name='차주계획', blank=True)
    etc = models.TextField(verbose_name='기타사항', null=True, blank=True)
    data = models.TextField(default='[]')
    week_data = models.CharField(verbose_name='주차', max_length=50, blank=True)

    class Meta:
        verbose_name = '주간업무보고서'
        verbose_name_plural = '주간업무보고서 관리'

    def __str__(self):
        return str(self.user)

    # 필드에 주차정보 넣기
    def week_save(self):
        firstday = date(self.sdate.year, self.sdate.month, 1)
        weekday = firstday.weekday()
        if weekday == 6:
            firstweek = int((6-weekday)+2)
        else:
            firstweek = int((6-weekday)+1)
        count = ""
        day = self.sdate.day
        if day <= firstweek :
            count = 1
        elif firstweek < day <= firstweek+7:
            count = 2
        elif firstweek+7 < day <= firstweek+14:
            count = 3
        elif firstweek+14 < day <= firstweek+21 :
            count = 4
        else :
            count = 5
        
        year = self.sdate.strftime("%Y")
        month = self.sdate.strftime("%m")
        week = year + "년 " + month + "월 " + str(count) + "주"
        self.week_data = week

    @property
    def week(self):
        # 시작일 기준 그 달의 첫째날
        firstday = date(self.sdate.year, self.sdate.month, 1)
        print(firstday)
        # 첫째날의 요일을 숫자로 반환
        weekday = firstday.weekday()
        print(weekday)
        # 첫주의 마지막날
        if weekday == 6:
            firstweek = int((6-weekday)+2)
        else:
            firstweek = int((6-weekday)+1)
        print(firstweek)
        count = ""
        day = self.sdate.day
        print(day)
        if day <= firstweek :
            count = 1
        elif firstweek < day <= firstweek+7:
            count = 2
        elif firstweek+7 < day <= firstweek+14:
            count = 3
        elif firstweek+14 < day <= firstweek+21 :
            count = 4
        else :
            count = 5
        week = str(self.sdate.year) + "년 " + str(self.sdate.month) + "월 " + str(count) + "주"
        return week


# class Daily(models.Model):
#     num = models.ForeignKey(JobReport, on_delete=models.CASCADE, null=True, blank=True)
#     daily_date = models.DateField(verbose_name='날짜')
#     goWork = models.TimeField(verbose_name='출근시간')
#     leaveWork = models.TimeField(verbose_name='퇴근시간')
#     content = models.TextField(verbose_name='업무내용')
