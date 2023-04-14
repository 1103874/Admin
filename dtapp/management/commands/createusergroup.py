# from django.contrib.contenttypes.models import ContentType
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
#
# from perf_mgr.models import Feedback, TeamKPI, MemberWorkProfile
#
#
# class Command(BaseCommand):
#
#     help = 'create user group'
#
#     def handle(self, *args, **options):
#
#         # Code to execute when the command is run
#         self.stdout.write('Create user group : team_leader')
#
#         Group.objects.filter(name='team_leader').delete()
#
#         # create user group
#         new_group, created = Group.objects.get_or_create(name='team_leader')
#
#         ct = ContentType.objects.get_for_model(Feedback)
#         permission = Permission.objects.filter(content_type=ct)
#
#
#         # Group에 Permission 할당하기
#         for p in permission:
#             print(p.codename)
#             new_group.permissions.add(p)
#
#         ct = ContentType.objects.get_for_model(TeamKPI)
#         permission = Permission.objects.filter(content_type=ct)
#
#
#         # Group에 Permission 할당하기
#         for p in permission:
#             print(p.codename)
#             new_group.permissions.add(p)
#
#
#         # ----------------------------------------------------------------------
#         # Code to execute when the command is run
#         self.stdout.write('Create user group : supporter')
#
#         Group.objects.filter(name='supporter').delete()
#
#         # create user group
#         new_group, created = Group.objects.get_or_create(name='supporter')
#
#         ct = ContentType.objects.get_for_model(TeamKPI)
#         permission = Permission.objects.filter(content_type=ct)
#
#
#         # Group에 Permission 할당하기
#         for p in permission:
#             print(p.codename)
#             new_group.permissions.add(p)
#
#             # ----------------------------------------------------------------------
#             # Code to execute when the command is run
#             self.stdout.write('Create user group : sys_manager')
#
#             Group.objects.filter(name='sys_manager').delete()
#
#             # create user group
#             new_group, created = Group.objects.get_or_create(name='sys_manager')
#
#             ct = ContentType.objects.get_for_model(MemberWorkProfile)
#             permission = Permission.objects.filter(content_type=ct)
#
#             # Group에 Permission 할당하기
#             for p in permission:
#                 print(p.codename)
#                 new_group.permissions.add(p)
#
#
#
#
#
#
#
#
