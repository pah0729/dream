import functools
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from .models import Annual
from accounts.models import Profile, AnnualApprovalLine


# 연차결재 validation check
def is_validation_action(profile):
    ret = []

    if AnnualApprovalLine.objects.filter(manager=profile, approval=None):
        ret.append('승인')
        ret.append('반려')

    elif AnnualApprovalLine.objects.filter(approval=profile):
        ret.append('대기')
        ret.append('반려')

    return ret


def annual_process_check(func=None,fail_url='/'):

    def decorator(view_func):
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            id = kwargs.get('pk')

            try:
                if request.user.profile.team is None or request.user.profile.position is None:
                    messages.error(request, '현재 사용자의 소속팀 또는 직급이 누락되어 접근할 수 없습니다.')
                    return HttpResponseRedirect(fail_url)
            except:
                messages.error(request, '현재 사용자의 소속팀 또는 직급이 누락되어 접근할 수 없습니다.')
                return HttpResponseRedirect(fail_url)

            confirm = None
            try:
                confirm = Annual.objects.get(pk=id)
            except:
                pass

            if confirm is None:
                messages.warning(request, '어디서 약을 팔어')
                return HttpResponseRedirect(fail_url)

            actions = is_validation_action(request.user.profile)
            task = AnnualApprovalLine.objects.all()

            # 결재권한 체크
            if not actions:
                if confirm.user.user.profile == request.user.profile:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.warning(request, '결재 권한이 없습니다.')
                    return HttpResponseRedirect(fail_url)

            # 연차결재라인 체크
            if not confirm.step.approval == request.user.profile :
                if confirm.finalApproval == False and confirm.step.manager == request.user.profile and confirm.step.approval == None:
                    return view_func(request, *args, **kwargs)
                elif confirm.finalApproval == False:
                    messages.warning(request, '결재가 불가능합니다.')
                    return HttpResponseRedirect(fail_url)
                else:
                    approvals = []
                    user = confirm.user.user.profile
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
                    
                    # print('신청자의 결재라인: ',approvals)

                    # 접근자가 결재권한을 가질경우 자기 하위에 있는 사원들의 휴가원만 열람가능
                    viewer = False
                    for users in approvals:
                        if users == request.user.profile:
                            viewer = True

                    if viewer == False:
                        messages.warning(request, '해당 휴가원 열람이 불가능합니다.')
                        return HttpResponseRedirect(fail_url)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    if func:
        return decorator(func)
    return decorator
