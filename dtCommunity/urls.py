from django.urls import path
from . import views
from django.views.generic import TemplateView

## DevOps 커뮤니티 게시판
app_name = 'dtCommunity'

urlpatterns = [

    ## Project App
    path('dtProject/', views.project_list, name='dtProject-list'),
    # path('dtProject/', views.IndexView.as_view(), name='dtProject-list'),
    # path('dtProject/new', views.project_create, name='dtProject-create'), # 함수형 뷰 호출
    path('dtProject/new', views.projectCreateView.as_view(), name='dtProject-create'), # 클래스형 뷰 호출
    # path('dtProject/<int:project_id>/', views.project_detail, name='dtProject-detail'),
    path('dtProject/<int:project_id>', views.projectDetailView.as_view(), name='dtProject-detail'),
    # path('dtProject/<int:project_id>/edit', views.project_update, name='dtProject-update'),
    path('dtProject/<int:project_id>/edit', views.projectUpdateView.as_view(), name='dtProject-update'),
    # path('dtProject/<int:project_id>/delete', views.project_delete, name='dtProject-delete'),
    path('dtProject/<int:project_id>/delete', views.projectDeleteView.as_view(), name='dtProject-delete'),





]