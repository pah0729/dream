import os
import django
import schedule
import time

# pip install schedule
# 당일 10시

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glocal.settings")
django.setup()
from django.core.management.base import BaseCommand, CommandError
from annual.models import Annual, AnnualDate, MinusData
from accounts.models import Profile
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.core.mail import send_mail

def get_timestamp():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


def job():
    now = time.localtime()
    sid = transaction.savepoint()
    is_success = False
    is_msg = ''
    #print("annual_email start - " + get_timestamp())
    try:
        # 이메일발송
        datas = AnnualDate.objects.filter(is_active=False, is_delete=False)
        for user in Profile.objects.filter(user__is_superuser=False).exclude(user__is_active=False):
            #print('')
            #print('<<',user,'>>')
            annual = datas.filter(user=user)
            twomonth = date.today() - relativedelta(months=10)
            sixmonth = date.today() - relativedelta(months=6)
            twodata = annual.filter(ocrncDate = twomonth).count()
            sixdata = annual.filter(ocrncDate = sixmonth).count()
            #print('유효기간 6개월이하:',data,'개')
            if sixdata > 0 :
                reciever = [user.email_google]
                send_mail('(사)글로컬드림아카데미 연차 유효기간 알림', '연차 유효기간이 6개월 남았습니다. 기간 내 사용하지 않은 연차는 소멸되므로 유의하여주시기 바랍니다.', 'glocalgroupware@gmail.com', reciever)
                #print(user,reciever)
            if twodata > 0 :
                reciever = [user.email_google]
                send_mail('(사)글로컬드림아카데미 연차 유효기간 알림', '연차 유효기간이 2개월 남았습니다. 기간 내 사용하지 않은 연차는 소멸되므로 유의하여주시기 바랍니다.', 'glocalgroupware@gmail.com', reciever)
                #print(user,reciever)
        transaction.savepoint_commit(sid)
    except Exception as e :
        transaction.savepoint_rollback(sid)
        is_msg = '실패'
        push('annual_email Job Error', str(e))
    else:
        is_success = True
        is_msg = '성공'
        #print("annual_email end - " + get_timestamp())
    finally:
        is_msg = '성공'
        #end_time = time.localtime()
        #print('작업완료')

class Command(BaseCommand):
    """ 가상 환경 진입 후 manage.py 파일 있는 위치에서 python manage.py cellery 명령시 작동 됨 """
    """ restart_celery(args=None, kwargs=None) 사용시 명령어로만 리로딩 됨 """
    """ autoreload.run_with_reloader 사용시 소스 변경시 자동 리로딩 됨 """
    """ autoreload시 celery에 job들이 초기화 됨 """

    help = '연차 소멸'

    def handle(self, *args, **options):
        print('Starting annual email')
        try:
            #restart_celery(args=None, kwargs=None)
            job()
        except CommandError:
            self.stdout.write(self.style.ERROR('annual email error'))
        else:
            self.stdout.write(self.style.SUCCESS('annual email send success'))