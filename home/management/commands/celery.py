import shlex, os
import subprocess
from accounts.slack import opererror_slack
from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload
#from django.utils.autoreload import autoreload_started


def restart_celery(*args, **kwargs):
    try:
        cmd = 'pkill -9 -f celery'
        subprocess.call(shlex.split(cmd))
        cmd = 'celery -A glocal worker -l info'
        subprocess.call(shlex.split(cmd))
    except OSError:
        raise CommandError('Celery reload error....')


class Command(BaseCommand):
    """ 가상 환경 진입 후 manage.py 파일 있는 위치에서 python manage.py cellery 명령시 작동 됨 """
    """ restart_celery(args=None, kwargs=None) 사용시 명령어로만 리로딩 됨 """
    """ autoreload.run_with_reloader 사용시 소스 변경시 자동 리로딩 됨 """
    """ autoreload시 celery에 job들이 초기화 됨 """

    help = 'celery auto reload 담당'

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        try:
            #restart_celery(args=None, kwargs=None)
            autoreload.run_with_reloader(restart_celery, args=None, kwargs=None)
        except CommandError:
            content = [{"title":"celery.py","text":"celery reload failed"}]
            opererror_slack(attachments=content)
            self.stdout.write(self.style.ERROR('Celery reload failed'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully celery reload '))