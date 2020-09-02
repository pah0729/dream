from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoList, Profile, Team
from .forms import NewForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import requires_csrf_token, csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.

@login_required
@requires_csrf_token
def todolist(request):
    #투두리스트 작성
    if request.method=="POST":
        form = NewForm(request.POST)
        if form.is_valid():
            todolist = form.save(commit=False)
            todolist.userName = request.user.profile
            todolist.team = request.user.profile.team
            todolist.save()
            messages.success(request, '추가되었습니다.')
            return redirect('todo_list:todolist')
        else:
            form = NewForm()

    #sortable 리스트 정렬
    with transaction.atomic():
        for index, todolist_pk in enumerate(request.POST.getlist("todolist[]")):
            todolist = get_object_or_404(TodoList, pk=todolist_pk)
            todolist.disp = index
            todolist.save()
    
    viewteam = ''
    #팀 투두 필터
    if request.GET.get('team'):
        teamfilter = request.GET.get('team')
        viewteam = teamfilter
        todoteamlist = TodoList.objects.select_related('userName__user','team').filter(cmpltDate__isnull=True, team__name=teamfilter).order_by('important')
    else:
        viewteam = request.user.profile.team.name
        todoteamlist = TodoList.objects.select_related('userName__user','team').filter(cmpltDate__isnull=True, team__name=request.user.profile.team).order_by('important')

    todolist = TodoList.objects.select_related('userName__user','team').filter(cmpltDate__isnull=True, userName=request.user.profile).order_by('disp','-pk')
    teamlist = TodoList.objects.values_list('team__name',flat=True).distinct()
    context = {
        'todolist' : todolist,
        'todoteamlist' : todoteamlist,
        'teamlist' : teamlist,
        'viewteam' : viewteam
    }
    return render(request,'todo_list/todolist.html', context)

#히스토리
@login_required
def todohistory(request):
    # 리스트 페이지네이션
    todohistory = TodoList.objects.select_related('userName__user','team').filter(cmpltDate__isnull=False).order_by('-cmpltDate')
    search = request.GET.get('search')
    if search:
        todohistory = todohistory.filter(Q (userName__user__username__icontains=search) | Q (content__icontains=search) | Q (cmpltDate__icontains=search) | Q (date__icontains=search) | Q (team__name__icontains=search))
    total_len = len(todohistory)
    page = request.GET.get('page', 1)
    paginator = Paginator(todohistory, 10)
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = history.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    context = {
        'todohistory' : history,
        'page_range': page_range,
        'total_len' : total_len,
        'max_index' : max_index-2,
    }
    return render(request,'todo_list/todohistory.html', context)
#제거
@login_required
def todoremove(request, pk):
    todoremove = get_object_or_404(TodoList, pk=pk)
    if request.user.profile == todoremove.userName:
        todoremove.delete()
        messages.error(request, 'TO-DO 삭제 완료')
        return redirect('todo_list:todolist')
    else:
        messages.error(request, '타인의 TO-DO는 삭제할 수 없습니다')
        return redirect('todo_list:todolist')
    
#히스토리에서 복구
@login_required
def todorecovery(request,pk):
    todorecovery = get_object_or_404(TodoList, pk=pk)

    if request.user.profile == todorecovery.userName:
        todorecovery.cmpltDate = None
        todorecovery.save()
        messages.success(request, 'TO-DO가 복구되었습니다.')
        return redirect('todo_list:todohistory')
    else:
        messages.error(request,'타인의 TO-DO는 복구할 수 없습니다')
        return redirect('todo_list:todohistory')

#완료
@login_required
def todocmplt(request, pk):
    todocmplt = get_object_or_404(TodoList, pk=pk)

    if request.user.profile == todocmplt.userName:
        todocmplt.cmplt = True
        todocmplt.cmpltDate = timezone.now()
        todocmplt.save()
        messages.success(request, 'TO-DO가 완료되었습니다.')
        return redirect('todo_list:todolist')
    else:
        messages.error(request,'타인의 TO-DO는 완료할 수 없습니다.')
        return redirect('todo_list:todolist')