from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

# from apps.models import User
from apps.validators import file_size
from auth_SKO.models import User


# Create your models here.

class projectPost(models.Model):

    TYPE_CHOICES = [
        ('기술지원', "기술지원"),
        ("운용지원", "운용지원"),
        ("경영지원", "경영지원"),
    ]
    type = models.CharField(max_length=10, verbose_name='구분', choices=TYPE_CHOICES, default="기술지원")

    STATUS_CHOICES = [
        ("기획/분석", "기획/분석"),
        ("설계", "설계"),
        ("구현", "구현"),
        ("테스트", "테스트"),
        ("상용화", "상용화"),
    ]
    status = models.CharField(max_length=10, verbose_name='진행단계', choices=STATUS_CHOICES, default="기획/분석")

    dt_start = models.DateField(verbose_name='시작일')
    dt_end = models.DateField(verbose_name='종료일')
    title = models.CharField(max_length=50, unique=True, verbose_name='과제명', error_messages={'unique': '이미 존재하는 제목입니다.'})
    content1 = models.TextField(verbose_name='개요', validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')])
    content2 = models.TextField(verbose_name='기대효과', validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')])
    content3 = models.TextField(verbose_name='진행내역', validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')])
    file_upload = models.FileField(verbose_name='첨부파일', upload_to='files/dtCommunity/', blank=True, validators=[file_size])

    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def filename(self):
        return self.file_upload.name

    def __str__(self):
        return self.title

    class Meta :
        verbose_name_plural = '프로젝트 현황'

