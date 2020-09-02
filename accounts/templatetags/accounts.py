from django import template

from accounts.models import Profile, Team
from notice.models import NoticeTarget
from annual.models import Annual


register = template.Library()


@register.simple_tag
def get_profile_list():
    return Profile.objects.filter(user__is_superuser=False).exclude(user__is_active=False ).order_by('pk')


@register.simple_tag
def get_team_list():
    return Team.objects.all().order_by('pk')


@register.simple_tag(takes_context=True)
def get_alram_notices(context):
    """ 공지사항 알람 리스트 가져오기"""
    user = context['request'].user.profile
    
    return NoticeTarget.objects.filter(user=user, read=False)


@register.simple_tag(takes_context=True)
def get_alram_confirms(context):
    """ 결제 알람 리스트 가져오기"""
    user = context['request'].user.profile
    confirms = []
    confirms = Annual.objects.filter(step__approval=user, status='대기')

    return confirms


@register.simple_tag(takes_context=True)
def get_alram_length(context):
    """ 전체 알람 크기 알아오기 """
    user = context['request'].user.profile
    notice_len = NoticeTarget.objects.filter(user=user, read=False).count()
    annual_len = Annual.objects.filter(step__approval=user, status='대기').count()

    return notice_len + annual_len


@register.simple_tag(takes_context=True)
def get_user_org_list(context):

    user = context['request'].user.profile
    if user is None:
        return None

    return [{
        "id": t.get('id'),
        "user": t.get('user__username'),
        "userImg": t.get('userImg'),
        "team": t.get('team__name'),
        "position": t.get('position__name'),
        "email_google": t.get('email_google'),
        "email": t.get('email'),
        "phone": t.get('phone')
    } for t in Profile.objects.filter(user__is_active=True).order_by('-pk').values(
        'id', 'user__username', 'userImg', 'team__name', 'position__name',
        'email_google', 'email', 'phone')]
