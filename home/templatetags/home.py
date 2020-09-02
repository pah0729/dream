from django import template
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Profile, Team
from notice.models import Notice, NoticeTarget
from todo_list.models import TodoList
from commute.models import Commute
from annual.models import Annual
from django.db import transaction
from project.models import Project
from django.db.models import Q
from django.views.generic import TemplateView
from datetime import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


register = template.Library()


@register.simple_tag
def get_profile_list():
    return Profile.objects.select_related('user').filter(user__is_superuser=False).exclude(user__is_active=False ).order_by('pk')


@register.simple_tag
def get_team_list():
    return Team.objects.all().order_by('-pk')


@register.simple_tag
def get_alluser_count():
    alluser = Profile.objects.select_related('user').filter(user__is_superuser = False, user__is_active=True).count()
    return alluser


@register.simple_tag
def get_attendance_count():
    alluser = Profile.objects.select_related('user').filter(user__is_superuser = False, user__is_active=True)
    commute_today = Commute.objects.select_related('user__user').filter(date_commute__year=date.today().year, date_commute__month=date.today().month, date_commute__day=date.today().day)
    annual_today = Annual.objects.select_related('user__user').filter(finalApproval=True, sdate__lte=date.today(), fdate__gte=date.today())
    
    alluser_count = alluser.count()
    attendance_count = 0 #출근
    leave_count = 0 #퇴근
    workout_count = 0 #외근
    annual_count = 0 #연차
    half_annual_count = 0 #반차
    absent_count = 0 #결근
    unregistered_count = 0 #미등록
    unregistered = []

    for user in alluser:
        commute = commute_today.filter(user=user)
        if commute.count() != 0:
            status = commute.last()
            if status.condition == '출근':
                attendance_count += 1
            elif status.condition == '퇴근':
                leave_count += 1
            elif status.condition == '외근':
                workout_count += 1
            elif status.condition == '복귀':
                attendance_count += 1
            elif status.condition == '연차':
                annual_count += 1
            elif status.condition == '오전반차':
                half_annual_count += 1
            elif status.condition == '오후반차':
                half_annual_count += 1
            elif status.condition == '결근':
                absent_count += 1

        else:
            annual = annual_today.filter(user=user)
            if annual.count() == 1:
                annual = annual_today.get(user=user)
                if annual.datediff >= 1:
                    annual_count += 1
                else:
                    unregistered_count += 1
                    unregistered.append(user.user.username)
            else:
                unregistered_count += 1
                unregistered.append(user.user.username)

    context = {
        'alluser_count':alluser_count,
        'attendance_count':attendance_count,
        'leave_count':leave_count,
        'workout_count':workout_count,
        'annual_count':annual_count,
        'half_annual_count':half_annual_count,
        'absent_count':absent_count,
        'unregistered':unregistered,
        'unregistered_count':unregistered_count,
        'etc':unregistered_count+absent_count
        }

    return context


@register.simple_tag(takes_context=True)
def get_notices(context):
    """ 공지사항 리스트 가져오기"""
    user = context['request'].user.profile
    notice_list = Notice.objects.select_related('user__user').filter(Q(targets__icontains=user)|Q(user=user)|Q(targets="전체선택")).order_by('-pk')
    paginator = Paginator(notice_list, 5)
    notices = paginator.page(1)
    return notices


@register.simple_tag(takes_context=True)
def get_projects(context):
    """ 프로젝트 리스트 가져오기"""
    user = context['request'].user.profile
    return Project.objects.select_related('user__user','team').filter(Q(targets__icontains=user.user.username)|Q(user=user)).order_by('-pk')

@register.simple_tag(takes_context=True)
def get_todoes(context):
    """ todolist 리스트 가져오기"""
    user = context['request'].user.profile
    return TodoList.objects.select_related('userName').filter(cmpltDate__isnull=True, userName=user).order_by('disp','-pk')


@register.simple_tag(takes_context=True)
def get_project_calendar(context):
    eventlist = Project.objects.select_related('user__user','team').all()
    return eventlist