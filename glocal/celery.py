from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glocal.settings')

app = Celery('glocal')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

"""
django + redis + celery 연결 및 목적 + 작업 방법

redis install 알아서 - https://redis.io/download

redis server run port = default(6379)
redis-server # server run
redis-cli ping # server test 성공시 PONG 응답

celery + redis 관련 lib 설치
pip install -r requirements.txt

settings.py 에 celery broker + backend 설정
settings.py 이 존재하는 같은 폴더에 celery.py 파일 추가(지금 보고 있는 파일)
장고 프로젝트 폴더 __init__.py에 셀러리 앱 설정

모든 앱 폴더안에 tasks.py 파일을 만들면 사용 가능

accounts app 안에 tasks.py 파일 참조

task에 job들을 실제 코드에서 call 하는 부분 notice app에 views.py 파일 참조

 
shell 에서 셀러리 worker 실행(이미 redis server는 run 되고 있는 상황) - manage.py 파일이 있는 위치에서 실행
celery -A glocal worker -l info

그럼 실제 테스트를 돌려보면 됨

사용 목적 - 작업시간이 오래 걸리는 작업들(푸쉬 보내기,메일 보내기,파일 압축하기등 사용자가 기다릴 이유가 없는 일들)을 task로 실행 django에서는 그냥 호출만 함( 응답을 기다리지 않음)


결과 
뷰에 있는 task를 호출하면 redis에 할일 등록
셀러리 워커가 redis에 할일 목록을 가져와 작업
그에 대한 결과를 redis에 알림 끝

누가 이쁘게 문서로 만들면 좋겠음

"""
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))