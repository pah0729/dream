from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from annual.models import Annual, AnnualDate, MinusData
from accounts.models import Profile, AnnualApprovalLine
from annual.forms import AnnualForm, ConfirmForm, ManageForm, AnnualDateForm
from django.contrib import messages
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import date, datetime , timedelta
from dateutil.relativedelta import relativedelta
from django.urls import reverse_lazy
from annual.decorators import annual_process_check,is_validation_action
from django.views.generic import TemplateView
from annual import tasks
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers


# TemplateView 와 login_required 믹스인
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

# 연차 신청 목록
@login_required
def annual_list(request):
    
    # 리스트 페이지네이터
    annual_list = Annual.objects.select_related('user__user','team').all().order_by('-pk')

    query = request.GET.get('search')
    if query:
            annual_list = Annual.objects.select_related('user__user','team').filter(Q (user__user__username__icontains=query) | Q (team__name__icontains=query) | Q(division__icontains=query) | Q(sdate__icontains=query)| Q(fdate__icontains=query)| Q(status__icontains=query)).distinct()
    total_len = len(annual_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(annual_list, 20)
    try:
        annuals = paginator.page(page)
    except PageNotAnInteger:
        annuals = paginator.page(1)
    except EmptyPage:
        annuals = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = annuals.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request,'annual/apply_list.html',{'list': annuals, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

# 휴가원 관리
@login_required
def approval_list(request):
    if request.user.is_staff == False:
        messages.error(request, '관리자가 아니면 접근할 수 없습니다.')
        return redirect('annual:calendar')

    # 리스트 페이지네이터
    approval_list = Annual.objects.select_related('user__user','team').filter(finalApproval=True).order_by('-sdate','-pk')
    query = request.GET.get('search')
    if query:
            approval_list = Annual.objects.select_related('user__user','team').exclude(finalApproval=False).filter(Q (user__user__username__icontains=query) |Q (team__name__icontains=query) | Q(division__icontains=query) | Q(sdate__icontains=query)| Q(fdate__icontains=query)| Q(status__icontains=query)).distinct().order_by('-sdate','-pk')
    total_len = len(approval_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(approval_list, 20)
    try:
        approvals = paginator.page(page)
    except PageNotAnInteger:
        approvals = paginator.page(1)
    except EmptyPage:
        approvals = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = approvals.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request,'annual/apply_approval.html',{'list' : approvals, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

# 승인된 연차 상세보기
@login_required
def approval_detail(request, pk):
    detail = get_object_or_404(Annual, pk=pk)
    confirm = request.POST.get('action')
    today = date.today()
    if request.user.is_staff == False:
        messages.error(request, '관리자가 아닙니다.')
        return redirect('annual:approval')

    if detail.finalApproval == False:
        messages.error(request, '결재 진행중이거나 반려된 휴가원은<br>열람 및 취소할 수 없습니다.')
        return redirect('annual:approval')

    if request.method == 'POST':
        detail.status = confirm
        detail.finalApproval = False
        detail.return_reason = '관리자 승인취소 : '+ request.user.username
        pushu = detail.user
        if detail.status == '반려' and pushu.pushToken != '' and pushu.notifySettings == True:
            domain = Site.objects.get_current().domain
            link = 'https://{domain}{url}'.format(domain=domain, url=detail.get_absolute_url())
            tasks.push_link.delay(**{"token": pushu.pushToken, "title": "[드림웨어] 연차가 승인 취소되었습니다. (관리자)", "url": link})
        detail.save()
        messages.success(request, '승인 취소가 완료되었습니다.')
        return redirect('annual:approval')
            
    return render(request, 'annual/detail.html', {'detail':detail, 'today':today})

# 전직원 연차 현황
@login_required
def total(request):
    annualdata = []
    Profile_list = []
    ocrncdate = []
    ocrncdate_ex = []
    extncdate_oc = []
    extncdate = []
    total = []
    use = []
    extnc = []
    due = []
    remain = []
    alluser = Profile.objects.select_related('user').all()
    allannual = Annual.objects.select_related('user').all()
    userfilter = alluser.filter(user__is_superuser=False).exclude(user__is_active=False).order_by('entry_date')
    query = request.GET.get('type')
    if query == '퇴사':
        userfilter = alluser.filter(user__is_superuser=False).exclude(user__is_active=True).order_by('entry_date')
    if query == '재직':
        userfilter = alluser.filter(user__is_superuser=False).exclude(user__is_active=False).order_by('entry_date')
    for user in userfilter:
        # 연차가 발생하지 않은 사원
        if not AnnualDate.objects.filter(user=user).count():
            # 발생한 총 연차 개수
            create = 0.0
            total.append(create)
            # 사용예정일수
            if allannual.filter(user=user, division='연차', finalApproval=True, sdate__gt=date.today()).count():
                duesum = 0.0
                dues = 0.0
                for dueDate in allannual.filter(user=user, division='연차', finalApproval=True, sdate__gt=date.today()):
                    dues += duesum + float(dueDate.datediff)
                due.append(dues)
            else:
                dues = 0.0
                due.append(dues)
            # 연차 개수 연산
            alldata = AnnualDate.objects.filter(user=user, is_active=True).count()
            minusdata = MinusData.objects.filter(user=user, payback=False).count()
            extncdata = AnnualDate.objects.filter(user=user, is_delete=True).count()
            sumdata = (alldata + minusdata) / 2
            use.append(sumdata)
            result = create - sumdata - (extncdata / 2) - dues
            remain.append(result)
            # 소멸한 연차 개수
            delete = 0.0
            extnc.append(delete)
            # 마지막 연차 발생일
            ocrncdate.append('없음')
            ocrncdate_ex.append('없음')
            # 가까운 연차 소멸일
            extncdate_oc.append('없음')
            extncdate.append('없음')
            Profile_list.append(user)
        
        # 연차가 발생한 사원
        else:
            # 발생한 총 연차 개수
            allcount = AnnualDate.objects.filter(user=user).count()
            create = allcount / 2
            total.append(create)
            # 사용예정일수
            if allannual.filter(user=user, division='연차', finalApproval=True, sdate__gt=date.today()).count():
                duesum = 0.0
                dues = 0.0
                for dueDate in allannual.filter(user=user, division='연차', finalApproval=True, sdate__gt=date.today()):
                    dues += duesum + float(dueDate.datediff)
                due.append(dues)
            else:
                dues = 0.0
                due.append(dues)
            # 연차 개수 연산
            alldata = AnnualDate.objects.filter(user=user, is_active=True).count()
            minusdata = MinusData.objects.filter(user=user, payback=False).count()
            extncdata = AnnualDate.objects.filter(user=user, is_delete=True).count()
            sumdata = (alldata + minusdata) / 2
            use.append(sumdata)
            result = create - sumdata - (extncdata / 2) - dues
            remain.append(result)
            # 최근 연차 발생일
            ocrdates = AnnualDate.objects.filter(user=user).latest('ocrncDate')
            ocrdate = ocrdates.ocrncDate
            exdate = ocrdates.extncDate
            ocrncdate.append(ocrdate)
            ocrncdate_ex.append(exdate)
            # 가까운 연차 소멸일
            if AnnualDate.objects.filter(user=user, is_delete=False).exclude(is_active=True).count():
                extdates = AnnualDate.objects.filter(user=user, is_delete=False).exclude(is_active=True).first()
                tenures = int(((extdates.ocrncDate - user.entry_date).days + 1) / 365)  # 입사 1년미만때 발생연차판별
                if tenures < 1:  # 1년미만에 발생되었다면 소멸일은 입사일+1년
                    extdate = user.entry_date + relativedelta(years=1)
                else:  # 아니면 소멸일은 발생일로부터 1년
                    extdate = extdates.ocrncDate + relativedelta(years=1)
                extncdate_oc.append(extdates.ocrncDate)
                extncdate.append(extdate)
            else:
                extncdate_oc.append('없음')
                extncdate.append('없음')
            # 소멸한 연차 개수
            deletes = AnnualDate.objects.filter(user=user, is_delete=True).count()
            delete = deletes / 2
            extnc.append(delete)

            Profile_list.append(user)

        lists = zip(Profile_list, ocrncdate, ocrncdate_ex, extncdate_oc, extncdate, total, use, extnc, due, remain)
        annualdata = ([user for user in lists])

    return render(request,'annual/total_list.html',{'annualdata':annualdata})

# 전직원 연차 목록
@login_required
def datemanage(request, pk):
    post = get_object_or_404(Profile, pk=pk)

    # 리스트 페이지네이터
    datemanage_list = AnnualDate.objects.filter(user=post).order_by('-pk')
    query = request.GET.get('search')
    if query:
            datemanage_list = AnnualDate.objects.filter(Q (user=post) & ( Q (ocrncDate__icontains=query) | Q(memo__icontains=query) ))
    total_len = len(datemanage_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(datemanage_list, 50)
    try:
        dates = paginator.page(page)
    except PageNotAnInteger:
        dates = paginator.page(1)
    except EmptyPage:
        dates = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = dates.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index])
    
    num = request.POST.get('number')
    memo = request.POST.get('memo')
    ocrncDate = request.POST.get('ocrncDate')
    if request.method == 'POST':

        # 관리자만 생성가능
        if request.user.is_staff == True:
            number = float(num) * 2
            for annualdates in range(int(number)):
                AnnualDate.objects.create(user=post, ocrncDate=ocrncDate, memo=memo)
            messages.success(request, '연차 생성이 완료되었습니다.')
            return redirect('annual:datemanage', pk)

        # 관리자가 아니면 걸러내기
        elif request.user.is_staff == False:
            messages.error(request, '관리자가 아닙니다.')
            return redirect('annual:datemanage', pk)
    
    else:
        return render(request,'annual/plus_manage.html',{'datemanage': dates, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2, 'pk':pk, 'post':post})

# 연차 삭제
@login_required
def removedate(request):
    pk = request.POST.get("pk")
    if request.method=="POST":
        annualdate = get_object_or_404(AnnualDate, pk=pk)
        if request.user.is_staff == True:
            annualdate.delete()
            messages.success(request, '연차 삭제를 완료했습니다.')
            return JsonResponse({'result': 'ok' })
        else:
            messages.error(request, '관리자가 아닙니다.')
            return JsonResponse({'result': 'fail' })

# 연차데이터 수정
@login_required
def modify(request):
    pk = request.POST.get("pk")
    ocr = request.POST.get("ocr")
    memo = request.POST.get("memo")
    use = request.POST.get("use")
    active = request.POST.get("active")

    if request.method=="POST":
        annual = get_object_or_404(AnnualDate, pk=pk)
        if request.user.is_staff == True:
            annual.ocrncDate = ocr
            annual.memo = memo
            annual.finalUpdtd = use
            if use == "":
                annual.finalUpdtd = None
            if active == "false":
                annual.is_active = False
            elif active == "true":
                annual.is_active = True
            annual.save()
            messages.success(request, '연차데이터 수정을 완료했습니다.')
            return JsonResponse({'result': 'ok' })
        else:
            messages.error(request, '관리자가 아닙니다.')
            return JsonResponse({'result': 'fail' })
    return JsonResponse({'result': 'ok' })

# 전직원 마이너스 연차 목록
@login_required
def minusmanage(request, pk):
    post = get_object_or_404(Profile, pk=pk)

    # 리스트 페이지네이터
    minusmanage_list = MinusData.objects.filter(user=post).order_by('-pk')
    query = request.GET.get('search')
    if query:
            minusmanage_list = MinusData.objects.filter(Q (user=post) & ( Q (ocrncDate__icontains=query) ))
    total_len = len(minusmanage_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(minusmanage_list, 50)
    try:
        dates = paginator.page(page)
    except PageNotAnInteger:
        dates = paginator.page(1)
    except EmptyPage:
        dates = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = dates.number -1 
    max_index = len(paginator.page_range) 
    start_index = index -2 if index >= 2 else 0 
    if index < 2 : 
        end_index = 5-start_index 
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index 
    page_range = list(paginator.page_range[start_index:end_index])

    num = request.POST.get('number')
    ocrncDate = request.POST.get('ocrncDate')
    if request.method == 'POST':

        # 관리자만 생성가능
        if request.user.is_staff == True:
            number = float(num) * 2
            for minusdatas in range(int(number)):
                MinusData.objects.create(user=post, ocrncDate=ocrncDate)
            messages.success(request, '마이너스 연차 생성이 완료되었습니다.')
            return redirect('annual:minusmanage', pk)

        # 관리자가 아니면 걸러내기
        elif request.user.is_staff == False:
            messages.error(request, '관리자가 아닙니다.')
            return redirect('annual:minusmanage', pk)

    return render(request,'annual/minus_manage.html',{'minusmanage' : dates, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2, 'pk':pk, 'post':post})

# 마이너스 연차데이터 수정
@login_required
def modify_minus(request):
    pk = request.POST.get("pk")
    ocr = request.POST.get("ocr")
    payback = request.POST.get("payback")

    if request.method=="POST":
        minus = get_object_or_404(MinusData, pk=pk)
        if request.user.is_staff == True:
            minus.ocrncDate = ocr
            if payback == "false":
                minus.payback = False
            elif payback == "true":
                minus.payback = True
            minus.save()
            messages.success(request, '마이너스 연차데이터 수정을 완료했습니다.')
            return JsonResponse({'result': 'ok' })
        else:
            messages.error(request, '관리자가 아닙니다.')
            return JsonResponse({'result': 'fail' })
    return JsonResponse({'result': 'ok' })

# 연차 신청
@login_required
def new(request):

    # 남은 연차개수 카운트
    cal = 0 
    for i in AnnualDate.objects.filter(user=request.user.profile) : 
        cal += i.annualcal
    for j in MinusData.objects.filter(user=request.user.profile) :
        cal -= j.minuscal
    annualtotal = cal

    # 승인된 연차개수 카운트
    approvalcal = 0
    if Annual.objects.filter(user=request.user.profile, division='연차', finalApproval=True, sdate__gt=date.today()).count():
        for k in Annual.objects.filter(user=request.user.profile, division='연차', finalApproval=True, sdate__gt=date.today()):
            approvalcal += float(k.datediff)
    annualapproval = approvalcal


    # 승인 예정인 연차개수 카운트
    willcal = 0
    if Annual.objects.filter(user=request.user.profile, division='연차', status='대기', sdate__gt=date.today()).count():
        for k in Annual.objects.filter(user=request.user.profile, division='연차', status='대기', sdate__gt=date.today()):
            willcal += float(k.datediff)
    annualwill = willcal

    # 사용가능 연차개수 카운트
    annualavailable = cal - willcal - approvalcal
    task = AnnualApprovalLine.objects.all()
    approvals = []
    approval_user = request.user.profile
    approvals.append(approval_user)
    temp_user = None

    # 신청자의 연차 결재선이 없으면 걸러내기
    if task.filter(manager=request.user.profile).count() == 0:
        messages.error(request, '연차 결재선이 지정되지 않아<br>신청할 수 없습니다.')
        return redirect('annual:list')

    if request.method == 'POST':
        
        form = AnnualForm(request.POST, request.FILES)
        
        if form.is_valid():
            annual = form.save(commit=False)
            annual.user = request.user.profile
            annual.team = request.user.profile.team
            annual.position = request.user.profile.position
            
            # 신청한 일수체크
            if annual.datediff <= 0:
                messages.error(request, '휴가 일수는 0 또는 음수가 입력될 수 없습니다.')
                return render(request, 'annual/apply.html', {'form':form})

            else:
                # 같은 날짜에 신청된 내용이 있는지 체크
                a = Annual.objects.filter(user=request.user.profile, sdate=annual.sdate, finalApproval=True).count()
                if a == 0:
                    annual.step = task.get(manager=request.user.profile)

                    while(True):
                        try:
                            if temp_user is None:
                                temp_user = approval_user
                            temp = AnnualApprovalLine.objects.get(manager=temp_user)
                            temp_user = temp.approval
                        except:
                            break
                        
                        if temp.approval is None:
                            break
                        else:
                            approvals.append(temp.approval)

                    #print('신청자의 결재선: ',len(approvals))

                    if annual.step.approval == None:
                        annual.status = '승인'
                        annual.finalApproval = True
                        annual.director_center = request.user.username
                    else:
                        annual.status = '대기'
                        if len(approvals) == 4:
                            if task.filter(approval=request.user.profile):
                                #print('실장있는팀의 팀장')
                                annual.teamleader = request.user.username
                        elif len(approvals) == 3:
                            if task.filter(approval=request.user.profile).count() == 1:
                                #print('실장있는팀의 실장')
                                annual.chief = request.user.username
                            elif task.filter(approval=request.user.profile).count() > 1:
                                #print('일반팀의 팀장')
                                annual.teamleader = request.user.username
                        elif len(approvals) == 2:
                            #print('국장')
                            annual.director_office = request.user.username

                    annual.save()
                    push = annual.step.approval
                    if push != None and push.pushToken != '' and push.notifySettings == True:
                        domain = Site.objects.get_current().domain
                        title = "[드림웨어] "+str(annual.user.user.username)+"님의 연차 결재요청"
                        link = 'https://{domain}{url}'.format(domain=domain, url=annual.get_absolute_url())
                        tasks.push_link.delay(**{"token": push.pushToken, "title": title, "url": link})
                    messages.success(request, '신청이 완료되었습니다.')
                    return redirect('annual:list')
                else:
                    messages.error(request, '이미 신청한 날짜입니다.')
                    return render(request, 'annual/apply.html', {'form':form})
        else:
            messages.error(request, '유효성 검증에 실패했습니다.')
            return redirect('annual:list')
    else:
        form = AnnualForm()
        return render(request, 'annual/apply.html', {'form':form, 'annualtotal':annualtotal, 'annualwill':annualwill, 'annualavailable':annualavailable, 'annualapproval':annualapproval})

# 연차 신청 (관리자용)
@login_required
def manage(request):
    task = AnnualApprovalLine.objects.all()
    if request.method == 'POST':
        
        form = ManageForm(request.POST)
        
        if form.is_valid():
            annual = form.save(commit=False)
            
            # 관리자가 아니면 걸러내기
            if request.user.is_staff == False:
                messages.error(request, '관리자가 아닙니다.')
                return redirect('annual:manage')
            
            # 다이렉트로 최종결재 승인
            else:
                if annual.datediff <= 0:
                    messages.error(request, '휴가 일수는 0 또는 음수가 입력될 수 없습니다.')
                    return render(request, 'annual/apply_manage.html', {'form':form})

                else:
                    if annual.user is None:
                        messages.error(request, '사원을 선택하세요.')
                        return render(request, 'annual/apply_manage.html', {'form':form})

                    a = Annual.objects.select_related('user').filter(user=annual.user, sdate=annual.sdate, finalApproval=True).count()
                    if a == 0:
                        annual.team = annual.user.team
                        annual.position = annual.user.position
                        annual.remark = '신청 대리인 : ' + request.user.username
                        annual.local = '-'
                        if annual.user.phone:
                            annual.relationship = '본인'
                            annual.network = annual.user.phone
                        else:
                            annual.relationship = '-'
                            annual.network = '-'

                        annual.step = task.get(approval=None)
                        annual.status = '승인'
                        annual.finalApproval = True

                        office_get = task.get(approval=annual.step.manager)
                        annual.director_office = office_get.manager.user.username
                        annual.director_center = annual.step.manager.user.username

                        annual.save()
                        pushu = annual.user
                        if annual.status == '승인' and pushu.pushToken != '' and pushu.notifySettings == True:
                            domain = Site.objects.get_current().domain
                            title = "[드림웨어] 관리자가 연차 신청을 완료했습니다."
                            link = 'https://{domain}{url}'.format(domain=domain, url=annual.get_absolute_url())
                            tasks.push_link.delay(**{"token": pushu.pushToken, "title": title, "url": link})
                        messages.success(request, '연차 신청이 완료되었습니다.<br>모든 결재가 자동으로 처리되었습니다.')
                        return redirect('annual:list')
                    else:
                        messages.error(request, '해당 사원은 선택하신 기간에 이미 승인된 연차가 있습니다.')
                        return render(request, 'annual/apply_manage.html', {'form':form})
            
        else:
            messages.error(request, '유효성 검증에 실패했습니다.')
            return redirect('annual:list')
    else:
        form = ManageForm()
        return render(request, 'annual/apply_manage.html', {'form':form})

# 연차결재 프로세스
@login_required
@annual_process_check(fail_url=reverse_lazy('annual:list'))
def confirm(request, pk):

    confirm = get_object_or_404(Annual, pk=pk)
    actions = is_validation_action(request.user.profile)
    today = date.today()
    task = AnnualApprovalLine.objects.all()
    apply_approvals = []
    approvals = []
    approval_user = request.user.profile
    apply_approvals.append(confirm.user)
    approvals.append(approval_user)
    temp_user = None
    temp_apply_user = None

    if request.method == 'POST':
        try:
            action = request.POST['action']
        except:
            messages.error(request, 'value값을 임의로 조작하지 마세요!!!')
            return redirect('annual:list')

        if action in actions and (confirm.step.approval == request.user.profile or confirm.step.approval == None):
            
            confirm.status = action

            while(True):
                try:
                    if temp_user is None:
                        temp_user = approval_user
                    temp = AnnualApprovalLine.objects.get(manager=temp_user)
                    temp_user = temp.approval
                except:
                    break
                
                if temp.approval is None:
                    break
                else:
                    approvals.append(temp.approval)

            while(True):
                try:
                    if temp_apply_user is None:
                        temp_apply_user = confirm.user
                    temp2 = AnnualApprovalLine.objects.get(manager=temp_apply_user)
                    temp_apply_user = temp2.approval
                except:
                    break
                
                if temp2.approval is None:
                    break
                else:
                    apply_approvals.append(temp2.approval)
                    
            #print('신청자의 결재라인: ',len(apply_approvals))
            #print('결재자의 결재라인: ',len(approvals))
            
            if confirm.status == '대기':
                confirm.step = task.get(manager=request.user.profile)
                # 실장 결재라인이 있는팀의 사원이 신청한것
                if len(apply_approvals) == 5 :
                    if len(approvals) == 4:
                        confirm.teamleader = request.user.username
                        confirm.teamleader_comment = request.POST.get("comment")
                        confirm.return_reason = ''
                    elif len(approvals) == 3:
                        confirm.chief = request.user.username
                        confirm.chief_comment = request.POST.get("comment")
                        confirm.return_reason = ''
                    elif len(approvals) == 2:
                        confirm.director_office = request.user.username
                        confirm.director_office_comment = request.POST.get("comment")
                        confirm.return_reason = ''

                # 팀장 결재라인만 있는팀의 사원이 신청한것
                if not task.filter(approval=confirm.user).count():
                    if len(apply_approvals) == 4:
                        if len(approvals) == 3:
                            confirm.teamleader = request.user.username
                            confirm.teamleader_comment = request.POST.get("comment")
                            confirm.return_reason = ''
                        elif len(approvals) == 2:
                            confirm.director_office = request.user.username
                            confirm.director_office_comment = request.POST.get("comment")
                            confirm.return_reason = ''
                    elif len(apply_approvals) == 3:
                        if len(approvals) == 2:
                            confirm.director_office = request.user.username
                            confirm.director_office_comment = request.POST.get("comment")
                            confirm.return_reason = ''
                    
                # 팀장이 신청한것
                if task.filter(approval=confirm.user).count() >= 1:
                    if len(apply_approvals) == 4:
                        #print('실장 존재')
                        if len(approvals) == 3:
                            confirm.chief = request.user.username
                            confirm.chief_comment = request.POST.get("comment")
                            confirm.return_reason = ''
                        elif len(approvals) == 2:
                            confirm.director_office = request.user.username
                            confirm.director_office_comment = request.POST.get("comment")
                            confirm.return_reason = ''
                    elif len(apply_approvals) == 3:
                        #print('팀장만 존재 or 실장 본인신청')
                        if len(approvals) == 2:
                            confirm.director_office = request.user.username
                            confirm.director_office_comment = request.POST.get("comment")
                            confirm.return_reason = ''


            elif confirm.status == '승인':
                confirm.step = task.get(manager=request.user.profile)
                confirm.finalApproval = True
                confirm.director_center = request.user.username
                confirm.director_center_comment = request.POST.get("comment")
                confirm.return_reason = ''
            elif confirm.status == '반려':
                confirm.return_reason = request.POST.get("comment")
                confirm.finalApproval = False

            confirm.save()
            push = confirm.step.approval
            pushu = confirm.user

            if confirm.status == '대기' and push.pushToken != '' and push.notifySettings == True:
                domain = Site.objects.get_current().domain
                title = "[드림웨어] "+str(confirm.user.user.username)+"님의 연차 결재요청"
                link = 'https://{domain}{url}'.format(domain=domain, url=confirm.get_absolute_url())
                tasks.push_link.delay(**{"token": push.pushToken, "title": title, "url": link})

            elif confirm.status == '승인' and pushu.pushToken != '' and pushu.notifySettings == True:
                domain = Site.objects.get_current().domain
                link = 'https://{domain}{url}'.format(domain=domain, url=confirm.get_absolute_url())
                tasks.push_link.delay(**{"token": pushu.pushToken, "title": "[드림웨어] 신청하신 연차가 승인되었습니다.", "url": link})

            elif confirm.status == '반려' and pushu.pushToken != '' and pushu.notifySettings == True:
                domain = Site.objects.get_current().domain
                link = 'https://{domain}{url}'.format(domain=domain, url=confirm.get_absolute_url())
                tasks.push_link.delay(**{"token": pushu.pushToken, "title": "[드림웨어] 신청하신 연차가 거절되었습니다.", "url": link})

            messages.success(request, '결재를 완료했습니다.')
            return redirect('annual:list')

        else:
            messages.error(request, '결재 절차에 오류가 있습니다.')
            return redirect('annual:list')

    return render(request, 'annual/confirm.html', {'actions':actions,'confirm':confirm, 'today':today})

# 연차 캘린더
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['eventlist'] = Annual.objects.select_related('user__user').filter(finalApproval=True)
        return context