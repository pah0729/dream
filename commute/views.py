from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Commute, Profile
from annual.models import Annual
from .forms import CommuteForm, CommuteAdForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils import formats

# Create your views here.

@login_required
def commute_list(request):

    # 리스트 페이지네이션
    commute_list = Commute.objects.select_related('user__user').all().order_by('-date_commute')
    query = request.GET.get('search')
    if query:
        commute_list = Commute.objects.filter(Q (user__user__username__icontains=query) | Q (condition__icontains=query) | Q (date_commute__icontains=query)).order_by('-date_commute')
    total_len = len(commute_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(commute_list, 10)
    try:
        commutes = paginator.page(page)
    except PageNotAnInteger:
        commutes = paginator.page(1)
    except EmptyPage:
        commutes = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = commutes.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    user = request.user.profile
    half = Annual.objects.filter(user=user, finalApproval=True, sdate__lte=date.today(), fdate__gte=date.today(), datediff="0.5")
    today_commute = Commute.objects.select_related('user__user').filter(Q(condition="오전반차")|Q(condition="오후반차"), user=user, date_commute__date=date.today())
    if request.method == "POST":
        form = CommuteForm(request.POST)
        if form.is_valid():
            commute = form.save(commit=False)
            commute.user= user
            # 동일한 기록이 있고 외근이 아닐때
            if Commute.objects.select_related('user__user').filter(user=commute.user, date_commute__date=date.today(), condition=commute.condition).exists() and commute.condition != "외근"  and commute.condition != "복귀":
                messages.warning(request, '이미 등록하셨습니다!') 
            # 결근 등록 후 다른 기록을 등록할 때
            elif Commute.objects.select_related('user__user').filter(user=commute.user, date_commute__date=date.today(), condition="결근").exists():
                messages.warning(request, '이미 결근처리되었습니다')
            # 다른 기록을 등록 후 결근을 등록할 때
            elif Commute.objects.select_related('user__user').filter(user=commute.user, date_commute__date=date.today()).exists() and commute.condition=="결근":
                messages.warning(request, '이미 등록된 다른 기록이 있습니다.')
            # 휴가원 없이 반차 등록할 때
            elif (commute.condition == "오전반차" or commute.condition == "오후반차") and (not Annual.objects.filter(user=commute.user, finalApproval=True, sdate__lte=date.today(), fdate__gte=date.today()).exists()):
                messages.warning(request, '사전에 제출된 휴가원이 없습니다. 당일 사용시 관리자에게 요청하세요')
            # 반차 등록을 했는데 또 등록할 때
            elif (commute.condition == "오전반차" or commute.condition == "오후반차") and (Commute.objects.select_related('user__user').filter((Q(condition="오전반차")|Q(condition="오후반차")), user=commute.user, date_commute__date=date.today()).exists()):
                messages.warning(request, '이미 반차 등록을 하셨습니다.')
            # 출근 등록을 안하고 퇴근을 등록할 때
            elif (not Commute.objects.select_related('user__user').filter(user=commute.user, date_commute__date=date.today(), condition="출근").exists()) and commute.condition == "퇴근":
                messages.warning(request, '출근이 등록되지 않았습니다')
            else:
                commute.save()
                messages.success(request, '등록이 완료되었습니다.')
            return redirect('commute:list')
    else:
        form = CommuteForm()
    return render(request,'commute/list.html',{'list': commutes, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2, 'form':form, 'half':half, 'today_commute':today_commute})

@login_required
def detail_ajax(request):
    if request.method == "GET":
        pk = request.GET.get("pk")
        try:
            post = Commute.objects.get(pk=pk)
        except:
            return render(request, 'commute/list.html', {"success":False}, status=400)
        date = post.date_commute + timezone.timedelta(hours=9)
        date_format = formats.date_format(date, "SHORT_DATETIME_FORMAT")
        data = {
            'pk': post.pk,
            'user': post.user.user.username,
            'date_commute': date_format,
            'condition':post.condition,
            'reason':post.reason,
            'local':post.local,
        }
        return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii': False}, status=200)
    return render(request, 'commute/list.html',{"success":False}, status=400)

@login_required
def detail(request, pk):
    post = get_object_or_404(Commute, pk=pk)
    
    return render(request, 'commute/detail.html', {'post' : post})

def new(request):
    return render(request, 'commute/list.html')

@login_required
def absenteeism(request):
    user= request.user.profile
    if user.user.is_staff == False :
        messages.error(request, '접근 권한이 없습니다.')
        return redirect('main')

    if request.method == "POST":
        uu = request.POST['userName']
        uuu = Profile.objects.get(user__username=uu)
        form = CommuteAdForm(request.POST)
        if form.is_valid():
            
            cmad = form.save(commit=False)
            cmad.user = uuu
            
            cmad.condition = "결근"
            cmad.reason = "-"
            cmad.local = "39.0287452, 125.7583873"
            cmad.save()
            messages.success(request, '결근 처리되었습니다.')
            return redirect('commute:absenteeism')
    else : 
        commute_list = []
        aa = []
        absenteeism = []
        for i in Profile.objects.filter(user__is_superuser = False, user__is_active=True):
            if not Commute.objects.select_related('user__user').filter(user=i, date_commute__date=date.today()).count():
                ab = "x"
                if Annual.objects.select_related('user__user').filter(user=i, finalApproval=True, sdate__lte=date.today(), fdate__gte=date.today()).exists():
                    ab = "o"
                aa.append(ab)
                commute_list.append(i)
                ss = zip(commute_list, aa)
                absenteeism = ([i for i in ss])
    
       

    return render(request,'commute/absenteeism.html',{'commute_list':commute_list, 'absenteeism':absenteeism})