# """
# python manage.py createusergroup을 통해 만들어진 그룹에 사용자를 추가한다.
# """
#
# # 1단계 : python manage.py createusergroup을 통해 만들어진 그룹에 사용자를 추가한다.
#
# from django.contrib.auth.models import Group
# from django.core.management.base import BaseCommand
# from rest_framework.authtoken.models import Token
#
# from accounts.models import User
# from perf_mgr.models import MemberWorkProfile
#
#
# # 2단계 : python manage.py createuser를 통해 사용자를 추가한다.
#
# class Command(BaseCommand):
#
#     def create_user(self, username, first_name, job_name, team_name,region_name, group_name):
#
#         # Login용 사용자 생성
#         user = User.objects.create_user(
#             username=username,
#             email='t@t.com',
#             password='1111',
#             first_name=first_name,
#             last_name='',
#             phone_number='010-1234-5678',
#             is_active=True,
#             is_staff=False,
#             is_superuser=False,
#             region_name='Access담당',
#             team_name=team_name,
#             job_name=job_name,
#         )
#
#         token = Token.objects.create(user=user)
#
#         # 보관용 User DB instance 생성
#         MemberWorkProfile.objects.create(
#             username=username,
#             first_name=first_name,
#             region_name=region_name,
#             team_name=team_name,
#             job_name=job_name,
#         )
#
#
#         if group_name :
#             group = Group.objects.get(name=group_name)
#             group.user_set.add(user)
#
#         print(f'username: {username}, first_name: {first_name}, job_name: {job_name}, team_name: {team_name}, group_name: {group_name}')
#
#
#     def handle(self, *args, **options):
#
#         self.create_user('dev1', '김팀장', 'Team Leader', 'DevOps TF','Access담당', 'team_leader')
#         self.create_user('dev2', '김팀원', '팀원', 'DevOps TF','Access담당', 'supporter')
#         self.create_user('dev3', '이팀원', '팀원', 'DevOps TF','Access담당', '')
#         self.create_user('dev4', '박팀원', '팀원', 'DevOps TF','Access담당', '')
#         self.create_user('dev5', '최팀원', '팀원', 'DevOps TF','Access담당', '')
#         self.create_user('dev6', '안팀원', '팀원', 'DevOps TF','Access담당', 'sys_manager')
#
#         self.create_user('hr1', '김팀장', 'Team Leader', 'HR팀', '기업문화', 'team_leader')
#         self.create_user('hr2', '김팀원', '팀원', 'HR팀', '기업문화', 'supporter')
#         self.create_user('hr3', '이팀원', '팀원', 'HR팀', '기업문화', '')
#         self.create_user('hr4', '박팀원', '팀원', 'HR팀', '기업문화', '')
#         self.create_user('hr5', '최팀원', '팀원', 'HR팀', '기업문화', '')
#         self.create_user('hr6', '안팀원', '팀원', 'HR팀', '기업문화', 'sys_manager')
#
#
#
#
#         mygroup = Group.objects.get(name='team_leader')
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#         for user in users:
#             print(mygroup.name, user.username, user.first_name)  # 사용자 이름 출력
#
#
#         mygroup = Group.objects.get(name='supporter')
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#         for user in users:
#             print(mygroup.name, user.username, user.first_name)  # 사용자 이름 출력
#
#         mygroup = Group.objects.get(name='sys_manager')
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#
#         users = mygroup.user_set.all()  # mygroup에 속한 모든 사용자를 조회
#         for user in users:
#             print(mygroup.name, user.username, user.first_name)  # 사용자 이름 출력
