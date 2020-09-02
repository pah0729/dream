from django import template

from accounts.models import Profile, AnnualApprovalLine


register = template.Library()


@register.simple_tag(takes_context=True)
def get_approvals(context):
    approvals = []
    user = context['request'].user.profile
    approvals.append(user)
    temp_user = None
    while(True):
        try:
            if temp_user is None:
                temp_user = user
            temp = AnnualApprovalLine.objects.get(manager=temp_user)
            temp_user = temp.approval
        except:
            break
        
        if temp.approval is None:
            break
        else:
            approvals.append(temp.approval)
            
    return approvals