from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from .models import JobReport, Profile
from .forms import JobReportForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests, json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def jobreport_list(request):
    team = request.GET.get('team')
    year = request.GET.get('year')
    month = request.GET.get('month')
    week = request.GET.get('week')

    jobreport_list =  JobReport.objects.select_related('user__user', 'user__team').all().order_by('-week_data', '-pk')

    if team and not year and not month and not week:
        if team == '전체':
            jobreport_list =  JobReport.objects.select_related('user__user', 'user__team').all().order_by('-week_data', '-pk')
        else:
            jobreport_list =  JobReport.objects.select_related('user__user', 'user__team').filter(user__team=team).order_by('-week_data', '-pk')
    elif team and year and month and week:
        week_data = year+' '+month+' '+week
        if team == '전체':
            jobreport_list =  JobReport.objects.select_related('user__user', 'user__team').filter(week_data=week_data).order_by('-week_data', '-pk')
        else:
            jobreport_list =  JobReport.objects.select_related('user__user', 'user__team').filter(user__team=team, week_data=week_data).order_by('-week_data', '-pk')
    
    # 리스트 페이지네이션
    query = request.GET.get('search')
    if query:
        jobreport_list = (JobReport.objects.filter(Q (user__user__username__icontains=query) | Q (user__team__name__icontains=query))) or [i for i in jobreport_list if query in i.week]
    total_len = len(jobreport_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(jobreport_list, 20)
    try:
        jobreports = paginator.page(page)
    except PageNotAnInteger:
        jobreports = paginator.page(1)
    except EmptyPage:
        jobreports = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = jobreports.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request,'jobReport/list.html',{'list': jobreports, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

@login_required
def new(request):
    user = request.user.profile
    if request.method == "POST":
        form = JobReportForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = user
            job.week_save()
            job.save()
            messages.info(request, '등록이 완료되었습니다')
            return redirect('jobreport:list')
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('jobreport:list')
    else:
        form = JobReportForm
        
    return render(request, 'jobReport/new.html', {'form':form})

@login_required
def detail(request, pk):
    post = get_object_or_404(JobReport, pk=pk)
    return render(request,'jobReport/detail.html',{'post' : post})


@login_required
def edit(request, pk):
    post = get_object_or_404(JobReport, pk=pk)
    user = request.user.profile
    if user == post.user or user.user.is_staff==True:
        if request.method == "POST":
            form = JobReportForm(request.POST, instance=post)
            if form.is_valid():
                jobreport = form.save(commit=False)
                jobreport.week_save()
                jobreport.save()
                messages.info(request, '수정이 완료되었습니다')
                return redirect('jobreport:detail', pk)
            else :
                messages.error(request, '데이터가 유효하지 않습니다.')
                return redirect('jobreport:detail', pk)
        else:
            form = JobReportForm(instance=post)
    else:
        messages.error(request, '권한이 없습니다.')
    return render(request, 'jobReport/edit.html', {'form': form, 'pk':pk, 'post':post})
    