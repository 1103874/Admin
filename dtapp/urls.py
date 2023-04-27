from django.urls import path
from . import views, export
from django.views.generic import TemplateView

## DevOps 앱 게시판
app_name = 'dtapp'

urlpatterns = [

    ## SRreview App
    path('srReview/', views.sr_list, name='srReview-list'),
    path('srReview/<int:sr_id>/', views.srDetailView.as_view(), name='srReview-detail'),
    path('srReview/new/', views.srCreateView.as_view(), name='srReview-create'),
    # path('srReview/<int:sr_id>/delete/', views.sr_delete, name='srReview-delete'),
    path('srReview/<int:sr_id>/delete/', views.srDeleteView.as_view(), name='srReview-delete'),
    path('srReview/<int:sr_id>/edit/', views.srUpdateView.as_view(), name='srReview-update'),
    path('srReview/chart/', views.sr_chart, name='srReview-chart'),

    ## CEItree App
    path('ceiTree/index/', views.ceiTree_index, name='ceiTree-index'),
    path('ceiTree/', views.ceiTree_list, name='ceiTree-list'),
    path('ceiTree/<str:inputqoe>', views.ceiTree_list2, name='ceiTree_list2'),  ## HDV_QoE1, DATA_QoE1.. 형식 리스트
    path('ceiTree/group/<str:group>/', views.ceiTree_list3, name='ceiTree_list3'),  ## HDV_, DATA_ 분류 형식 리스트
    path('ceiTree/type/<str:baduser>/', views.ceiTree_list4, name='ceiTree_list4'),  ## OOO_배드유저 형식 리스트
    path('ceiTree/type/HDV_단절', views.ceiTree_list5, name='ceiTree_list5'),  ## 종합_단절, HDV_단절 형식 리스트
    path('ceiTree/type/HDV_커버리지', views.ceiTree_list6, name='ceiTree_list6'),  ## 종합_커버리지, HDV_커버리지 형식 리스트
    path('ceiTree/type/Data_단절', views.ceiTree_list7, name='ceiTree_list7'),  ## 종합_단절, Data_단절 형식 리스트
    path('ceiTree/type/Data_커버리지', views.ceiTree_list8, name='ceiTree_list8'),  ## 종합_커버리지, Data_커버리지 형식 리스트

    path('ceiTree/<int:cei_id>/', views.ceiTreeDetailView.as_view(), name='ceiTree-detail'),
    path('ceiTree/new/', views.ceiTreeCreateView.as_view(), name='ceiTree-create'),
    path('ceiTree/<int:cei_id>/delete/', views.ceiTreeDeleteView.as_view(), name='ceiTree-delete'),
    path('ceiTree/<int:cei_id>/edit/', views.ceiTreeUpdateView.as_view(), name='ceiTree-update'),
    path('ceiTree/work/ajax/load-types', views.load_types, name='ajax_load_types'),  # 구분 AJAX

    path('ceiTree/BM/', views.ceiTreeBM_list, name='ceiTreeBM-list'),
    path('ceiTree/BM/<int:cei_id>/', views.ceiTreeBMDetailView.as_view(), name='ceiTreeBM-detail'),
    path('ceiTree/BM/new/', views.ceiTreeBMCreateView.as_view(), name='ceiTreeBM-create'),
    path('ceiTree/BM/<int:cei_id>/delete/', views.ceiTreeBMDeleteView.as_view(), name='ceiTreeBM-delete'),
    path('ceiTree/BM/<int:cei_id>/edit/', views.ceiTreeBMUpdateView.as_view(), name='ceiTreeBM-update'),
    path('ceiTree/<int:cei_id>/', views.ceiTreeDetailView2.as_view(), name='ceiTreeBM-detail2'),

    path('ceiTree/download/', export.export_cei_tree, name='ceiTree-export'),

    ## 전사 Process & Guied App
    path('process/index/', views.ProcessGuide_index, name='processGuide-index'),
    path('process/', views.processGuide_list, name='processGuide-list'),
    path('process/<str:inputType>', views.processGuide_list2, name='processGuide-list2'),  ## 가이드_기술지원_RM, 프로세스_운용지원_운용.. 형식 리스트
    path('process/type1/<str:inputType2>', views.processGuide_list3, name='processGuide-list3'),  ## 가이드_기술지원_RM, 프로세스_운용지원_운용.. 형식 리스트

    path('process/new/', views.processGuideCreateView.as_view(), name='processGuide-create'),
    path('process/<int:process_id>/delete/', views.processGuideDeleteView.as_view(), name='processGuide-delete'),
    path('process/<int:process_id>/edit/', views.processGuideUpdateView.as_view(), name='processGuide-update'),

    path('process/ajax/load-types', views.load_process_types, name='process_ajax_load_types'),  # 구분 AJAX
    path('process/ajax/load-subtypes', views.load_process_subtypes, name='process_ajax_load_subtypes'),  # 세부구분 AJAX

    path('process/download/', export.export_processGuide, name='processGuide-export'),

]
