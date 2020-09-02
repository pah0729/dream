from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from accounts.models import Profile
from commute.models import Commute
from annual.models import Annual
from .models import AcesStts
from notice.models import NoticeTarget
from .forms import  LoginForm, AcesSttsForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import *
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from ipaddress import ip_address, ip_network
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from django.utils.encoding import force_bytes
from django.conf import settings
import hmac
from hashlib import sha1
from home import tasks
from django.template import RequestContext


def signin(request):
     if request.method == "POST":
          try:
               username = request.POST['username']+"@gmail.com"
               password = request.POST['password']
          except MultiValueDictKeyError:
               messages.warning(request, '어디서 약을 팔어 -3- ??')
               return HttpResponseRedirect("/")
          try:
               profile_email = Profile.objects.get(email_google=username)
          except ObjectDoesNotExist:
               messages.warning(request, '아이디를 확인해주세요.')
               return HttpResponseRedirect("/")
          
          try:
               active = Profile.objects.get(email_google=username, user__is_active=True)
          except ObjectDoesNotExist:
               messages.info(request, '관리자 승인 대기중입니다.')
               return HttpResponseRedirect("/")
          
          if profile_email:      
               user = authenticate(username = profile_email, password = password)
               if user is not None:
                    login(request, user)
                    form = AcesSttsForm(request.POST)
                    log = form.save(commit=False)
                    log.user = request.user.profile
                    log.save()
                    next_url = request.GET.get('next')
                    if next_url:
                         return HttpResponseRedirect(next_url)
                    else:
                         return redirect('main')
               else:
                    messages.warning(request, '비밀번호를 확인해주세요.')
                    return HttpResponseRedirect("/")     
     else:
          form = LoginForm()                
          return render(request, 'login.html', {'form': form})
       
@login_required
def signout(request):
    logout(request)
    return redirect('login')

@login_required
def main(request):
     return render(request, 'main.html')

     

@require_POST
@csrf_exempt
def git(request):

     forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
     client_ip_address = ip_address(forwarded_for)
     whitelist = requests.get('https://api.github.com/meta').json()['hooks']

     for valid_ip in whitelist:
          if client_ip_address in ip_network(valid_ip):
               break
     else:
          return HttpResponseForbidden('Permission denied(whitelist).')


     # Verify the request signature
     header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
     if header_signature is None:
          return HttpResponseForbidden('Permission denied(header_signature).')

     sha_name, signature = header_signature.split('=')
     if sha_name != 'sha1':
          return HttpResponseServerError('Operation not supported.', status=501)

     mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
     if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
          return HttpResponseForbidden('Permission denied(secret code invalid).')
     

     # Process the GitHub events
     event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

     if event == 'ping':
          return HttpResponse('pong')
     elif event == 'push':
          # 요기다 deploy 하는 부분을 연결하면 될듯
          tasks.reload.delay()
          # push_slack(msg='git push webhook test')

          return HttpResponse('success')

     return HttpResponse(status=204)

 
# 404에러(Error)
def handler404(request, exception):
    return render(request,'404.html')

def handler500(request, template_name='500.html'):
    return render(request,'500.html')

# 사원 전체 현황
@login_required
def status(request):
     query = request.GET.get('team')
     user_list = []
     user_status = []
     alluser = Profile.objects.select_related('user').filter(user__is_superuser = False, user__is_active=True).order_by('-team','entry_date')
     if query:
          alluser = Profile.objects.select_related('user').filter(user__is_superuser = False, user__is_active=True, team__name=query).order_by('team','-position','entry_date')
     commute_today = Commute.objects.filter(date_commute__year=date.today().year, date_commute__month=date.today().month, date_commute__day=date.today().day)
     annual_today = Annual.objects.filter(finalApproval=True, sdate__lte=date.today(), fdate__gte=date.today())
     for user in alluser:
          commute = commute_today.filter(user=user)
          if commute.count() != 0:
               status = commute.last()
               user_status.append(status)
               user_list.append(user)
          else:
               annual = annual_today.filter(user=user)
               if annual.count() != 0:
                    annual = annual_today.get(user=user)
                    # print(annual.datediff)
                    if annual.datediff >= 1:
                         user_status.append(annual)
                         user_list.append(user)
                    else:
                         user_status.append('미등록')
                         user_list.append(user)
               else:
                    user_status.append('미등록')
                    user_list.append(user)
     lists = zip(user_list, user_status)
     data = ([user for user in lists])
     
     return render(request, 'userStatus.html', {'data':data})