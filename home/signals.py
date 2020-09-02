from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserLoginLog


def get_client_ip(request):
    default = '192.168.0.1'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
        if ip is None:
            return default

    return ip


@receiver(user_logged_in)
def login_user_logged_in(sender, user, request, **kwargs):
    """ 로그인시 로깅 """
    log = UserLoginLog()
    log.user = user
    log.ip_address = get_client_ip(request)
    log.user_agent = request.META['HTTP_USER_AGENT']
    log.save()
