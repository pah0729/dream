import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glocal.settings")
django.setup()

from django.db import transaction
from django.contrib.auth.models import User
from accounts.models import Team, Position, Profile
from home.models import AcesStts
from annual.models import Annual, AnnualDate ,MinusData
from commute.models import Commute
from notice.models import Notice, NoticeTarget, Comment
from todo_list.models import TodoList
from project.models import Project, ProjectTarget, Todo, TodoComment




""" project Data init """





""" accounts App Data init """

team0 = Team.objects.create(name='총괄', disp='1')
team1 = Team.objects.create(name='교육운영팀', disp='2')
team2 = Team.objects.create(name='경영지원실', disp='3')
team3 = Team.objects.create(name='교육지원팀', disp='4')
team4 = Team.objects.create(name='과학팀', disp='5')
team5 = Team.objects.create(name='코딩팀', disp='6')
team6 = Team.objects.create(name='공예팀', disp='7')
team7 = Team.objects.create(name='요리팀', disp='8')
team8 = Team.objects.create(name='SI팀', disp='9')

position0 = Position.objects.create(name='사원', disp='999')
position1 = Position.objects.create(name='팀장', disp='3')
position2 = Position.objects.create(name='대표', disp='1')
position3 = Position.objects.create(name='국장', disp='2')
position4 = Position.objects.create(name='과장', disp='999')
position5 = Position.objects.create(name='실장', disp='999')

# 대표 1 년 이상 전달 동안 결근 X 

user0 = User.objects.create_user('장석민', 'user0@gamil.com', 'test1234')
Profile.objects.create(user=user0, userNum='A0000001',team=team0, position=position2,entry_date='2017-05-28',email_google='user0@gmail.com', email='user0@google.com', phone='010-0000-0001', residentNumber='000000-0000000' )
# 사무국장 1 년 이상 전달 동안 결근 X 
user1 = User.objects.create_user('이남정', 'user1@gamil.com', 'test1234')
Profile.objects.create(user=user1, userNum='A0000001',team=team0, position=position3,entry_date='2017-05-01',email_google='user1@gmail.com', email='user1@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# SI 팀장 1 년 이상 전달 동안 결근 X 
user2 = User.objects.create_user('임동규', 'user2@gamil.com', 'test1234')
Profile.objects.create(user=user2, userNum='A0000001',team=team8, position=position1,entry_date='2017-12-10',email_google='user2@gmail.com', email='user2@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# SI 사원 1 년 미만   결근 O 
user3 = User.objects.create_user('유수미', 'user3@gamil.com', 'test1234')
Profile.objects.create(user=user3, userNum='A0000001',team=team8, position=position0,entry_date='2018-12-28',email_google='user3@gmail.com', email='user3@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 요리 팀장 1 년 미만 전달 결근 X
user4 = User.objects.create_user('이수현', 'user4@gamil.com', 'test1234')
Profile.objects.create(user=user4, userNum='A0000001',team=team7, position=position1,entry_date='2018-10-10',email_google='user4@gmail.com', email='user4@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 요리 사원  1 년 미만 결근 X
user5 = User.objects.create_user('지정미', 'user5@gamil.com', 'test1234')
Profile.objects.create(user=user5, userNum='A0000001',team=team7, position=position0,entry_date='2019-04-10',email_google='user5@gmail.com', email='uesr5@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 코딩 팀장 1 년 미만 결근 X
user6 = User.objects.create_user('고은영', 'user6@gamil.com', 'test1234')
Profile.objects.create(user=user6, userNum='A0000001',team=team5, position=position1,entry_date='2018-12-10',email_google='user6@gmail.com', email='user6@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 코딩 사원  --  1 년 미만 결근 X
user7 = User.objects.create_user('황지영A', 'user7@gamil.com', 'test1234')
Profile.objects.create(user=user7, userNum='A0000001',team=team5, position=position0,entry_date='2018-04-10',email_google='user7@gmail.com', email='user7@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 과학 팀장 1 년 이상 결근 O
user8 = User.objects.create_user('장세영', 'user8@gamil.com', 'test1234')
Profile.objects.create(user=user8, userNum='A0000001',team=team4, position=position1,entry_date='2018-05-27',email_google='user8@gmail.com', email='user8@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
# 과학 사원  1 년 이상 결근 X
user9 = User.objects.create_user('황지영B', 'user9@gamil.com', 'test1234')
Profile.objects.create(user=user9, userNum='A0000001',team=team4, position=position0,entry_date='2018-06-27',email_google='user9@gmail.com', email='user9@google.com', phone='010-0000-0001', residentNumber='000000-0000000')
#교육운영팀 팀장 1 년 이상 결근 X
user10 = User.objects.create_user('이정란', 'user10@gamil.com', 'test1234')
Profile.objects.create(user=user10, userNum='A0000001',team=Team.objects.get(name='교육운영팀'), position=Position.objects.get(name='팀장'),entry_date='2018-06-15',email_google='user10@gmail.com', email='user10@google.com', phone='010-0000-0001', residentNumber='000000-0000000')


''' 연차 자동생성 배치 파일 생성 '''

AnnualDate.objects.create(user=Profile.objects.get(user__username='유수미'),ocrncDate='2019-01-28')
AnnualDate.objects.create(user=Profile.objects.get(user__username='유수미'),ocrncDate='2019-02-28')
AnnualDate.objects.create(user=Profile.objects.get(user__username='유수미'),ocrncDate='2019-03-28')
AnnualDate.objects.create(user=Profile.objects.get(user__username='유수미'),ocrncDate='2019-04-28')
AnnualDate.objects.create(user=Profile.objects.get(user__username='유수미'),ocrncDate='2019-01-28')

AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-06-27')
AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-07-27')
AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-08-27')
AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-09-27')
AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-10-27')
AnnualDate.objects.create(user=Profile.objects.get(user__username='장세영'),ocrncDate='2018-11-27')

AnnualDate.objects.create(user=Profile.objects.get(user__username='이남정'),ocrncDate='2018-09-01')
AnnualDate.objects.create(user=Profile.objects.get(user__username='이남정'),ocrncDate='2018-10-01')
AnnualDate.objects.create(user=Profile.objects.get(user__username='이남정'),ocrncDate='2018-11-01')
AnnualDate.objects.create(user=Profile.objects.get(user__username='이남정'),ocrncDate='2018-12-01')

AnnualDate.objects.create(user=Profile.objects.get(user__username='지정미'),ocrncDate='2018-12-01')

""" Todo App Data init """
# 유수미-SI팀 - 종요도 높음 - 완료 X 
TodoList.objects.create(userName=Profile.objects.get(user__username='유수미'),team=Team.objects.get(name='SI팀'),date='2019-06-05',content='투두리스트1-중요도높음',disp='12',important='1')
# 지정미-요리팀 - 종요도 보통 - 완료 X 
TodoList.objects.create(userName=Profile.objects.get(user__username='지정미'),team=Team.objects.get(name='요리팀'),date='2019-04-14',content='투두리스트2-중요도보통',disp='13',important='2')
# 장세영-과학팀 - 종요도 낮음 - 완료 X 
TodoList.objects.create(userName=Profile.objects.get(user__username='장세영'),team=Team.objects.get(name='과학팀'),date='2019-02-10',content='투두리스트3-중요도낮음',disp='15',important='3')

# 유수미-SI팀 - 종요도 보통 - 완료 o
TodoList.objects.create(userName=Profile.objects.get(user__username='유수미'),team=Team.objects.get(name='SI팀'),date='2019-06-05',content='투두리스트4-중요도보통',disp='16',important='2', cmplt=True, cmpltDate='2019-06-15' )
# 지정미-요리팀 - 종요도 낮음 - 완료 o
TodoList.objects.create(userName=Profile.objects.get(user__username='지정미'),team=Team.objects.get(name='요리팀'),date='2019-04-14',content='투두리스트5-중요도낮음',disp='18',important='3',cmplt=True, cmpltDate='2019-05-25' )
# 장세영-과학팀 - 종요도 높음 - 완료 o
TodoList.objects.create(userName=Profile.objects.get(user__username='장세영'),team=Team.objects.get(name='과학팀'),date='2019-02-14',content='투두리스트6-중요도높음',disp='5',important='1',cmplt=True, cmpltDate='2019-03-20' )




""" commute App Data init """
# 장석민 출근
Commute.objects.create(user=Profile.objects.get(user__username='장석민'),condition='출근',local='36.808969600000005,127.07144439999999')

# 장석민 퇴근
Commute.objects.create(user=Profile.objects.get(user__username='장석민'),condition='퇴근',local='36.808969600000005,127.07144439999999')

# 지정미 외근
Commute.objects.create(user=Profile.objects.get(user__username='지정미'),condition='외근',local='36.808969600000005,127.07144439999999')

# 유수미 결근 -연차계없음 (1년 미만)
Commute.objects.create(user=Profile.objects.get(user__username='유수미'),condition='결근',local='36.808969600000005,127.07144439999999')

# 장세영 결근 -연차계없음 (1년 이상)
Commute.objects.create(user=Profile.objects.get(user__username='장세영'),condition='결근',local='36.808969600000005,127.07144439999999')

# 이수현 반차
Commute.objects.create(user=Profile.objects.get(user__username='이수현'),condition='오후반차',local='36.808969600000005,127.07144439999999')

# 이남정 결근 연차계있음


""" Notice App Data init """

# 1번 게시글 
notice1 = Notice.objects.create(user=Profile.objects.get(user__username='장석민'),team=Team.objects.get(name='총괄'),title='서울국제유아교육전&키즈페어',content='서울국제유아교육전&키즈페어 무료초대권 나눠드리려 합니다!관심 있으신 분들은 저에게 오시면 드리겠습니다초대권이 많이 있으니 가족분들 것도가져가셔도 됩니다~감사합니다 : )',targets='고은영,유수미,이남정,이수현,임동규',date='2019-06-21')

# 1번 게시글-읽음여부
NoticeTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=notice1, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=notice1, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='이남정'), num=notice1, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='이수현'), num=notice1, read=False)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='임동규'), num=notice1, read=False)

# 1번 게시글-댓글
Comment.objects.create(user=Profile.objects.get(user__username='유수미'), content="확인했습니다.", date='2019-06-21', num=notice1)

# 2번 게시글
notice2 = Notice.objects.create(user=Profile.objects.get(user__username='이남정'),team=Team.objects.get(name='총괄'), title='공지합니다.',content='글로컬 특성상 수업 나가시는 선생님들이 많으신데 전기 사용 관리가 잘되지 않아서 공지합니다. * 수업 나가시거나 자리를 30분 이상 비우게 되는 경우 자기 PC 전원은 꼭 꺼주시길 바랍니다.* 마지막으로 사무실에서 나가시는 선생님은 꼭 불을 꺼주시길 바랍니다.* 나가시기 전에 에어컨 전원도 꼭 확인해주시길 바랍니다.',targets='황지영,이수현,임동규,지정미',date='2019-06-20')

# 2번 게시글-읽음여부
NoticeTarget.objects.create(user=Profile.objects.get(user__username='황지영'), num=notice2, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='이수현'), num=notice2, read=False)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='임동규'), num=notice2, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='지정미'), num=notice2, read=False)

# 2번 게시글-댓글 
Comment.objects.create(user=Profile.objects.get(user__username='지정미'), content="확인했습니다.", date='2019-06-22', num=notice2)

# 3번 게시글
notice3 = Notice.objects.create(user=Profile.objects.get(user__username='지정미'),team=Team.objects.get(name='요리팀'), title='박람회 견학 관련 공지',content='박람회 견학을 진행합니다.전 직원 참석은 어려워 각팀에서 한두명씩 스케줄을 고려하여  선정하였습니다.일자- 7월11일 목요일 서울국제유아교육전 키즈페어장소-서울 코엑스출발-오전 9시 사무실 모여서 차량 2대로 출발출장 갈사람들 명단입니다.김태희, 정혜윤, 조은영, 김희준, 김아람, 황지영B, 이정인, 김길일부 사람은 스케줄 조정이 가능한지 여부 확인하여주세요.',targets='이수현,장세영,장석민',date='2019-05-19')

# 3번 게시글-읽음여부
NoticeTarget.objects.create(user=Profile.objects.get(user__username='장석민'), num=notice3, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='이수현'), num=notice3, read=True)
NoticeTarget.objects.create(user=Profile.objects.get(user__username='장세영'), num=notice3, read=True)

# 3번 게시글-댓글 
Comment.objects.create(user=Profile.objects.get(user__username='장세영'), content="확인했습니다.", date='2019-05-25', num=notice3)
Comment.objects.create(user=Profile.objects.get(user__username='이수현'), content="확인했습니다.", date='2019-05-26', num=notice3)

""" annual App Data init """

# < 연차 자동 발생 > - 

# 소멸일이 되었지만 사용하지 않은 연차

#연차 신청 - 팀장결제 X
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-20', fdate='2019-06-20', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='요청')

# 연차 신청 - 팀장결제 O 사무국장결제 X
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-21', fdate='2019-06-21', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='승인', teamleader='임동규')

# 연차 신청 - 팀장반려
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-22', fdate='2019-06-27', datediff='5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='반려', teamleader='임동규')

# 연차 신청 - 사무국장결제 O 대표결제 X
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-22', fdate='2019-06-22', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='사무국장', status='승인', teamleader='이남정')

# 연차 신청 - 사무국장반려
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-20', fdate='2019-06-20', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='사무국장', status='반려', teamleader='이남정')

# 연차 신청 - 대표 결제 O 
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-22', fdate='2019-06-22', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='승인', teamleader='장석민')

# 연차 신청 - 대표반려
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-22', fdate='2019-06-22', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='반려', teamleader='장석민')

# 반차 신청 - 결제 X
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-20', fdate='2019-06-20', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='요청')

# 반차 신청 - 팀장결제 O 사무국장결제 X
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-21', fdate='2019-06-21', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='승인', teamleader='임동규')

# 연차 신청 - 팀장반려
Annual.objects.create(user=Profile.objects.get(user__username='유수미'), team=Team.objects.get(name='SI팀'), position=Position.objects.get(name='사원'), division='연차', sdate='2019-07-22', fdate='2019-07-22', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='팀장', status='반려', teamleader='임동규')

# 반차 신청 - 사무국장결제 O 대표결제 X
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-22', fdate='2019-08-22', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='사무국장', status='승인', teamleader='이남정')

# 연차 신청 - 사무국장반려
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-07-20', fdate='2019-07-20', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='사무국장', status='반려', teamleader='이남정')

# 반차 신청 - 대표 O 대표결제 X
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-12', fdate='2019-08-12', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='승인', teamleader='장석민')

# 연차 신청 - 대표반려
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-08-17', fdate='2019-08-17', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='반려', teamleader='장석민')
  
# 반차 신청 - 대표 O 대표결제 
Annual.objects.create(user=Profile.objects.get(user__username='장세영'), team=Team.objects.get(name='과학팀'), position=Position.objects.get(name='팀장'), division='연차', sdate='2019-07-01', fdate='2019-07-01', datediff='0.5', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='승인', teamleader='장석민')

# 연차 신청 - 대표 O 대표결제 
Annual.objects.create(user=Profile.objects.get(user__username='이남정'), team=Team.objects.get(name='총괄'), position=Position.objects.get(name='국장'), division='연차', sdate='2019-06-28', fdate='2019-06-28', datediff='1', reason='사유', local='천안', relationship='언니', network='010-9512-5265', remark='기타사유', step='센터장', status='승인', teamleader='장석민')



# 마이너스 연차일 경우

MinusData.objects.create(user=Profile.objects.get(user__username='지정미'), ocrncDate='2019-06-01')
MinusData.objects.create(user=Profile.objects.get(user__username='지정미'), ocrncDate='2019-06-20')

# 상환 o 
MinusData.objects.create(user=Profile.objects.get(user__username='지정미'), ocrncDate='2019-06-01', payback= True)


""" home App Data init """

# 1회
AcesStts.objects.create(user=Profile.objects.get(user__username='지정미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='임동규'))

# 5회
AcesStts.objects.create(user=Profile.objects.get(user__username='장세영'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장세영'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장세영'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장세영'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장세영'))

# 10회
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))
AcesStts.objects.create(user=Profile.objects.get(user__username='유수미'))


# 15회
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))
AcesStts.objects.create(user=Profile.objects.get(user__username='장석민'))

# 20회
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))
AcesStts.objects.create(user=Profile.objects.get(user__username='이남정'))

""" project App Data init """

# 대기
project3= Project.objects.create(user=Profile.objects.get(user__username='장석민'), title='코딩팀 수업연계', content='수업연계 프로젝트입니다.', targets='고은영,유수미,이남정,이수현,임동규', sdate='2019-07-02', edate='2019-07-14')

ProjectTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=project3)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=project3)


Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project3, targets='고은영', content='todo1', condition='대기', important='높음', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project3, targets='유수미', content='todo2', condition='대기', important='낮음', sdate='2019-07-02', edate='2019-07-14')
# 중지
project4= Project.objects.create(user=Profile.objects.get(user__username='장석민'), title='과학팀 드론', content='드론 프로젝트입니다.', targets='고은영,유수미,이남정,이수현,임동규', sdate='2019-07-02', edate='2019-07-14')

ProjectTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=project4)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=project4)


Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project4, targets='고은영', content='todo1', condition='완료', important='높음', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project4, targets='유수미', content='todo2', condition='중지', important='낮음', sdate='2019-07-02', edate='2019-07-14')
# 완료
project5= Project.objects.create(user=Profile.objects.get(user__username='장석민'), title='과학팀 드론', content='드론 프로젝트입니다.', targets='고은영,유수미,이남정,이수현,임동규', sdate='2019-07-02', edate='2019-07-14')

ProjectTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=project5)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=project5)


Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project5, targets='고은영', content='todo1', condition='완료', important='높음', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project5, targets='유수미', content='todo2', condition='완료', important='낮음', sdate='2019-07-02', edate='2019-07-14')
# 진행 - %
project1= Project.objects.create(user=Profile.objects.get(user__username='장석민'), title='si팀 사내 그룹웨어 프로젝트', content='1. 출퇴근부 2. 공지사항 3. 연차관리 4. todolist 5. 스케줄관리', targets='고은영,유수미,이남정,이수현,임동규', sdate='2019-07-02', edate='2019-07-14')

ProjectTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=project1)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=project1)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='이수현'), num=project1)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='임동규'), num=project1)

Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1, targets='고은영', content='출퇴근부', condition='대기', important='높음', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1, targets='유수미', content='공지사항', condition='대기', important='낮음', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1, targets='이남정', content='todolist', condition='진행', important='보통', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1, targets='이수현', content='연차관리', condition='완료', important='보통', sdate='2019-07-02', edate='2019-07-14')
Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project1, targets='임동규', content='스케줄관리', condition='대기', important='높음', sdate='2019-07-02', edate='2019-07-14')

project2= Project.objects.create(user=Profile.objects.get(user__username='장석민'), title='소프트웨어팀 수납관리 프로젝트', content='수강생들의 수납관리를 할 수 있는 프로그램', targets='고은영,유수미,이남정,이수현,임동규', sdate='2019-07-12', edate='2019-07-17')

ProjectTarget.objects.create(user=Profile.objects.get(user__username='고은영'), num=project2)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='유수미'), num=project2)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='이수현'), num=project2)
ProjectTarget.objects.create(user=Profile.objects.get(user__username='임동규'), num=project2)

todo1= Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2, targets='고은영', content='todo1', condition='대기', important='높음', sdate='2019-07-02', edate='2019-07-14')
todo2=Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2, targets='유수미', content='todo2', condition='완료', important='낮음', sdate='2019-07-02', edate='2019-07-14')
todo3=Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2, targets='이남정', content='todo3', condition='진행', important='보통', sdate='2019-07-02', edate='2019-07-14')
todo4=Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2, targets='이수현', content='todo4', condition='완료', important='보통', sdate='2019-07-02', edate='2019-07-14')
todo5=Todo.objects.create(user=Profile.objects.get(user__username='이남정'), num=project2, targets='임동규', content='todo5', condition='완료', important='높음', sdate='2019-07-02', edate='2019-07-14')

TodoComment.objects.create(user=Profile.objects.get(user__username='유수미'), content='확인했습니다.', num=todo1)
TodoComment.objects.create(user=Profile.objects.get(user__username='유수미'), content='확인했습니다.', num=todo2)
TodoComment.objects.create(user=Profile.objects.get(user__username='유수미'), content='확인했습니다.', num=todo3)
TodoComment.objects.create(user=Profile.objects.get(user__username='유수미'), content='확인했습니다.', num=todo4)
TodoComment.objects.create(user=Profile.objects.get(user__username='유수미'), content='확인했습니다.', num=todo5)
