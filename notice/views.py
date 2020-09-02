from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from .models import Notice, Comment, Profile, Team, NoticeTarget, Tag, CaseManagement, CaseTag
from .forms import NoticeForm, CommentForm, NoticeTargetForm, CaseManagementForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from accounts import push
from accounts import tasks
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# Create your views here.

# 공지사항
@login_required
def list2(request, tag=None):
    user = request.user.profile
    tag_all = Tag.objects.annotate(num_post=Count('notice')).order_by('-pk')

    if tag:
        if user.user.is_staff==True:
            notice_list = Notice.objects.filter(tag_set__name__iexact=tag).prefetch_related('target_set__user','comment_set').select_related('user__user','team').all().order_by('-pk')
        else:
            notice_list = Notice.objects.filter(tag_set__name__iexact=tag).filter(Q(targets__icontains=user)|Q(user=user)|Q(targets="전체선택")).order_by('-pk')

    else:
        if user.user.is_staff==True:
            notice_list = Notice.objects.prefetch_related('target_set__user','comment_set').select_related('user__user','team').all().order_by('-pk')
        else:
            notice_list = Notice.objects.filter(Q(targets__icontains=user)|Q(user=user)|Q(targets="전체선택")).order_by('-pk')

    # 리스트 페이지네이션
    query = request.GET.get('search')
    if query:
        notice_list = Notice.objects.filter(Q (user__user__username__icontains=query) | Q (important__icontains=query) | Q (date__icontains=query)| Q (title__icontains=query))
    total_len = len(notice_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(notice_list, 10)
    try:
        notices = paginator.page(page)
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = notices.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request,'notice/list.html',{'list' : notices, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

# 공지사항 작성
@login_required
def new(request):
    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user.profile
            notice.save()
            notice.tag_save()
            post = get_object_or_404(Notice, pk=notice.pk)
            form = NoticeTargetForm(request.POST)
            if post.targets == "전체선택":
                for i in Profile.objects.filter(user__is_superuser=False):
                    tg = form.save(commit=False)
                    tg.pk = None

                    tg.user = Profile.objects.get(user__username=i)
                    tg.num = post
                    tg.save()

                    if tg.user.pushToken != '' and tg.user.notifySettings == True :
                        # celery task call pushbullet link or text
                        domain = Site.objects.get_current().domain
                        title = "[드림웨어] "+str(notice.title)
                        link = 'https://{domain}{url}'.format(domain=domain, url=notice.get_absolute_url())
                        tasks.push_link.delay(**{"token": tg.user.pushToken, "title": title, "url": link})

            else:
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
                        title = "[드림웨어] "+str(notice.title)
                        link = 'https://{domain}{url}'.format(domain=domain, url=notice.get_absolute_url())
                        tasks.push_link.delay(**{"token": tg.user.pushToken, "title": title, "url": link})

            messages.success(request, '등록이 완료되었습니다')
            return redirect('notice:list')
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('notice:list')
    else:
        form = NoticeForm()
    return render(request, 'notice/new.html', {'form': form,'target' : Profile.objects.all().order_by('pk'), 'teams':Team.objects.all().order_by('pk')})
    
# 공지사항 디테일
@login_required
def detail(request, pk):
    post = get_object_or_404(Notice, pk=pk)
    user = request.user.profile

    if NoticeTarget.objects.filter(num=post, user=user).exists() :
        noticeTarget = NoticeTarget.objects.get(num=post, user=user)
        
        form = NoticeTargetForm(request.POST, instance=noticeTarget)
        if form.is_valid():
            noticeTarget = form.save(commit=False)
            noticeTarget.read = True
            noticeTarget.save()
    
    aa = NoticeTarget.objects.filter(num=post, read=True, user__user__is_superuser=False, user__user__is_active=True)
    readSttst= aa.count()

    ab = NoticeTarget.objects.filter(num=post, user__user__is_active=True)
    readPercent = int((readSttst/ab.count())*100)

    ac = NoticeTarget.objects.filter(num=post, read=False, user__user__is_active=True,user__user__is_superuser=False)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user.profile
            comment.num = post
            comment.save()
            if post.user.pushToken != '' and post.user.notifySettings == True:
                # celery task call pushbullet link or text
                domain = Site.objects.get_current().domain
                link = 'https://{domain}{url}'.format(domain=domain, url=post.get_absolute_url())
                tasks.push_link.delay(**{"token": post.user.pushToken, "title": "공지에 새로운 댓글이 등록 되었습니다.", "url": link})
            
            return redirect('notice:detail', pk)
    else:
        form = CommentForm()

    return render(request, 'notice/detail.html', {'detail' : Comment.objects.filter(num=post).order_by('pk'), 'post' : post, 'form':form, 'readSttst':readSttst, 'readPercent':readPercent, 'aa':aa, 'ac':ac})

# 공지 삭제
@login_required
def remove(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    user = request.user.profile
    if user == notice.user :
        notice.delete()
        messages.success(request, '공지가 삭제되었습니다.')
        return redirect('notice:list')
    else:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('notice:detail', pk)

# 공지 코멘트 삭제
@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user.profile
    if user == comment.user :
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('notice:detail', comment.num.pk)
    else:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('notice:detail', comment.num.pk)


# 사례관리 목록
@login_required
def case_list(request, tag=None):
    user = request.user.profile
    tag_all = CaseTag.objects.annotate(num_post=Count('casemanagement')).order_by('-pk')

    if tag:
        case_list = CaseManagement.objects.filter(tag_set__name__iexact=tag).select_related('user__user').all().order_by('-pk')

    else:
        case_list = CaseManagement.objects.select_related('user__user').all().order_by('-pk')

    # 리스트 페이지네이션
    query = request.GET.get('search')
    if query:
        case_list = CaseManagement.objects.filter(Q (user__user__username__icontains=query) | Q (date__icontains=query)| Q (title__icontains=query))
    total_len = len(case_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(case_list, 10)
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
    
    # 페이징 5개 이상이면 생략
    index = cases.number -1 # URL에서 ?page= 다음에 들어오는 숫자
    max_index = len(paginator.page_range) # 마지막 페이지
    start_index = index -2 if index >= 2 else 0 # 현재 페이지번호 기준으로 2페이지 전의 페이지번호
    if index < 2 : 
        end_index = 5-start_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    else: 
        end_index = index +3 if index <= max_index - 3 else max_index # 현재 페이지번호 기준으로 2페이지 뒤의 페이지번호
    page_range = list(paginator.page_range[start_index:end_index])

    return render(request,'notice/list_case.html',{'list' : cases, 'page_range':page_range, 'total_len':total_len, 'max_index':max_index-2})

# 사례 작성
@login_required
def case_new(request):
    # 관리자가 아니면 걸러내기
    if request.user.is_staff == False:
        messages.error(request, '관리자가 아닙니다.')
        return redirect('notice:case_list')

    if request.method == "POST":
        form = CaseManagementForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user.profile
            case.save()
            case.tag_save()

            messages.success(request, '등록이 완료되었습니다')
            return redirect('notice:case_list')
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('notice:case_list')
    else:
        form = CaseManagementForm()
    return render(request, 'notice/new_case.html', {'form': form})

# 사례 디테일
@login_required
def case_detail(request, pk):
    post = get_object_or_404(CaseManagement, pk=pk)
    return render(request, 'notice/detail_case.html', {'post' : post})

# 사례 수정
@login_required
def case_edit(request, pk):
    post = get_object_or_404(CaseManagement, pk=pk)
    user = request.user.profile
    if user != post.user :
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('notice:case_detail', pk)

    if request.method == "POST":
        form = CaseManagementForm(request.POST, instance=post)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user.profile
            case.save()
            case.tag_set.clear()
            case.tag_save()
            messages.success(request, '수정이 완료되었습니다')
            return redirect('notice:case_detail', pk)
        else :
            messages.error(request, '데이터가 유효하지 않습니다.')
            return redirect('notice:case_detail', pk)
    else:
        form = CaseManagementForm(instance=post)
    return render(request, 'notice/edit_case.html', {'form': form, 'post':post})

# 사례 삭제
@login_required
def case_remove(request, pk):
    post = get_object_or_404(CaseManagement, pk=pk)
    user = request.user.profile
    if user == post.user :
        post.delete()
        messages.success(request, '사례가 삭제되었습니다.')
        return redirect('notice:case_list')
    else:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('notice:case_detail', pk)