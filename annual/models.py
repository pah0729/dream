from django.db import models
from accounts.models import Profile, Team, Position, AnnualApprovalLine
from commute.models import Commute
from django.utils import timezone
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.urls import reverse

# 연차신청 모델
class Annual(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True, related_name='annuals')
    team = models.ForeignKey(Team, verbose_name='팀', on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, verbose_name='직급', on_delete=models.CASCADE, null=True, blank=True)
    DIVISION_CHOICES = (
        ('연차', '연차'),
        ('대체휴무', '대체휴무'),
        ('기타', '기타'),
    )
    division = models.CharField(verbose_name='휴가구분', max_length=5, choices=DIVISION_CHOICES, default='연차')
    divreason = models.CharField(verbose_name='휴가구분:기타', max_length=20, null=True, blank=True)
    sdate = models.DateField(verbose_name='시작일')
    fdate = models.DateField(verbose_name='종료일')
    datediff = models.DecimalField(verbose_name='일수', max_digits=3, decimal_places=1, default=0)
    reason = models.TextField(verbose_name='사유')
    local = models.CharField(verbose_name='휴가지역', max_length=20)
    relationship = models.CharField(verbose_name='관계', max_length=20, default='')
    network = models.CharField(verbose_name='비상연락처', max_length=20)
    remark = models.TextField(verbose_name='비고')
    finalApproval = models.BooleanField(verbose_name='최종승인여부', default=False)
    step = models.ForeignKey(AnnualApprovalLine, verbose_name='결재자', on_delete=models.SET_NULL, blank=True, null=True)
    STATUS_ANNUAL_CHOICES = (
        ('대기', '대기'),
        ('반려', '반려'),
        ('승인', '승인'),
    )
    status = models.CharField(verbose_name='상태', max_length=2, choices=STATUS_ANNUAL_CHOICES, default='대기')
    return_reason = models.CharField(verbose_name='반려 사유', max_length=50, null=True, blank=True)
    teamleader = models.CharField(verbose_name='팀장 결재자', max_length=20, null=True, blank=True)
    teamleader_comment = models.CharField(verbose_name='팀장 코멘트', max_length=20, null=True, blank=True)
    chief = models.CharField(verbose_name='실장 결재자', max_length=20, null=True, blank=True)
    chief_comment = models.CharField(verbose_name='실장 코멘트', max_length=20, null=True, blank=True)
    director_office = models.CharField(verbose_name='사무국장 결재자', max_length=20, null=True, blank=True)
    director_office_comment = models.CharField(verbose_name='사무국장 코멘트', max_length=20, null=True, blank=True)
    director_center = models.CharField(verbose_name='센터장 결재자', max_length=20, null=True, blank=True)
    director_center_comment = models.CharField(verbose_name='센터장 코멘트', max_length=20, null=True, blank=True)
    create = models.DateTimeField(verbose_name='신청일', default=datetime.now)
    file = models.FileField(verbose_name='첨부서류', blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '연차 신청'
        verbose_name_plural = '연차 신청 관리'

    # 최종승인 완료된 연차 오브젝트 가져오기
    @staticmethod
    def get_annual_day(day):
        return  Annual.objects.filter(finalApproval=True, division='연차', sdate__lte=day, fdate__gte=day)

    # 최종승인 완료된 대체휴무 오브젝트 가져오기
    @staticmethod
    def get_annual_altrn_day(day):
        return  Annual.objects.filter(finalApproval=True, division='대체휴무', sdate__lte=day, fdate__gte=day)

    # 최종승인 완료된 기타휴무 오브젝트 가져오기
    @staticmethod
    def get_annual_etc_day(day):
        return  Annual.objects.filter(finalApproval=True, division='기타', sdate__lte=day, fdate__gte=day)

    def get_absolute_url(self):
        return reverse('annual:confirm', args=[self.pk])

# 연차 모델
class AnnualDate(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True, related_name='annualdates')
    ocrncDate = models.DateField(verbose_name='발생일', default=date.today)
    extncDate = models.DateField(verbose_name='소멸일', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='사용여부', default=False)
    is_delete = models.BooleanField(verbose_name='자동소멸', default=False)
    finalUpdtd= models.DateField(verbose_name='사용일', null=True, blank=True)
    memo = models.CharField(verbose_name='발생사유', max_length=20 , default='자동발생')

    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name = '연차'
        verbose_name_plural = '연차 관리'

    # 사용 가능한 연차 체크
    @staticmethod
    def get_user_annualDate(user):
        return AnnualDate.objects.filter(user=user, is_active=False, is_delete=False)

    # 반차 발생 (연차 발생시 2번실행)
    @staticmethod
    def pull_ocrnc(user, date):
        return AnnualDate.objects.create(user=user, ocrncDate=date.today(), memo='자동발생')

    # 연차 소멸일 자동입력
    @property
    def extncDate_save(self):
        """
        * 이 함수를 call 했을 때, 자동으로 소멸일이 갱신됨.

        ** 2020년 근로기준법 변경사항 :
        3월 31일 이후에 근속연수 만 1년 미만에 월 단위로 발생한 연차는 
        근속연수가 만 1년이 되는 날에 전부 소멸한다.

        *** 사용한 곳 : plus_manage.html --> 템플릿 태그 (페이지 접속시 함수 실행됨)
        """
        user = self.user
        ocrncDate = self.ocrncDate
        startDate = date(2020,3,31)  # 근로기준법 적용일
        tenures = int(((ocrncDate - user.entry_date).days + 1) / 365)
        # 근속 1년 미만일 때 발생한 연차인지 판단
        if tenures < 1:  # 1년미만 월차 일 경우
            if ocrncDate < startDate:  # 개정일 전 발생연차 (발생일+1년)
                self.extncDate = self.ocrncDate + relativedelta(years=1)
                self.save()
                return self.ocrncDate + relativedelta(years=1)
            if ocrncDate >= startDate:  # 개정일 이후 발생연차 (입사일+1년)
                self.extncDate = user.entry_date + relativedelta(years=1)
                self.save()
                return user.entry_date + relativedelta(years=1)
        else:  # 근속 만1년 이상일 때 (발생일+1년)
            self.extncDate = self.ocrncDate + relativedelta(years=1)
            self.save()
            return ocrncDate + relativedelta(years=1)
    extncDate_save.fget.short_description = '소멸일'

    # 연차 소멸체크
    @staticmethod
    def get_extnc(date):
        return AnnualDate.objects.filter(is_active=False, is_delete=False, extncDate__lte = date)

    # 연차 개수 카운트
    @property
    def annualcal(self):
        if self.is_active == False and self.is_delete == False :
            return float(0.5)
        else:
            return float(0.0)
    annualcal.fget.short_description = '연차개수'

# 마이너스 연차 모델
class MinusData(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True, related_name='minusdatas')
    ocrncDate = models.DateField(verbose_name='발생일')
    payback = models.BooleanField(verbose_name='삭감여부', default=False)
    finalUpdtd= models.DateField(verbose_name='최종업데이트', auto_now=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '연차 마이너스'
        verbose_name_plural = '연차 마이너스 관리'

    # 마이너스 반차 생성 (마이너스 연차시 2번실행)
    @staticmethod
    def pull_minusData(user, date):
        return MinusData.objects.create(user=user, ocrncDate=date.today())

    # 마이너스연차 개수 카운트
    @property
    def minuscal(self):
        if self.payback == False :
            return float(0.5)
        else:
            return float(0.0)
    minuscal.fget.short_description = '마이너스개수'