from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Team(models.Model):
   name = models.CharField(verbose_name='팀명', max_length=20, unique=True)
   memo = models.CharField(verbose_name='메모', max_length=50, blank=True, null=True)

   def __str__(self):
       return self.name

   class Meta:
       verbose_name = '조직'
       verbose_name_plural = '조직 관리'

class TeamRelationship(models.Model):
   source = models.ForeignKey(Team, verbose_name='대상조직', on_delete=models.CASCADE, related_name='subs')
   parent = models.ForeignKey(Team, verbose_name='상위조직', on_delete=models.CASCADE, blank=True, null=True)
   display = models.IntegerField(verbose_name='화면표시순서', default=999)

   class Meta:
       verbose_name = '조직 관계'
       verbose_name_plural = '조직도 관리'

   def __str__(self):
       return '%s - 상위부서:%s' % (self.source.name, self.parent if self.parent else '없음(최상위)')

   def save(self, *args, **kwargs):
       if TeamRelationship.objects.filter(source=self.parent,parent=self.source).exists():
           raise Exception('Infinite repetition(무한반복)')
       super(TeamRelationship, self).save(*args, **kwargs)

class Position(models.Model):
   name = models.CharField(verbose_name='직급', max_length=10, unique=True)

   def __str__(self):
       return self.name

   class Meta:
       verbose_name = '직급'
       verbose_name_plural = '직급 관리'

class Belong(models.Model):
   name = models.CharField(verbose_name='소속', max_length=6, unique=True)

   def __str__(self):
       return self.name

   class Meta:
       verbose_name = '소속'
       verbose_name_plural = '소속 관리'

class Profile(models.Model):
   user = models.OneToOneField(User, verbose_name='이름', on_delete=models.CASCADE, blank=True, null=True)
   userNum = models.CharField(verbose_name='사번', max_length=8, blank=True)
   userImg = models.ImageField(verbose_name='사진', upload_to='profile_images', default='default_img.png')
   team = models.ForeignKey(Team, verbose_name='팀', on_delete=models.SET_NULL, blank=True, null=True)
   position = models.ForeignKey(Position, verbose_name='직급', on_delete=models.SET_NULL, null=True, blank=True)
   email_google = models.CharField(verbose_name='구글메일', max_length=256, blank=True, unique=True)
   email = models.CharField(verbose_name='개인메일', max_length=256, blank=True)
   phone = models.CharField(verbose_name='연락처', max_length=20, null=True, blank=True)
   entry_date = models.DateField(verbose_name='입사일')
   residentNumber = models.CharField(verbose_name='주민등록번호',max_length=20, blank=True)
   pushToken = models.CharField(verbose_name='푸시토큰', max_length=256, blank=True, default='')
   belong = models.ForeignKey(Belong, verbose_name='소속회사', on_delete=models.SET_NULL, blank=True, null=True)
   notifySettings = models.BooleanField(verbose_name='알림수신여부', default=True)
   really_address = models.CharField(verbose_name='실거주주소', max_length=200, null=True, blank=True)
   address = models.CharField(verbose_name='등본상주소', max_length=200, null=True, blank=True)
   emergency_phone = models.CharField(verbose_name='비상연락처', max_length=20, null=True, blank=True)

   class Meta:
       verbose_name = '프로필'
       verbose_name_plural = '프로필 관리'

   @property
   def get_tenures(self):
       return int(((date.today() - self.entry_date).days + 1) / 365)

   def __str__(self):
       # return self.user
       return str(self.user) if self.user else ''

class AnnualApprovalLine(models.Model):
   manager = models.ForeignKey(Profile,verbose_name='담당자', on_delete=models.CASCADE, related_name='manager')
   approval = models.ForeignKey(Profile, verbose_name='결재자', on_delete=models.SET_NULL, blank=True, null=True, related_name='approval')

   class Meta:
       verbose_name = '연차 결재선'
       verbose_name_plural = '연차 결재선 관리'

   def __str__(self):
       return '연차결재선 - 담당자:%s -> 결재자:%s' % (self.manager, self.approval)

   def save(self, *args, **kwargs):
       if AnnualApprovalLine.objects.filter(manager=self.approval, approval=self.manager).exists():
           raise Exception('Infinite repetition(무한반복)')
       super(AnnualApprovalLine, self).save(*args, **kwargs)