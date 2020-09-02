from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from .models import Profile, Team, Project, ProjectTarget, Todo, TodoTarget, TodoComment
from .forms import ProjectForm, ProjectTargetForm, TodoForm, TodoTargetForm, TodoCommentForm,ConditionForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from accounts import tasks
from django.contrib.sites.models import Site
from datetime import *
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

@login_required
def list3(request):
    user = request.user.profile
    
    if user.user.is_staff == True :
        project_list = Project.objects.prefetch_related('todo').select_related('user__user').all().order_by('-pk')
    else:
        project_list = Project.objects.prefetch_related('todo').select_related('user__user').filter(Q(targets__icontains=user)|Q(user=user)).order_by('-pk')
    
    # 리스트 페이지네이션
    
    
    query = request.GET.get('search')
    if query:
        project_list = (project_list.filter(Q (user__user__username__icontains=query) | Q (title__icontains=query))) or [i for i in project_list if query in i.condition()]
    total_len = len(project_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(project_list, 10)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = projects.number -1 # URL에서 ?page= 다음에 들어오는 숫
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])


    return render(request,'project/project_list.html',{'list': projects, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

@login_required
def new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            
            project.save()
            post = get_object_or_404(Project, pk=project.pk)
            form = ProjectTargetForm(request.POST)
            target = post.targets.split(',')
            for i in target :
                tg = form.save(commit=False)
                tg.pk = None
                tg.user = Profile.objects.get(user__username=i)
                tg.num = post
                tg.save()
                if tg.user.pushToken != '' and tg.user.notifySettings == True:
                    # celery task call pushbullet link or text
                    domain = Site.objects.get_current().domain
                    link = 'https://{domain}{url}'.format(domain=domain, url=project.get_absolute_url())
                    tasks.push_link.delay(**{"token": tg.user.pushToken, "title": "당신에게 새로운 프로젝트가 등록 되었습니다.", "url": link})

            messages.info(request, '등록이 완료되었습니다')
            return redirect('project:list')
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('project:list')
    else:
        form = ProjectForm()
    return render(request, 'project/project_new.html', {'form': form,'target' : Profile.objects.all().order_by('pk'), 'teams':Team.objects.all().order_by('pk')})
    
@login_required
def edit(request, pk):
    post = get_object_or_404(Project, pk=pk)
    user = request.user.profile
    if user == post.user or user.user.is_staff==True:
        if request.method == "POST":
            form = ProjectForm(request.POST, instance=post)
            if form.is_valid():
                project = form.save(commit=False)
                project.save()
                form = ProjectTargetForm(request.POST)
                target = post.targets.split(',')
                for i in target :
                    if  not ProjectTarget.objects.select_related('user__user').filter(num=post, user__user__username=i).exists() :
                        
                        tg = form.save(commit=False)
                        
                        tg.pk = None
                        
                        tg.user = Profile.objects.get(user__username=i)
                        
                        tg.num = post
                        
                        tg.save()
                        if tg.user.pushToken != '' and tg.user.notifySettings == True :
                            # celery task call pushbullet link or text
                            domain = Site.objects.get_current().domain
                            link = 'https://{domain}{url}'.format(domain=domain, url=project.get_absolute_url())
                            tasks.push_link.delay(**{"token": tg.user.pushToken, "title": "당신에게 새로운 프로젝트가 등록 되었습니다.", "url": link})
                            # push.push(tg.user,'새로운 공지 등록 되었습니다.',notice.title)

                messages.info(request, '수정이 완료되었습니다')
                return redirect('project:todo_list', pk)
            else :
                messages.error(request, '데이터가 유효하지 않습니다.')
                return redirect('project:todo_list', pk)
        else:
            form = ProjectForm(instance=post)
    else:
        messages.error(request, '권한이 없습니다.')
    return render(request, 'project/project_edit.html', {'form': form,'target' : Profile.objects.select_related('user', 'team').all().order_by('pk'), 'teams':Team.objects.all().order_by('pk'), 'pk':pk, 'post':post, 'target2':post.targets.split(',')})
    


@login_required
def todo(request, pk):
    
    post = get_object_or_404(Project, pk=pk)
    user= request.user.profile
    if (not Project.objects.filter(pk=post.pk, targets__icontains=user).exists()) and (not post.user==user) and (user.user.is_staff==False):
        messages.error(request, '접근 권한이 없습니다')
        return redirect('project:list')
    
    cd = request.GET.get('condition')
    if cd and cd=="전체":
        todo = Todo.objects.filter(num=post).order_by('-pk')
    elif cd :
        todo = Todo.objects.filter(num=post, condition=cd).order_by('-pk')
    else:
        todo=Todo.objects.filter(num=post).order_by('-pk')
        cd = '전체'
    
    

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user.profile
            todo.num = post
            todo.save()

            post1 = get_object_or_404(Todo, pk=todo.pk)
            form = TodoTargetForm(request.POST)
            target = post1.targets.split(',')
            for i in target :
                td = form.save(commit=False)
                td.pk = None
                td.user = Profile.objects.get(user__username=i)
                td.num = post1
                td.save()
                if td.user.pushToken != '' and td.user.notifySettings == True:
                    # celery task call pushbullet link or text
                    domain = Site.objects.get_current().domain
                    link = 'https://{domain}{url}'.format(domain=domain, url=todo.get_absolute_url())
                    tasks.push_link.delay(**{"token": td.user.pushToken, "title": "당신에게 새로운 프로젝트 Todo가 등록 되었습니다.", "url": link})
            messages.info(request, '등록이 완료되었습니다')
            return redirect('project:todo_list', pk)
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('project:todo_list', pk)
    else:
        form = TodoForm()
        target=[]
        for i in ProjectTarget.objects.filter(num=post).order_by('pk'):
            target.append(i.user)
       
    return render(request, 'project/todo_list.html', {'todo' : todo, 'cd':cd, 'post' : post, 'form': form, 'pk':pk, 'target' : target, 'teams':Team.objects.all().order_by('pk')})
   

@login_required
def detail(request, pk):
    post = get_object_or_404(Todo, pk=pk)
    user = request.user.profile
    if request.method =="POST":
        form1 = ConditionForm(request.POST, instance=post)
        if form1.is_valid():
            if  TodoTarget.objects.filter(num=post, user=user).exists() or user==post.user or user.user.is_staff==True:
                todo = form1.save(commit=False)
                if todo.condition == '완료':
                    todo.complate = date.today()

                todo.save()
                return redirect('project:todo_list',post.num.pk)
                
            else: 
                messages.error(request, '권한이 없습니다.')
            return redirect('project:todo_detail', pk)

    if request.method == "POST":
        form2 = TodoCommentForm(request.POST)
        if form2.is_valid():
            comment = form2.save(commit=False)
            comment.user = request.user.profile
            comment.num = post
            comment.save()
            if post.user.pushToken != '' and post.user.notifySettings == True:
                # celery task call pushbullet link or text
                domain = Site.objects.get_current().domain
                link = 'https://{domain}{url}'.format(domain=domain, url=post.get_absolute_url())
                tasks.push_link.delay(**{"token": post.user.pushToken, "title": "당신의 글에 새로운 댓글이 등록 되었습니다.", "url": link})
            target = post.targets.split(',')
            for i in target :
                if TodoTarget.objects.filter(num=post, user__user__username=i).exclude(user__pushToken = '').exists() :
                    todo = Profile.objects.get(user__username=i)
                    if todo.notifySettings == True:
                        # celery task call pushbullet link or text
                        domain = Site.objects.get_current().domain
                        link = 'https://{domain}{url}'.format(domain=domain, url=post.get_absolute_url())
                        tasks.push_link.delay(**{"token": todo.pushToken, "title": "당신의 todo에 새로운 댓글이 등록 되었습니다.", "url": link})
                        # push.push(tg.user,'새로운 공지 등록 되었습니다.',notice.title)

                # push.push(tg.user,'새로운 공지 등록 되었습니다.',notice.title)
            
            return redirect('project:todo_detail', pk)
    else:
        form2 = TodoCommentForm()
    return render(request, 'project/todo_detail.html', {'detail': TodoComment.objects.filter(num=post).order_by('pk'), 'post':post})


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'project_calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['eventlist'] = Project.objects.all()
        return context

@login_required
def stop(request, pk):
    post = get_object_or_404(Project, pk=pk)
    user = request.user.profile
    if user == post.user or user.user.is_staff==True:
        todo = Todo.objects.filter(num=post).exclude(condition='완료')
        for i in todo:
            i.condition = '중지'
            i.save()
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('project:list')

@login_required
def indvd(request):
    viewtodo = request.GET.get('todo')
    user=request.user.profile
    if viewtodo and viewtodo =="작성자":
        todo = Todo.objects.filter(user=user, condition="진행").order_by('-pk')
    elif viewtodo and viewtodo =="오늘(작성자)" :
        todo = Todo.objects.filter(user=user, condition="진행", sdate__lte=date.today(), edate__gte=date.today()).order_by('-pk')
    elif viewtodo and viewtodo =="오늘(대상자)" :
        todo = Todo.objects.filter(targets__icontains=user, condition="진행", sdate__lte=date.today(), edate__gte=date.today()).order_by('-pk')
    else:
        todo=Todo.objects.filter(targets__icontains=user, condition="진행").order_by('-pk')
        viewtodo = '대상자'
    return render(request, 'project/indvd.html', {'todo':todo,'viewtodo':viewtodo})



@login_required
def history(request):
    todo_history = Todo.objects.select_related('user__user').filter(condition="완료").order_by('-pk')
    query = request.GET.get('search')

    if query:
        todo_history = todo_history.filter(Q (user__user__username__icontains=query) | Q (targets__icontains=query) | Q (content__icontains=query) | Q (sdate__icontains=query) | Q (important__icontains=query) | Q (edate__icontains=query))

    total_len = len(todo_history)
    page = request.GET.get('page', 1)
    paginator = Paginator(todo_history, 10)
    try:
        historys = paginator.page(page)
    except PageNotAnInteger:
        historys = paginator.page(1)
    except EmptyPage:
        historys = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = historys.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    context = {
        'list' : historys,
        'page_range': page_range,
        'total_len' : total_len,
        'max_index' : max_index-2,
    }
    return render(request, 'project/history.html', context)


