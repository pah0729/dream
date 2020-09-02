from django.db import models
# from accounts.models import Team
from accounts.models import Profile, Team
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Project(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(verbose_name='제목', max_length=50)
    content = models.TextField(verbose_name='내용')
    CONDITION_CHOICES = (
        ('대기', '대기'),
        ('중지', '중지'),
        ('완료', '완료'),
        ('진행', '진행')
    )
    condition = models.CharField(verbose_name='상태', choices=CONDITION_CHOICES, max_length=2, default='대기')
    # t_code = models.Team.t_code()
    targets = models.TextField(verbose_name='대상자',default='{}')
    sdate = models.DateField(verbose_name='시작일')
    edate = models.DateField(verbose_name='종료일')
    

    @property
    # def commentCount(self):
    #     cc = Comment.objects.filter(num=self.pk)
    #     commentCount = cc.count()
    #     return commentCount

    
    def progressBar(self):
        total = self.todo
        percent = 0
        if total.count() != 0:
            percent = int((total.filter(condition="완료").count()/total.count())*100)

        return percent
    
  
    def condition(self):

        myTodo = Todo.objects.select_related('num').filter(num=self.pk)

        if not myTodo.exists():
            self.condition="대기"
        elif not myTodo.exclude(condition="대기").exists():
            self.condition="대기"
        elif not myTodo.exclude(condition="완료").exists():
            self.condition="완료"
        elif not myTodo.exclude(condition="완료").exclude(condition="중지").exists():
            self.condition="중지"
        else:
            self.condition="진행"
        return self.condition

    def get_absolute_url(self):
        return reverse('project:todo_list', args=[self.pk])

    def __str__(self):
        return self.title + ' - ' + str(self.user)

    class Meta:
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트 관리'


class ProjectTarget(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
    num = models.ForeignKey(Project, verbose_name='프로젝트명', on_delete=models.CASCADE, related_name='project_target')
    read = models.BooleanField(verbose_name='읽음여부', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '프로젝트 대상자'
        verbose_name_plural = '프로젝트 대상자 관리'

class Todo(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
    num = models.ForeignKey(Project, verbose_name='프로젝트명', on_delete=models.CASCADE, null=True, blank=True, related_name='todo')
    targets = models.TextField(verbose_name='대상자', default='{}')
    content = models.TextField(verbose_name='내용')
    CONDITION_CHOICES = (
        ('대기', '대기'),
        ('중지', '중지'),
        ('완료', '완료'),
        ('진행', '진행')
    )
    condition = models.CharField(verbose_name='상태', choices=CONDITION_CHOICES, max_length=2, default='대기')
    IMPORT_CHOICES = (
        ('높음', '높음'),
        ('보통', '보통'),
        ('낮음', '낮음')
    )
    important = models.CharField(verbose_name='중요도', choices=IMPORT_CHOICES, max_length=2, default='보통')
    sdate = models.DateField(verbose_name='시작일')
    edate = models.DateField(verbose_name='종료일')
    complate = models.DateField(verbose_name='완료일', null=True, blank=True)
    
    def approve(self):
       self.approved_comment = True
       self.save()
       
    def __str(self):
       return self.content

    def get_absolute_url(self):
        return reverse('project:todo_detail', args=[self.pk])

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '프로젝트 하위업무'
        verbose_name_plural = '프로젝트 하위업무 관리'

class TodoTarget(models.Model):
    user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
    num = models.ForeignKey(Todo, verbose_name='업무지시자', on_delete=models.CASCADE)
    read = models.BooleanField(verbose_name='읽음여부', default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '프로젝트 하위업무 대상자'
        verbose_name_plural = '프로젝트 하위업무 대상자 관리'


class TodoComment(models.Model):
   user = models.ForeignKey(Profile, verbose_name='이름', on_delete=models.CASCADE, null=True, blank=True)
   content = models.TextField(verbose_name='내용')
   date = models.DateTimeField(default=timezone.now, verbose_name='등록날짜')
   num = models.ForeignKey(Todo, on_delete=models.CASCADE, verbose_name='구분코드')
   
   class Meta:
            verbose_name = '프로젝트 하위업무 코멘트'
            verbose_name_plural = '프로젝트 하위업무 코멘트 관리'

   def approve(self):
       self.approved_comment = True
       self.save()

   def __str__(self):
        return str(self.user)
        
    
