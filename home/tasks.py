from __future__ import absolute_import, unicode_literals
from celery import shared_task
import shlex, os
from subprocess import call, run
import platform
from glocal.secret import safe_get

@shared_task
def reload():
    try:
        os_env = platform.system().upper()
        CONDA_ENV = safe_get('CONDA_ENV', 'glocal')

        if os_env.find('WINDOW') != -1:
            raise Exception('Django reload shell error....')

        run('bash -c "conda activate' + CONDA_ENV + '; python -V"', shell=True)

        cmd = 'python manage.py deploy'
        call(shlex.split(cmd))

    except:
        print('Reload Error')
        return False

    return True