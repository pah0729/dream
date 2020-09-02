import os
import django
import schedule
import time

# pip install schedule
# 당일 12시 00분


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glocal.settings")
django.setup()
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from accounts.models import Profile
from annual.models import Annual, AnnualDate, MinusData
from commute.models import Commute
from datetime import date
from dateutil.relativedelta import relativedelta

def get_timestamp():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

def job():
    sid = transaction.savepoint()
    is_success = False
    is_msg = ''
    #print("annual_create start - " + get_timestamp())
    try:
        for user in Profile.objects.filter(user__is_superuser=False).exclude(user__is_active=False) :
            #print('')
            #print('<<',user,'>>')
            # 근속연수 계산
            tenures = int(((date.today() - user.entry_date).days + 1) / 365)
            #print('* 근속연수:',tenures)
            # 근속연수가 1년 미만일 경우, 월차의 개념으로 달마다 1개씩 발생
            if tenures < 1 :
                #print('(1년미만: 월차)')
                
                # 입사일 + 1달이 오늘이면 연차 발생
                if user.entry_date.day == date.today().day and user.entry_date.month != date.today().month:
                #if (i.entry_date + relativedelta(months=1))== date.today() or (i.entry_date + relativedelta(months=2))== date.today() or (i.entry_date + relativedelta(months=3))== date.today() or (i.entry_date + relativedelta(months=4))== date.today() or (i.entry_date + relativedelta(months=5))== date.today() or (i.entry_date + relativedelta(months=6))== date.today() or (i.entry_date + relativedelta(months=7))== date.today() or (i.entry_date + relativedelta(months=8))== date.today() or (i.entry_date + relativedelta(months=9))== date.today() or (i.entry_date + relativedelta(months=10))== date.today() or (i.entry_date + relativedelta(months=11))== date.today() :
                    #print('* 연차발생: True')

                    # 연차 발생일 전 한 달 동안의 출퇴근 기록에 결근이 있는지 체크, 있으면 해당 월에는 연차가 발생하지 않음
                    plus = (date.today() - relativedelta(months=1))
                    if not Commute.is_absenteeism(user,plus,date.today()):
                        #print('* 결근: 없음')
                        
                        # 상환되지 않은 마이너스 연차가 있을 때
                        if MinusData.objects.filter(user=user, payback=False).first() is not None :
                            #print('* 마이너스: 있음')

                            # 마이너스 연차가 반차일 때
                            if MinusData.objects.filter(user=user, payback=False).count() == 1:
                                #print('마이너스종류: 반차')
                                minusdata = MinusData.objects.filter(user=user, payback=False).first()
                                minusdata.payback = True # 마이너스 연차 상환처리
                                minusdata.save()
                                #print('반차상환 완료')
                                #AnnualDate.objects.create(user=user, ocrncDate=date.today()) # 반차발생
                                AnnualDate.objects.create(user=user, ocrncDate=date.today(), is_active=True, memo='자동발생 (마이너스연차 자동삭감)', finalUpdtd=minusdata.ocrncDate)
                                AnnualDate.pull_ocrnc(user, date.today())
                                #print('반차 1개 발생됨')

                            # 마이너스 연차가 반차가 아닐 때
                            else : 
                                    #print('마이너스종류: 연차')
                                    for minusdata in range(2):
                                        minusdata = MinusData.objects.filter(user=user, payback=False).first()
                                        minusdata.payback = True # 마이너스 연차 상환처리
                                        minusdata.save()
                                        AnnualDate.objects.create(user=user, ocrncDate=date.today(), is_active=True, memo='자동발생 (마이너스연차 자동삭감)', finalUpdtd=minusdata.ocrncDate)
                                        #print('연차상환 완료')

                        # 마이너스 연차가 없을 때
                        else:	
                            #print('* 마이너스: 없음')
                            for create in range(2):
                                #create = AnnualDate.objects.create(user=user, ocrncDate=date.today()) # 연차 발생
                                create = AnnualDate.pull_ocrnc(user, date.today())
                                #print('반차 1개 발생됨')
                        
            # 근속연수가 1년 이상일 때
            elif tenures >= 1 :
                #print('(1년이상)')
                # 입사일 + 1년이 오늘이면 연차 발생
                #if  (i.entry_date + relativedelta(years=1)) == date.today() :
                if  user.entry_date.strftime('%m%d') == date.today().strftime('%m%d') :
                    #print(user, '* 연차발생: True')

                    # 15개 + 근속 연수 2년 마다 1개씩 추가 발생
                    j = 15 + int(((tenures - 1) / 2))
                    #print('* 발생개수:',j)
                    for k in range(j):
    
                        # 상환되지 않은 마이너스 연차가 있을 떄
                        if MinusData.objects.filter(user=user, payback=False).first() is not None :
                            #print(user,'* 마이너스: 있음')

                            # 마이너스 연차가 반차일 때
                            if MinusData.objects.filter(user=user, payback=False).count() == 1:
                                #print('마이너스종류: 반차')
                                minusdata = MinusData.objects.filter(user=user, payback=False).first()
                                minusdata.payback = True # 마이너스 연차 상환처리
                                minusdata.save()
                                #AnnualDate.objects.create(user=user, ocrncDate=date.today()) # 반차발생
                                AnnualDate.pull_ocrnc(user, date.today())
                                AnnualDate.objects.create(user=user, ocrncDate=date.today(), is_active=True, memo='자동발생 (마이너스연차 자동삭감)', finalUpdtd=minusdata.ocrncDate)
                                #print('반차 1개 발생됨')

                            # 마이너스 연차가 반차가 아닐 때
                            else : 
                                    #print('마이너스종류: 연차')
                                    for minusdata in range(2):
                                        minusdata = MinusData.objects.filter(user=user, payback=False).first()
                                        minusdata.payback = True # 마이너스 연차 상환처리
                                        minusdata.save()
                                        AnnualDate.objects.create(user=user, ocrncDate=date.today(), is_active=True, memo='자동발생 (마이너스연차 자동삭감)', finalUpdtd=minusdata.ocrncDate)
                                        #print('연차상환 완료')

                        # 마이너스 연차가 없을 때
                        else:
                            #print(user,'* 마이너스: 없음')
                            for create in range(2):
                                #create = AnnualDate.objects.create(user=user, ocrncDate=date.today()) # 연차 발생
                                create = AnnualDate.pull_ocrnc(user, date.today())
                                #print('반차 1개 발생됨')

        transaction.savepoint_commit(sid)
    except Exception as e :
        transaction.savepoint_rollback(sid)
        is_msg = '실패'
        #print('')
        #print('실패함')
    else:
        is_success = True
        is_msg = '성공'
        #print("annual_create end - " + get_timestamp())
    finally:
        is_msg = '성공'
        #print('작업완료')


class Command(BaseCommand):
    """ 가상 환경 진입 후 manage.py 파일 있는 위치에서 python manage.py cellery 명령시 작동 됨 """
    """ restart_celery(args=None, kwargs=None) 사용시 명령어로만 리로딩 됨 """
    """ autoreload.run_with_reloader 사용시 소스 변경시 자동 리로딩 됨 """
    """ autoreload시 celery에 job들이 초기화 됨 """

    help = '연차 소멸'

    def handle(self, *args, **options):
        print('Starting annual create')
        try:
            #restart_celery(args=None, kwargs=None)
            job()
        except CommandError:
            self.stdout.write(self.style.ERROR('annual create error'))
        else:
            self.stdout.write(self.style.SUCCESS('annual create success'))