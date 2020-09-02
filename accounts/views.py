from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Profile, Team , Position, AnnualApprovalLine
from annual.models import AnnualDate, MinusData
from accounts.forms import EditUserForm, RegisterForm, NotifyForm, manageForm, AnnualApprovalLineForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import  HttpResponse, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import requires_csrf_token, csrf_protect
import json
from accounts import tasks
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@login_required
def profile(request):
    cal = 0 
    for i in AnnualDate.objects.filter(user=request.user.profile) : 
        cal += i.annualcal
    for j in MinusData.objects.filter(user=request.user.profile) :
        cal -= j.minuscal
    annualtotal = cal

    stype = request.POST.get("type")
    if request.method=="POST":
        if stype == "set":
            setting = request.POST.get('setting')
            user = request.user.profile
            user.notifySettings = setting
            user.save()
            return JsonResponse({'result': user.notifySettings })
        elif stype == "tok":
            token = request.POST.get('pushToken')
            user = request.user.profile
            user.pushToken = token
            user.save()
            return JsonResponse({'result': 'ok' })

    return render(request,'accounts/myProfile.html',{'profile' : request.user.profile, 'annualtotal':annualtotal})

@login_required
def orgChart(request):
    team = Team.objects.all()
    user = Profile.objects.filter(user__is_active=True).exclude(user__username='admin').order_by('entry_date')
    return render(request,'accounts/orgchart.html',{'user':user, 'team':team})

@login_required
def targetPopup(request):
    return render(request,'accounts/target.html',{})

@login_required
def modifiedProfile(request):
    ctx = {}
    if request.method == "GET":
        edituser_form = EditUserForm(instance=request.user.profile)
        ctx.update({"form":edituser_form})
    elif request.method == "POST":
            edituser_form = EditUserForm(request.POST, request.FILES, instance=request.user.profile)
            if edituser_form.is_valid():
                user = request.user.profile
                user.save()
                ctx.update({"form":edituser_form})  
                messages.success(request, '수정이 완료되었습니다')  
                return redirect('accounts:profile')
    else:
        ctx.update({"form": edituser_form})
    return  render(request, "accounts/myProfileedit.html", ctx)

@login_required
def changepw(request):
    ctx = {}
    if request.method == "GET":
       pass
    elif request.method == "POST":
        current_password = request.POST.get("current_password")  
        user = request.user
        if check_password(current_password, user.password): #current_password 에 입력한 값과 User에 저장된 실제 비밀번호가 일치할때
            new_password = request.POST.get("new_password")
            password_confirm = request.POST.get("password_confirm") 
            if new_password == password_confirm: #new_password 에 입력한 값과 password_confirm 에 입력한 값이 일치할때 
                user.set_password(new_password)
                user.save()
                messages.success(request, '비밀번호 변경이 완료 되었습니다.')
                
            else:
                messages.error(request, '새로운 비밀번호를 다시 확인 해주세요.')
        else:
            messages.error(request, '현재 비밀번호와 일치하지 않습니다.')
    return render(request, "accounts/changepw.html", ctx)


# @login_required
# def resetpw(request):
#     if request.method=="POST":
#         pk = request.POST.get('pk')
#         user = get_object_or_404(Profile, pk=pk)
#         new_pw = "0000"
#         user.user.set_password(new_pw)
#         user.user.save()
#         user.save()
#         return JsonResponse({'result': 'ok' })   

#     return render(request, 'accounts/management.html', {"list":Profile.objects.filter(user__is_superuser=False).order_by('-pk')})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():     
            email_g = form.cleaned_data['email_google']
            if email_g[-10:] != "@gmail.com":
                messages.error(request, '구글메일에 "@gmail.com" 을 작성해 주세요.')
                return render(request, "accounts/register.html", {'form':form})
            else:
                if len(form.cleaned_data['residentNumber']) != 14:
                    messages.error(request, '주민번호는 - 포함 14자리만 가능합니다.')
                    return render(request, "accounts/register.html", {'form':form})
                try:
                    if len(form.cleaned_data['residentNumber'].split('-')) != 2:
                        messages.error(request, '주민번호에는 꼭 (-) 포함되어야 합니다.')
                        return render(request, "accounts/register.html", {'form':form})
                except IndexError:
                    messages.error(request, '주민번호에는 꼭 (-) 포함되어야 합니다.')
                    return render(request, "accounts/register.html", {'form':form})
                
                try:
                    user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=email_g,
                                                password=form.cleaned_data['residentNumber'].split('-')[1])
                except IntegrityError:   
                    messages.error(request, '이미 등록된 이름이 있습니다.')
                    return redirect('accounts:join')

                team = Team.objects.get(name=form.cleaned_data['team'])
                user.is_active = False
                
                user.save()
                pushs = Profile.objects.filter(user__is_staff=True)
                for push in pushs:
                    if push.pushToken != '':
                        # celery task call pushbullet link or text
                        domain = Site.objects.get_current().domain
                        link = 'https://{domain}{url}'.format(domain=domain, url='/accounts/management/')
                        tasks.push_link.delay(**{"token": push.pushToken, "title": "새로운 신입사원 등록이 있습니다.", "url": link})

                Profile.objects.create(user=user, email_google=email_g,team=team, position=Position.objects.get(name='사원'),
                                    email=form.cleaned_data['email'], phone=form.cleaned_data['phone'],really_address=form.cleaned_data['really_address'],address=form.cleaned_data['address'],
                                    emergency_phone=form.cleaned_data['emergency_phone'],
                                    entry_date=form.cleaned_data['entry_date'], residentNumber=form.cleaned_data['residentNumber'])
                return redirect('accounts:thanks')
        else:
            messages.error(request, '모든 내용을 작성해주세요.')
            return render(request, "accounts/register.html", {'form':form})

    else:
        form = RegisterForm() 
        return render(request, "accounts/register.html", {'form':form})
        

@login_required
def notify(request):
    ctx = {}
    if request.method == "GET":
        form = NotifyForm(instance=request.user.profile)
        ctx.update({"form":form})
    elif request.method == "POST":
        form = NotifyForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user = request.user.profile
            user.save()
            ctx.update({"form":form}) 
    else:
        ctx.update({"form": form})       
    return render(request,'accounts/notify.html',{"form":form})

@login_required
def management(request):
    user= request.user.profile
    if user.user.is_staff == False :
        messages.error(request, '접근 권한이 없습니다')
        return redirect('main')
    if request.method=="POST":
        pk = request.POST.get('pk')
        user = get_object_or_404(Profile, pk=pk)
        new_pw = "0000"
        user.user.set_password(new_pw)
        user.user.save()
        user.save()
        return JsonResponse({'result': 'ok' }) 
     
    # 리스트 페이지네이션
    profile_list = Profile.objects.select_related('user','team','position').filter(user__is_superuser=False).order_by('-entry_date','-pk')
    
    query = request.GET.get('search')
    if query:
        profile_list = Profile.objects.filter(Q (user__username__icontains=query) | Q (team__name__icontains=query) | Q (position__name__icontains=query)| Q (entry_date__icontains=query))
    total_len = len(profile_list)
    print(total_len)
    page = request.GET.get('page', 1)
    paginator = Paginator(profile_list, 20)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = profiles.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])
     

    return render(request, 'accounts/management.html', {'list': profiles, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

# @requires_csrf_token

@login_required
def manage_detail(request, pk):
    user= request.user.profile
    if user.user.is_staff == False :
        messages.error(request, '접근 권한이 없습니다')
        return redirect('main')
    manage = get_object_or_404(Profile, pk=pk)

    if request.method == "POST":
        form = manageForm(request.POST, instance=manage)
        if form.is_valid():
            manage2 = form.save(commit=False)
            if not manage.userNum and manage.team  and manage.position  and manage.belong  :
                # 사번을 담을 변수
                number = 'G'
                # second = ''
                # third = ''
                # number = 0

            
                #직급
                position_num=(
                    ('센터장','A'),
                    ('사무국장','B'),
                    ('실장','C'),
                    ('과장','C'),
                    ('팀장','D'),
                    ('사원','G')
                )

                # 소속
                belong_num=(
                    ('글로컬','A'),
                    ('오름창의과학','B'),
                    ('서정SC','C')
                )
                    
                
                # 팀
                team_num=(
                    ('총괄','A'),
                    ('경영지원팀','B'),
                    ('교육운영기획실','C'),
                    ('교육지원실','D'),
                    ('과학팀','E'),
                    ('코딩팀','F'),
                    ('공예팀','G'),
                    ('요리팀','H'),
                    ('SI팀','I')
                )
            
                for i, j in position_num:
                    if str(manage.position) == i:
                        number += j
            

                for i, j in belong_num:
                    if str(manage.belong) == i:
                        number += j

                for i, j in team_num:
                    if str(manage.team) == i:
                        number += j
                
                max_num=0
                for post in Profile.objects.filter(user__is_superuser=False):
                    if post.userNum :
                        num = int(post.userNum[4:])
                        if max_num < num:
                            max_num = num
                    
                number += str((max_num) + 1).rjust(4, '0')

                manage2.userNum=number
                manage2.user.is_active=True
                manage2.user.save()
                
            manage2.save()

            if request.POST.get("type") == 'leave':
                manage.user.is_active = False  # 비활성화
                manage.user.is_staff = False  # 스태프권한 몰수
                manage.notifySettings = False  # 푸시알림 수신해제
                manage.user.save()
                manage.save()
            return redirect('accounts:management')
    else:
        form = manageForm(instance=manage)
    return render(request, 'accounts/manage_detail.html', {'form':form, 'pk':manage.pk, 'manage':manage})

@login_required
def annual_approval_line(request):

    lines = AnnualApprovalLine.objects.all().order_by('-pk')

    if request.method == 'POST':
        
        form = AnnualApprovalLineForm(request.POST)
        
        if form.is_valid():
            approval = form.save(commit=False)
            
            # 관리자가 아니면 걸러내기
            if request.user.is_staff == False:
                messages.error(request, '관리자가 아닙니다.')
                return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

            else:
                if approval.manager is None:
                    messages.error(request, '담당자를 선택하세요.')
                    return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

                if approval.manager.user.is_superuser == True or approval.approval.user.is_superuser == True:
                    messages.error(request, '최고 관리자계정은<br>등록하실 수 없습니다.')
                    return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

                if approval.approval.user.is_active == False:
                    messages.error(request, '계정이 비활성화 된 사원은<br>결재자로 등록하실 수 없습니다.')
                    return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

                if approval.manager == approval.approval:
                    messages.error(request, '담당자와 결재자가<br>동일한 사원이 될 수 없습니다.')
                    return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

                a = lines.filter(manager=approval.manager).count()
                if a == 0:
                    approval.save()
                    messages.success(request, '해당 사원의 연차 결재선이<br>정상적으로 추가되었습니다.')
                    return redirect('accounts:annualapproval')
                else:
                    messages.error(request, '해당 사원은 이미 등록되어 있습니다.')
                    return redirect('accounts:annualapproval')

        else:
            messages.error(request, '유효성 검증에 실패했습니다.')
            return redirect('acounts:annualapproval')
    else:
        form = AnnualApprovalLineForm()
        return render(request, 'accounts/annualapproval.html', {'form':form, 'list': lines})

@login_required
def annual_approval_line_detail(request, pk):

    if request.user.is_staff == False :
        messages.error(request, '접근 권한이 없습니다')
        return redirect('accounts:annualapproval')

    approvals = get_object_or_404(AnnualApprovalLine, pk=pk)

    if request.method == "POST":

        form = AnnualApprovalLineForm(request.POST, instance=approvals)

        if form.is_valid():
            approval = form.save(commit=False)

            if approval.manager is None:
                messages.error(request, '담당자를 선택하세요.')
                return render(request, 'accounts/annualapproval_edit.html', {'form':form})

            if approval.manager.user.is_superuser == True or approval.approval.user.is_superuser == True:
                messages.error(request, '최고 관리자계정은<br>등록하실 수 없습니다.')
                return render(request, 'accounts/annualapproval_edit.html', {'form':form})

            if approval.approval.user.is_active == False:
                messages.error(request, '계정이 비활성화 된 사원은<br>결재자로 등록하실 수 없습니다.')
                return render(request, 'accounts/annualapproval_edit.html', {'form':form})

            if approval.manager == approval.approval:
                messages.error(request, '담당자와 결재자가<br>동일한 사원이 될 수 없습니다.')
                return render(request, 'accounts/annualapproval_edit.html', {'form':form})
            
            approval.save()
            messages.success(request, '해당 사원의 연차 결재선이<br>정상적으로 수정되었습니다.')
            return redirect('accounts:annualapproval')

        else:
            messages.error(request, '유효성 검증에 실패했습니다.')
            return redirect('accounts:annualapproval')

    else:
        form = AnnualApprovalLineForm(instance=approvals)
        return render(request, 'accounts/annualapproval_edit.html', {'form':form, 'approvals':approvals})