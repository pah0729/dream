import os
import django
import schedule
import time

# pip install schedule
# 00시 05분

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glocal.settings")
django.setup()
from django.core.management.base import BaseCommand, CommandError
from annual.models import Annual, AnnualDate, MinusData
from datetime import date
from django.db import transaction

def get_timestamp():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


def job():
    #now = time.localtime()
    sid = transaction.savepoint()
    is_success = False
    is_msg = ''
    #print("annual_extnc start - " + get_timestamp())
    try:
        AnnualDate.get_extnc(date.today()).update(is_delete=True)
        #print('')
        #print('*** 오늘 소멸처리된 반차 개수:',AnnualDate.get_extnc(date.today()).update(is_delete=True),'개 ***')
        transaction.savepoint_commit(sid)
    except Exception as e :
        transaction.savepoint_rollback(sid)
        is_msg = '실패'
        #print('')
        #print('실패함')
        push('annual_extnc Job Error', str(e))
    else:
        is_success = True
        is_msg = '성공'
        #print("annual_extnc end - " + get_timestamp())
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
        print('Starting annual extnc')
        try:
            #restart_celery(args=None, kwargs=None)
            job()
        except CommandError:
            self.stdout.write(self.style.ERROR('annual extnc error'))
        else:
            self.stdout.write(self.style.SUCCESS('annual extnc success'))