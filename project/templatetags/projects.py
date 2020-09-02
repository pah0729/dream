from django import template
from project.models import Todo


register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_todo_list(context):

    user = context['request'].user.profile
    if user is None:
        return None

    return [{
        "id": t.get('id'),
        "user": t.get('user'),
        "num": t.get('num'),
        "targets": t.get('targets'),
        "content": t.get('content'),
        "condition": t.get('condition'),
        "important": t.get('important'),
        "sdate": t.get('sdate'),
        "edate": t.get('edate')
    } for t in Todo.objects.filter(user=user, condition="진행").order_by('-pk').values(
        'id', 'user', 'num', 'targets', 'content',
        'condition', 'important', 'sdate', 'edate')]