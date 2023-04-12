from urllib import request

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import projectPost
from .forms import projectForm


# Create your views here.

## Project List(함수 뷰)
def project_list(request):
    projects = projectPost.objects.all().order_by('-dt_created')
    paginator = Paginator(projects, 100)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'dtCommunity/dtProject/project_list.html', {'page': page})


## Project List(클래스_제네릭 뷰)
# class IndexView(ListView):
#     model = projectPost
#     template_name = "dtCommunity/dtProject/project_list.html"
#     context_object_name = "projects"
#     paginate_by = 2
#     ordering = ["-dt_created"]


## Project Detail
class projectDetailView(LoginRequiredMixin, DetailView):
    model = projectPost
    template_name = "dtCommunity/dtProject/project_detail.html"
    pk_url_kwarg = "project_id"
    context_object_name = 'project'


## Project Create
class projectCreateView(LoginRequiredMixin, CreateView):
    model = projectPost
    form_class = projectForm
    template_name = "dtCommunity/dtProject/project_form.html"
    pk_url_kwarg = "project_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dtCommunity:dtProject-detail", kwargs={"project_id": self.object.id})


## Project Delete(함수 뷰)
# def project_delete(request, project_id):
#     post = get_object_or_404(projectPost, pk=project_id)
#     post.delete()
#     return redirect('dtCommunity:dtProject-list')

## Project Delete(제네릭 뷰)
class projectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = projectPost
    template_name = 'dtCommunity/dtProject/project_delete.html'
    pk_url_kwarg = 'project_id'

    def get_success_url(self):
        return reverse('dtCommunity:dtProject-list')

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        projects = self.get_object()
        return projects.author == user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False


## Project Update
class projectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = projectPost
    form_class = projectForm
    template_name = 'dtCommunity/dtProject/project_form.html'
    pk_url_kwarg = 'project_id'

    def get_success_url(self):
        return reverse('dtCommunity:dtProject-detail', kwargs={'project_id': self.object.id})

    # 'UserPassesTestMixin'은 개발자가 정의하는 커스텀 테스트('test_func')를 통과하는 유저만 뷰에 접근이 가능
    def test_func(self):  # test_func는 뷰에 접근할 수 있으면 True, 없으면 False 리턴
        projects = self.get_object()
        return projects.author == user  # sr 모델의 글쓴이와 로그인한 user가 동일하면 True, 아니면 False
