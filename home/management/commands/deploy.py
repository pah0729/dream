import shlex, os
from subprocess import call, run, Popen
import platform
from accounts.slack import opererror_slack
from django.core.management.base import BaseCommand, CommandError
from glocal.secret import safe_get


def restart(*args, **kwargs):
    try:
        os_env = platform.system().upper()
        CONDA_ENV = safe_get('CONDA_ENV', 'glocal')

        if os_env.find('WINDOW') != -1:
            raise CommandError('Django reload shell error....')

        run('bash -c "source activate' + CONDA_ENV + '; python -V"', shell=True)
        
        cmd = 'git pull'
        call(shlex.split(cmd))

        cmd = 'pip install -r requirements.txt'
        call(shlex.split(cmd))

        cmd = 'python manage.py makemigrations'
        call(shlex.split(cmd))

        cmd = 'python manage.py migrate'
        call(shlex.split(cmd))

        cmd = 'python manage.py collectstatic --noinput'
        call(shlex.split(cmd))

        DEV_ENV = safe_get('DEV_ENV', 'server')

        if DEV_ENV == 'local':
            cmd = 'python manage.py runserver'
            call(shlex.split(cmd))
        else:
            cmd = 'sudo systemctl restart gunicorn nginx'
            passwd = safe_get('DEV_ENV_PASS')
            proc = Popen(shlex.split(cmd))
            proc.communicate(passwd)

    except OSError:
        raise CommandError('Django reload shell error....')


class Command(BaseCommand):

    """ Django reloading """

    help = 'Django deploy auto reload 담당'

    def handle(self, *args, **options):
        print('Starting Dajngo reload...')
        try:
            restart(args=None, kwargs=None)
        except CommandError:
            content = [{"title":"deploy.py","text":"deploy reload shell failed"}]
            opererror_slack(attachments=content)
            self.stdout.write(self.style.ERROR('Django reload faild'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully Django reload '))