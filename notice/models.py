from django.db import models
from accounts.models import Profile, Team
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import re

# Create your models here.

class Notice(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True, related_name='notices')
    team = models.ForeignKey(Team, verbose_name='팀', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='제목', max_length=50)
    content = RichTextUploadingField(verbose_name="내용")
    hashtag = models.CharField(verbose_name='해시태그', max_length=50, blank=True)
    tag_set = models.ManyToManyField('Tag', blank=True, verbose_name='태그')
    file1 = models.FileField(verbose_name='파일', blank=True)
    file2 = models.FileField(verbose_name='파일', blank=True)
    file3 = models.FileField(verbose_name='파일', blank=True)
    file4 = models.FileField(verbose_name='파일', blank=True)
    file5 = models.FileField(verbose_name='파일', blank=True)
    targets = models.TextField(verbose_name='대상자',default='{}')
    date = models.DateTimeField(verbose_name='등록일', default=timezone.now)
    mdfdate = models.DateTimeField(verbose_name='수정일', null=True, blank=True)
    IMPORT_CHOICES = (
        ('높음', '높음'),
        ('보통', '보통'),
        ('낮음', '낮음')
    )
    important = models.CharField(verbose_name='중요도', choices=IMPORT_CHOICES, max_length=2, default='보통')

    def __str__(self):
        return self.title + ' - ' + str(self.user)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항 관리'

    @property
    def commentCount(self):
        return self.comment_set.count()

    def get_absolute_url(self):
        return reverse('notice:detail', args=[self.pk])

    @property
    def progressBar(self):
        total = self.target_set
        total = total.filter(user__user__is_active=True)
        read = total.filter(read=True, user__user__is_active=True).count()
        return int((read/total.count())*100)

    # NOTE: hashtag에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.hashtag)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(name=t)
            self.tag_set.add(tag)  # NOTE: ManyToManyField 에 인스턴스 추가

class Tag(models.Model):
    name = models.CharField(verbose_name='태그이름', max_length=140, unique=True)

    class Meta:
        verbose_name = '공지사항 태그'
        verbose_name_plural = '공지사항 태그 관리'

    def __str__(self):
        return self.name


class NoticeTarget(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True, related_name='notice_target_set')
    num = models.ForeignKey(Notice, verbose_name='공지사항 구분', on_delete=models.CASCADE,related_name='target_set')
    read = models.BooleanField(verbose_name='읽음여부', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '공지사항 대상자'
        verbose_name_plural = '공지사항 대상자 관리'



class Comment(models.Model):
   user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
   content = models.TextField(verbose_name='내용')
   date = models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
   num = models.ForeignKey(Notice, on_delete=models.CASCADE, verbose_name='구분코드',related_name='comment_set')

   class Meta:
        verbose_name = '공지사항 코멘트'
        verbose_name_plural = '공지사항 코멘트 관리'

   def approve(self):
       self.approved_comment = True
       self.save()

   def __str__(self):
        return str(self.content)

class CaseManagement(models.Model):
    user = models.ForeignKey(Profile, verbose_name='게시자', on_delete=models.CASCADE, null=True, blank=True, related_name='cases')
    title = models.CharField(verbose_name='제목', max_length=50)
    content = RichTextUploadingField(verbose_name="내용")
    hashtag = models.CharField(verbose_name='해시태그', max_length=50, blank=True)
    tag_set = models.ManyToManyField('CaseTag', blank=True, verbose_name='태그')
    date = models.DateTimeField(verbose_name='등록일', auto_now_add=True)
    mdfdate = models.DateTimeField(verbose_name='수정일', null=True, blank=True)

    def __str__(self):
        return self.title + ' - ' + str(self.user)

    class Meta:
        verbose_name = '사례'
        verbose_name_plural = '사례관리'

    # NOTE: hashtag에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.hashtag)

        if not tags:
            return

        for t in tags:
            tag, tag_created = CaseTag.objects.get_or_create(name=t)
            self.tag_set.add(tag)  # NOTE: ManyToManyField 에 인스턴스 추가

class CaseTag(models.Model):
    name = models.CharField(verbose_name='태그이름', max_length=140, unique=True)

    class Meta:
        verbose_name = '사례관리 태그'
        verbose_name_plural = '사례관리 태그 관리'

    def __str__(self):
        return self.name