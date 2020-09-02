import os
import django
import schedule
import time
from django.core.management.base import BaseCommand, CommandError
from annual.models import Annual, AnnualDate, MinusData
from commute.models import Commute
from datetime import date
from django.db import transaction

def get_timestamp():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

def job():
    now = time.localtime()
    sid = transaction.savepoint()
    is_success = False
    is_msg = ''
    #print("annual_use start - " + get_timestamp())
    try:
        # 모든 휴가원 중 최종승인 되었고 휴가일이 오늘인 것 가져옴
        annualAll = Annual.get_annual_day(date.today())
        annualAltrn = Annual.get_annual_altrn_day(date.today())
        annualEtc = Annual.get_annual_etc_day(date.today())
        today = date.today()
        # print('')
        # print('*** 오늘 연차 사용자 수:',annualAll.count(),'명 ***')
        # print('*** 오늘 대체휴무 사용자 수:',annualAltrn.count(),'명 ***')
        # print('*** 오늘 기타휴무 사용자 수:',annualEtc.count(),'명 ***')

        for annual in annualAll:
            user = annual.user
            # print('')
            # print('<<',user,'>>')
            # print('휴가종류:',annual.division)
            # print('사용일수:',annual.datediff)
            # print('남은반차개수:',AnnualDate.get_user_annualDate(user).count())
            
            # 출퇴근부에 그 날 작성된 기록이 없을때 실행
            if not Commute.objects.filter(user=user, date_commute__year=today.year, date_commute__month=today.month, date_commute__day=today.day):
                # print('출퇴근부 기록없음')
                # 사용가능한 연차가 있을때
                if len(AnnualDate.get_user_annualDate(user)):
                    # print('사용가능연차: 있음')
                    
                    # 연차 사용일 때
                    if annual.datediff != 0.5:
                        # 남은반차가 2개 이상일때만 한꺼번에 상환처리
                        if AnnualDate.get_user_annualDate(user).count() >= 2 :
                            annualdate = AnnualDate.get_user_annualDate(user).first()
                            annualdate.is_active = True
                            annualdate.finalUpdtd = date.today()
                            annualdate.save()
                            annualdate = AnnualDate.get_user_annualDate(user).first()
                            annualdate.finalUpdtd = date.today()
                            annualdate.is_active = True
                            annualdate.save()
                            # print('반차 2개 사용처리됨')
                            Commute.objects.create(user=user,condition='연차',local='36.7987729,127.0758844')
                            # print('출퇴근부 찍음')

                        # 남아있는 반차가 1개일때
                        else:
                            annualdate = AnnualDate.get_user_annualDate(user).first()
                            annualdate.finalUpdtd = date.today()
                            annualdate.is_active = True
                            annualdate.save()
                            # print('반차 1개 사용처리됨')
                            MinusData.pull_minusData(user, date.today())
                            # print('마이너스반차 1개 생성됨')
                            Commute.objects.create(user=user,condition='연차',local='36.7987729,127.0758844')
                            # print('출퇴근부 찍음')

                # 사용가능한 연차가 없을때
                else:
                    # print('사용가능연차: 없음')
                    # 당겨쓰는 연차
                    if annual.datediff != 0.5:
                        MinusData.pull_minusData(user, date.today())
                        MinusData.pull_minusData(user, date.today())
                        # print('마이너스반차 2개 생성됨')
                        Commute.objects.create(user=user,condition='연차',local='36.7987729,127.0758844')
                        # print('출퇴근부 찍음')

            # 출퇴근부에 오전반차 또는 오후반차가 찍혀있을때
            elif Commute.objects.filter(user=user, date_commute__year=today.year, date_commute__month=today.month, date_commute__day=today.day, condition="오전반차") or Commute.objects.filter(user=user, date_commute__year=today.year, date_commute__month=today.month, date_commute__day=today.day, condition="오후반차") :
                # print('출퇴근부에 반차 찍혀있음')
                # 사용가능한 연차가 있을때
                if len(AnnualDate.get_user_annualDate(user)):
                    # print('사용가능연차: 있음')
                    # 반차 사용일 때
                    if annual.datediff == 0.5 :
                        annualdate = AnnualDate.get_user_annualDate(user).first()
                        annualdate.finalUpdtd = date.today()
                        annualdate.is_active = True
                        annualdate.save()
                        # print('반차 1개 사용처리됨')
                else:
                    # print('사용가능연차: 없음')
                    # 당겨쓰는 반차
                    if annual.datediff == 0.5:
                        MinusData.pull_minusData(user, date.today())
                        # print('마이너스반차 1개 생성됨')

        for annualalt in annualAltrn:
            user1 = annualalt.user
            # print('')
            # print('<<',user1,'>>')
            # print('휴가종류:',annualalt.division)
            # print('사용일수:',annualalt.datediff)
            
            # 출퇴근부에 그 날 작성된 기록이 없을때 실행
            today = date.today()
            if not Commute.objects.filter(user=user1, date_commute__year=today.year, date_commute__month=today.month, date_commute__day=today.day):
                # print('출퇴근부 기록없음')
                # print('연차차감 없음')
                Commute.objects.create(user=user1, condition='연차', reason='대체휴무', local='36.7987729,127.0758844')
                # print('출퇴근부 찍음')

        for annualetc in annualEtc:
            user2 = annualetc.user
            # print('')
            # print('<<',user2,'>>')
            # print('휴가종류:',annualetc.division)
            # print('사유:',annualetc.divreason)
            # print('사용일수:',annualetc.datediff)
            
            # 출퇴근부에 그 날 작성된 기록이 없을때 실행
            today = date.today()
            if not Commute.objects.filter(user=user2, date_commute__year=today.year, date_commute__month=today.month, date_commute__day=today.day):
                # print('출퇴근부 기록없음')
                # print('연차차감 없음')
                Commute.objects.create(user=user2, condition='연차', reason=annualetc.divreason,local='36.7987729,127.0758844')
                # print('출퇴근부 찍음')

        transaction.savepoint_commit(sid)
    except Exception as e :
        transaction.savepoint_rollback(sid)
        is_msg = '실패'
        #print('')
        #print('실패함')
        push('annual_use Job Error', str(e))
    else:
        is_success = True
        is_msg = '성공'
        #print("annual_use end - " + get_timestamp())
    finally:
        is_msg = '성공'
        #end_time = time.localtime()
        #print('작업완료')


class Command(BaseCommand):
    """ 가상 환경 진입 후 manage.py 파일 있는 위치에서 python manage.py cellery 명령시 작동 됨 """
    """ restart_celery(args=None, kwargs=None) 사용시 명령어로만 리로딩 됨 """
    """ autoreload.run_with_reloader 사용시 소스 변경시 자동 리로딩 됨 """
    """ autoreload시 celery에 job들이 초기화 됨 """

    help = 'celery auto reload 담당'

    def handle(self, *args, **options):
        print('Starting annual use')
        try:
            #restart_celery(args=None, kwargs=None)
            job()
        except CommandError:
            self.stdout.write(self.style.ERROR('annual use error'))
        else:
            self.stdout.write(self.style.SUCCESS('annual use success'))