from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator  # Django의 Paginator
from django.db.models import Q, Count
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView

from .models import SRreview, CeiTreeList, CeiTreeBMList, Type, ProcessGuideList, Type2, Type3  # 사용 모델
from .forms import SRreviewForm, ceiTreeListForm, ceiTreeBMListForm, ProcessGuideListForm


# Create your views here.

### start SRreview App
## SR List
def sr_list(request):
    sr = SRreview.objects.all().order_by('-dt_created')
    paginator = Paginator(sr, 10000) # 한 페이지에 10개씩 보여주기
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)


    return render(request, 'dtapp/SRreview/SRreview_list.html', {'page': page})


## SR Detail
class srDetailView(LoginRequiredMixin, DetailView):
    model = SRreview
    template_name = "dtapp/SRreview/SRreview_detail.html"
    pk_url_kwarg = "sr_id"


## SR Create
class srCreateView(LoginRequiredMixin, CreateView):
    model = SRreview
    form_class = SRreviewForm
    template_name = "dtapp/SRreview/SRreview_form.html"
    pk_url_kwarg = "sr_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dtapp:srReview-detail", kwargs={"sr_id": self.object.id})


## SR Update
class srUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SRreview
    form_class = SRreviewForm
    template_name = 'dtapp/SRreview/SRreview_form.html'
    pk_url_kwarg = 'sr_id'

    def get_success_url(self):
        return reverse('dtapp:srReview-detail', kwargs={'sr_id': self.object.id})

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False


## SR Delete
# def sr_delete(request, sr_id):
#     sr = get_object_or_404(SRreview, pk=sr_id)
#     sr.delete()
#     return redirect('dtapp:srReview-list')

class srDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SRreview
    template_name = 'dtapp/SRreview/SRreview_delete.html'
    pk_url_kwarg = 'sr_id'

    def get_success_url(self):
        return reverse('dtapp:srReview-list')

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False


## SR Chart
@login_required()
def sr_chart(request):
    # region_list = ['안전보건', 'Access', 'AOC', 'Biz. 지원', 'Infra설비', 'SO', '전송', '기획운영', '기업문화', '수도권자산운영', '지역자산운영',
    #                '강남Access', '강북Access',
    #                '인천Access', '경기Access', '경남Access', '경북Access', '전남Access', '전북Access', '충남Access', '충북Access',
    #                '강원Access']
    region_list = sorted(list(set(SRreview.objects.values_list('region1', flat=True))))

    ## 대표이사 SR의 Chart data
    a = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='대표이사 BP').values_list('region1', flat=True))
    b = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='대표이사 BP').values_list('tot', flat=True))
    data1 = []

    for idx, region in enumerate(region_list):
        t = [idx2 for idx2, region2 in enumerate(a) if region2 == region]
        if len(t) > 0:
            data1.append(b[t[0]])
        else:
            data1.append(0)

    ## 경영지원담당 SR의 Chart data
    a = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='경영지원담당 BP').values_list('region1', flat=True))
    b = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='경영지원담당 BP').values_list('tot', flat=True))
    data2 = []

    for idx, region in enumerate(region_list):
        t = [idx2 for idx2, region2 in enumerate(a) if region2 == region]
        if len(t) > 0:
            data2.append(b[t[0]])
        else:
            data2.append(0)

    ## 기술지원담당 SR의 Chart data
    a = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='기술지원담당 BP').values_list('region1', flat=True))
    b = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='기술지원담당 BP').values_list('tot', flat=True))
    data3 = []

    for idx, region in enumerate(region_list):
        t = [idx2 for idx2, region2 in enumerate(a) if region2 == region]
        if len(t) > 0:
            data3.append(b[t[0]])
        else:
            data3.append(0)

    ## 운용지원담당 SR의 Chart data
    a = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='운용지원담당 BP').values_list('region1', flat=True))
    b = list(
        SRreview.objects.values('type', 'region1').annotate(
            tot=Count('region1')).filter(
            type='운용지원담당 BP').values_list('tot', flat=True))
    data4 = []

    for idx, region in enumerate(region_list):
        t = [idx2 for idx2, region2 in enumerate(a) if region2 == region]
        if len(t) > 0:
            data4.append(b[t[0]])
        else:
            data4.append(0)

    return render(request, 'dtapp/SRreview/SRreview_chart.html', context={'xaxis': region_list,
                                                                          'data1': data1,
                                                                          'data2': data2,
                                                                          'data3': data3,
                                                                          'data4': data4,
                                                                          })


### end SRreview App

## start CEItree App

def load_types(request):  ## AJAX
    work_group_id = request.GET.get('work_group_id')
    # work_types = Type.objects.filter(work_group_id=work_group_id).all()
    work_types = Type.objects.filter(work_group_id=work_group_id).order_by('name')
    return render(request, 'dtapp/CEItree/type_dropdown_list_options.html', {'work_types': work_types})


def ceiTree_index(request):
    hdv_categories = ['종합', '송수신', '음질', '단절', '커버리지']
    data_categories = ['종합', '접속', '화면전환', '단절', '속도', '커버리지']
    tot_sub_categories = ['단절', '커버리지']
    hdv_counts = []
    data_counts = []
    tot_sub_counts = []

    for category in hdv_categories:
        count = CeiTreeList.objects.filter(work_group__name='HDV', work_type__name=category).count()
        hdv_counts.append(count)

    for category in data_categories:
        count = CeiTreeList.objects.filter(work_group__name='DATA', work_type__name=category).count()
        data_counts.append(count)

    for category in tot_sub_categories:
        count = CeiTreeList.objects.filter(work_group__name='종합', work_type__name=category).count()
        tot_sub_counts.append(count)


    tot_count = CeiTreeList.objects.all().count()
    baduser_count = CeiTreeList.objects.filter(work_type__name='배드유저').count()


    context = {
        'hdv_categories': hdv_categories,
        'hdv_counts': hdv_counts,
        'data_categories': data_categories,
        'data_counts': data_counts,
        'tot_count': tot_count,
        'baduser_count': baduser_count,
        'tot_sub_categories': tot_sub_categories,
        'tot_sub_counts': tot_sub_counts,
    }


    return render(request, 'dtapp/CEItree/CEItree_index.html', context=context)


## CEItree List
def ceiTree_list(request):
    cei = CeiTreeList.objects.all().order_by('-dt_created')
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})


def ceiTree_list2(request, inputqoe): ## 모델 필드를 활용하여 HDV_QoE1, DATA_QoE1과 같은 inputqoe를 받아서 처리
    work_group__name, work_type__name = inputqoe.split('_')
    cei = CeiTreeList.objects.filter(work_group__name=work_group__name, work_type__name=work_type__name).all().order_by('-dt_created')
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})

def ceiTree_list3(request, group): ## 모델 필드를 활용하여 HDV, Data와 같은 group을 받아서 처리
    work_group__name = group
    cei = CeiTreeList.objects.filter(work_group__name=work_group__name).order_by('-dt_created')
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})
def ceiTree_list4(request, baduser): ## 모델 필드를 활용하여 HDV, Data와 같은 group을 받아서 처리
    work_type__name = baduser
    cei = CeiTreeList.objects.filter(work_type__name=work_type__name).order_by('-dt_created')
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})
def ceiTree_list5(request): ## 모델 필드를 활용하여 종합 단절, HDV 단절 type을 받아서 처리
    cei1 = CeiTreeList.objects.filter(work_group__name="종합", work_type__name="단절").order_by('-dt_created')
    cei2 = CeiTreeList.objects.filter(work_group__name="HDV", work_type__name="단절").order_by('-dt_created')
    cei = cei1 | cei2
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})
def ceiTree_list6(request): ## 모델 필드를 활용하여 종합 , HDV 커버리지 type을 받아서 처리
    cei1 = CeiTreeList.objects.filter(work_group__name="종합", work_type__name="커버리지").order_by('-dt_created')
    cei2 = CeiTreeList.objects.filter(work_group__name="HDV", work_type__name="커버리지").order_by('-dt_created')
    cei = cei1 | cei2
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})
def ceiTree_list7(request): ## 모델 필드를 활용하여 종합 단절, Data 단절 type을 받아서 처리
    cei1 = CeiTreeList.objects.filter(work_group__name="종합", work_type__name="단절").order_by('-dt_created')
    cei2 = CeiTreeList.objects.filter(work_group__name="Data", work_type__name="단절").order_by('-dt_created')
    cei = cei1 | cei2
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})
def ceiTree_list8(request): ## 모델 필드를 활용하여 종합 커버리지, Data 커버리지 type을 받아서 처리
    cei1 = CeiTreeList.objects.filter(work_group__name="종합", work_type__name="커버리지").order_by('-dt_created')
    cei2 = CeiTreeList.objects.filter(work_group__name="Data", work_type__name="커버리지").order_by('-dt_created')
    cei = cei1 | cei2
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list.html', {'page': page})


## CEItree Detail
class ceiTreeDetailView(DetailView):
    model = CeiTreeList
    template_name = "dtapp/CEItree/CEItree_detail.html"
    pk_url_kwarg = "cei_id"
    context_object_name = 'cei'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cei_hdv_before = self.object.cei_hdv_before
        cei_hdv_after = self.object.cei_hdv_after
        if cei_hdv_before is None or cei_hdv_after is None:
            cei_hdv_diff = "-"
        else:
            cei_hdv_diff = cei_hdv_after - cei_hdv_before
        cei_data_before = self.object.cei_data_before
        cei_data_after = self.object.cei_data_after
        if cei_data_before is None or cei_data_after is None:
            cei_data_diff = "-"
        else:
            cei_data_diff = cei_data_after - cei_data_before
        ber_hdv_before = self.object.ber_hdv_before
        ber_hdv_after = self.object.ber_hdv_after
        if ber_hdv_before is None or ber_hdv_after is None:
            ber_hdv_diff = "-"
        else:
            ber_hdv_diff = ber_hdv_after - ber_hdv_before
        ber_data_before = self.object.ber_data_before
        ber_data_after = self.object.ber_data_after
        if ber_data_before is None or ber_data_after is None:
            ber_data_diff = "-"
        else:
            ber_data_diff = ber_data_after - ber_data_before
        baduser_hdv_before = self.object.baduser_hdv_before
        baduser_hdv_after = self.object.baduser_hdv_after
        if baduser_hdv_before is None or baduser_hdv_after is None:
            baduser_hdv_diff = "-"
        else:
            baduser_hdv_diff = baduser_hdv_after - baduser_hdv_before
        baduser_data_before = self.object.baduser_data_before
        baduser_data_after = self.object.baduser_data_after
        if baduser_data_before is None or baduser_data_after is None:
            baduser_data_diff = "-"
        else:
            baduser_data_diff = baduser_data_after - baduser_data_before

        target_cei_before = self.object.target_cei_before
        target_cei_after = self.object.target_cei_after
        if target_cei_before is None or target_cei_after is None:
            target_cei_diff = "-"
        else:
            target_cei_diff = target_cei_after - target_cei_before


        context["cei_hdv_diff"] = cei_hdv_diff
        context["cei_data_diff"] = cei_data_diff
        context["ber_hdv_diff"] = ber_hdv_diff
        context["ber_data_diff"] = ber_data_diff
        context["baduser_hdv_diff"] = baduser_hdv_diff
        context["baduser_data_diff"] = baduser_data_diff

        context["target_cei_diff"] = target_cei_diff

        return context

## CEItree Create
class ceiTreeCreateView(LoginRequiredMixin, CreateView):
    model = CeiTreeList
    form_class = ceiTreeListForm
    template_name = "dtapp/CEItree/CEItree_form.html"
    pk_url_kwarg = "cei_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse("dtapp:ceiTree-detail", kwargs={"cei_id": self.object.id})
        return reverse("dtapp:ceiTree-index")


## CEItree Delete
class ceiTreeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CeiTreeList
    template_name = 'dtapp/CEItree/CEItree_delete.html'
    pk_url_kwarg = 'cei_id'

    def get_success_url(self):
        return reverse('dtapp:ceiTree-index')

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False


## CEItree Update
class ceiTreeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CeiTreeList
    form_class = ceiTreeListForm
    template_name = 'dtapp/CEItree/CEItree_form.html'
    pk_url_kwarg = 'cei_id'

    def get_success_url(self):
        # return reverse('dtapp:ceiTree-detail'
        #                , kwargs={'cei_id': self.object.id})
        return reverse("dtapp:ceiTree-index")

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False

## CEItree(BM) List
def ceiTreeBM_list(request):
    cei = CeiTreeBMList.objects.all().order_by('-dt_created')
    paginator = Paginator(cei, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/CEItree/CEItree_list_BM.html', {'page': page})

## CEItree(BM) Detail
class ceiTreeBMDetailView(DetailView):
    model = CeiTreeBMList
    template_name = "dtapp/CEItree/CEItree_detail_BM.html"
    pk_url_kwarg = "cei_id"
    context_object_name = 'cei'

## CEItree(BM) Detail에서 CEItree Detail로 이동
class ceiTreeDetailView2(DetailView):
    model = CeiTreeList
    template_name = "dtapp/CEItree/CEItree_detail_BM.html"
    pk_url_kwarg = "cei_id"
    context_object_name = 'cei'

## CEItree(BM) Create
class ceiTreeBMCreateView(LoginRequiredMixin, CreateView):
    model = CeiTreeBMList
    form_class = ceiTreeBMListForm
    template_name = "dtapp/CEItree/CEItree_form_BM.html"
    pk_url_kwarg = "cei_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dtapp:ceiTreeBM-detail", kwargs={"cei_id": self.object.id})
        # return reverse("dtapp:ceiTreeBM-list")


## CEItree(BM) Delete
class ceiTreeBMDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CeiTreeBMList
    template_name = 'dtapp/CEItree/CEItree_delete_BM.html'
    pk_url_kwarg = 'cei_id'

    def get_success_url(self):
        return reverse('dtapp:ceiTreeBM-list')

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False


## CEItree(BM) Update
class ceiTreeBMUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CeiTreeBMList
    form_class = ceiTreeBMListForm
    template_name = 'dtapp/CEItree/CEItree_form_BM.html'
    pk_url_kwarg = 'cei_id'

    def get_success_url(self):
        return reverse('dtapp:ceiTreeBM-detail'
                       , kwargs={'cei_id': self.object.id})

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return sr.author == self.request.user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False
## end CEItree App


## start 전사 Process & Guide App

## ProcessGuide 3단계 Dropdown List
def load_process_types(request):
    type1_id = request.GET.get('type1_id')
    type2 = Type2.objects.filter(type1_id=type1_id).order_by('name')
    return render(request, 'dtapp/ProcessGuide/type_dropdown_list_options.html', {'type2': type2})
def load_process_subtypes(request):
    type2_id = request.GET.get('type2_id')
    type3 = Type3.objects.filter(type2_id=type2_id).order_by('name')
    return render(request, 'dtapp/ProcessGuide/subtype_dropdown_list_options.html', {'type3': type3})

## ProcessGuide Index
def ProcessGuide_index(request):
    토탈 = 0
    가이드_기술지원_RM = 0
    가이드_기술지원_고객부정경험 = 0
    가이드_기술지원_구축 = 0
    가이드_기술지원_무선국 = 0
    가이드_기술지원_물자관리 = 0
    가이드_기술지원_시설물 = 0
    가이드_기술지원_운용 = 0
    가이드_기술지원_최적화 = 0
    가이드_기술지원_측정기 = 0
    가이드_운용지원_RM = 0
    가이드_운용지원_구축 = 0
    가이드_운용지원_시설물 = 0
    가이드_운용지원_운용 = 0
    가이드_운용지원_측정기 = 0
    프로세스_기술지원_RR = 0
    프로세스_기술지원_RM = 0
    프로세스_기술지원_Biz = 0
    프로세스_기술지원_운용 = 0
    프로세스_기술지원_고객부정경험 = 0
    프로세스_기술지원_구축 = 0
    프로세스_운용지원_RR = 0
    프로세스_운용지원_RM = 0
    프로세스_운용지원_구축 = 0
    프로세스_운용지원_운용 = 0
    안전보안_기술지원_안전 = 0
    안전보안_기술지원_운용 = 0
    안전보안_운용지원_안전 = 0
    안전보안_운용지원_운용 = 0
    표준운용보전지침_기술지원_안전 = 0
    표준운용보전지침_기술지원_운용 = 0
    표준운용보전지침_운용지원_안전 = 0
    표준운용보전지침_운용지원_운용 = 0

    토탈 = ProcessGuideList.objects.all().count()
    가이드_기술지원_RM = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='RM').count()
    가이드_기술지원_고객부정경험 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='고객부정경험').count()
    가이드_기술지원_구축 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='구축').count()
    가이드_기술지원_무선국 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='무선국').count()
    가이드_기술지원_물자관리 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='물자관리').count()
    가이드_기술지원_시설물 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='시설물').count()
    가이드_기술지원_운용 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='운용').count()
    가이드_기술지원_최적화 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='최적화').count()
    가이드_기술지원_측정기 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='기술지원', type3__name='측정기').count()
    가이드_운용지원_RM = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='운용지원', type3__name='RM').count()
    가이드_운용지원_구축 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='운용지원', type3__name='구축').count()
    가이드_운용지원_시설물 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='운용지원', type3__name='시설물').count()
    가이드_운용지원_운용 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='운용지원', type3__name='운용').count()
    가이드_운용지원_측정기 = ProcessGuideList.objects.filter(type1__name='가이드', type2__name='운용지원', type3__name='측정기').count()
    프로세스_기술지원_RR = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='R&R').count()
    프로세스_기술지원_RM = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='RM').count()
    프로세스_기술지원_Biz = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='Biz').count()
    프로세스_기술지원_운용 = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='운용').count()
    프로세스_기술지원_고객부정경험 = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='고객부정경험').count()
    프로세스_기술지원_구축 = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='기술지원', type3__name='구축').count()
    프로세스_운용지원_RR = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='운용지원', type3__name='R&R').count()
    프로세스_운용지원_RM = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='운용지원', type3__name='RM').count()
    프로세스_운용지원_구축 = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='운용지원', type3__name='구축').count()
    프로세스_운용지원_운용 = ProcessGuideList.objects.filter(type1__name='프로세스', type2__name='운용지원', type3__name='운용').count()
    안전보안_기술지원_안전 = ProcessGuideList.objects.filter(type1__name='안전/보안', type2__name='기술지원', type3__name='안전').count()
    안전보안_기술지원_운용 = ProcessGuideList.objects.filter(type1__name='안전/보안', type2__name='기술지원', type3__name='운용').count()
    안전보안_운용지원_안전 = ProcessGuideList.objects.filter(type1__name='안전/보안', type2__name='운용지원', type3__name='안전').count()
    안전보안_운용지원_운용 = ProcessGuideList.objects.filter(type1__name='안전/보안', type2__name='운용지원', type3__name='운용').count()
    표준운용보전지침_기술지원_안전 = ProcessGuideList.objects.filter(type1__name='표준운용보전지침', type2__name='기술지원', type3__name='안전').count()
    표준운용보전지침_기술지원_운용 = ProcessGuideList.objects.filter(type1__name='표준운용보전지침', type2__name='기술지원', type3__name='운용').count()
    표준운용보전지침_운용지원_안전 = ProcessGuideList.objects.filter(type1__name='표준운용보전지침', type2__name='운용지원', type3__name='안전').count()
    표준운용보전지침_운용지원_운용 = ProcessGuideList.objects.filter(type1__name='표준운용보전지침', type2__name='운용지원', type3__name='운용').count()

    context = {
        '토탈': 토탈,
        '가이드_기술지원_RM': 가이드_기술지원_RM,
        '가이드_기술지원_고객부정경험': 가이드_기술지원_고객부정경험,
        '가이드_기술지원_구축': 가이드_기술지원_구축,
        '가이드_기술지원_무선국': 가이드_기술지원_무선국,
        '가이드_기술지원_물자관리': 가이드_기술지원_물자관리,
        '가이드_기술지원_시설물': 가이드_기술지원_시설물,
        '가이드_기술지원_운용': 가이드_기술지원_운용,
        '가이드_기술지원_최적화': 가이드_기술지원_최적화,
        '가이드_기술지원_측정기': 가이드_기술지원_측정기,
        '가이드_운용지원_RM': 가이드_운용지원_RM,
        '가이드_운용지원_구축': 가이드_운용지원_구축,
        '가이드_운용지원_시설물': 가이드_운용지원_시설물,
        '가이드_운용지원_운용': 가이드_운용지원_운용,
        '가이드_운용지원_측정기': 가이드_운용지원_측정기,
        '프로세스_기술지원_RR': 프로세스_기술지원_RR,
        '프로세스_기술지원_RM': 프로세스_기술지원_RM,
        '프로세스_기술지원_Biz': 프로세스_기술지원_Biz,
        '프로세스_기술지원_운용': 프로세스_기술지원_운용,
        '프로세스_기술지원_고객부정경험': 프로세스_기술지원_고객부정경험,
        '프로세스_기술지원_구축': 프로세스_기술지원_구축,
        '프로세스_운용지원_RR': 프로세스_운용지원_RR,
        '프로세스_운용지원_RM': 프로세스_운용지원_RM,
        '프로세스_운용지원_구축': 프로세스_운용지원_구축,
        '프로세스_운용지원_운용': 프로세스_운용지원_운용,
        '안전보안_기술지원_안전': 안전보안_기술지원_안전,
        '안전보안_기술지원_운용': 안전보안_기술지원_운용,
        '안전보안_운용지원_안전': 안전보안_운용지원_안전,
        '안전보안_운용지원_운용': 안전보안_운용지원_운용,
        '표준운용보전지침_기술지원_안전': 표준운용보전지침_기술지원_안전,
        '표준운용보전지침_기술지원_운용': 표준운용보전지침_기술지원_운용,
        '표준운용보전지침_운용지원_안전': 표준운용보전지침_운용지원_안전,
        '표준운용보전지침_운용지원_운용': 표준운용보전지침_운용지원_운용,
    }

    return render(request, 'dtapp/ProcessGuide/ProcessGuide_index.html', context=context)





## ProcessGuide List
def processGuide_list(request):
    process = ProcessGuideList.objects.all().order_by('-dt_created')
    paginator = Paginator(process, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/ProcessGuide/ProcessGuide_list.html', {'page': page})
def processGuide_list2(request, inputType): ## 모델 필드를 활용하여 가이드_기술지원_RM, 프로세스_운용지원_운용 같은 inputType을 받아서 처리
    type1__name, type2__name, type3__name = inputType.split('_')
    process = ProcessGuideList.objects.filter(type1__name=type1__name, type2__name=type2__name, type3__name=type3__name).all().order_by('-dt_created')
    paginator = Paginator(process, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/ProcessGuide/ProcessGuide_list.html', {'page': page})
def processGuide_list3(request, inputType2): ## 모델 필드를 활용하여 가이드_기술지원_RM, 프로세스_운용지원_운용 같은 inputType을 받아서 처리
    type1__name = inputType2
    process = ProcessGuideList.objects.filter(type1__name=type1__name).all().order_by('-dt_created')
    paginator = Paginator(process, 10000)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtapp/ProcessGuide/ProcessGuide_list.html', {'page': page})




## ProcessGuide Create
class processGuideCreateView(LoginRequiredMixin, CreateView):
    model = ProcessGuideList
    form_class = ProcessGuideListForm
    template_name = "dtapp/ProcessGuide/ProcessGuide_form.html"
    pk_url_kwarg = "process_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse("dtapp:ceiTree-detail", kwargs={"cei_id": self.object.id})
        return reverse("dtapp:processGuide-index")

## ProcessGuide Delete
class processGuideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProcessGuideList
    template_name = 'dtapp/ProcessGuide/ProcessGuide_delete.html'
    pk_url_kwarg = 'process_id'

    def get_success_url(self):
        return reverse('dtapp:processGuide-index')

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return (sr.author == self.request.user) + (self.request.user.username=='admin') + (self.request.user.first_name=='인병렬') + (self.request.user.first_name=='최종언') + (self.request.user.first_name=='김희중') + (self.request.user.first_name=='조효상')  # 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False

## ProcessGuide Update
class processGuideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProcessGuideList
    form_class = ProcessGuideListForm
    template_name = 'dtapp/ProcessGuide/ProcessGuide_form.html'
    pk_url_kwarg = 'process_id'

    def get_success_url(self):
        # return reverse('dtapp:ceiTree-detail'
        #                , kwargs={'cei_id': self.object.id})
        return reverse("dtapp:processGuide-index")

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        sr = self.get_object()
        return (sr.author == self.request.user) + (self.request.user.username=='admin') + (self.request.user.first_name=='인병렬') + (self.request.user.first_name=='최종언') + (self.request.user.first_name=='김희중') + (self.request.user.first_name=='조효상')  # 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False

## end 전사 Process & Guide App
