from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from pushbullet import Pushbullet

# debug/test 용 타임 스탬프
def getTime():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


@shared_task
def push_msg(token, title, message):
    try:
        if token == '':
            return False
        driver_push = Pushbullet(token)

        driver_push.push_note(title, message)
    except:
        print('push Error--')
        return False

    return True


@shared_task
def push_link(token, title, url):
    try:
        # test delay code
        # time.sleep(60)
        if token == '':
            return False

        driver_push = Pushbullet(token)
        driver_push.push_link(title, url)
    except:
        print('push Error--')
        return False

    return True