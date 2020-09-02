import os
import django
import schedule
import time

# pip install schedule

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glocal.settings")
django.setup()


def get_timestamp():
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s


def job():
    print(get_timestamp())


try:
    schedule.every(1).minutes.do(job)
    """
    schedule.every().hour.do(job)
    schedule.every().day.at("10:30").do(job)
    schedule.every(5).to(10).minutes.do(job)
    schedule.every().monday.do(job)
    schedule.every().wednesday.at("13:15").do(job)
    schedule.every().minute.at(":17").do(job)
    """

except Exception as e:
    print("  Research_Schedule_Error - " + get_timestamp() + ' --- ' + str(e))


while True:
    schedule.run_pending()
    time.sleep(60)
    #time.sleep(1)
