from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from apps.models import regionType
from apps.validators import file_size
from auth_SKO.models import User


# Create your models here.


## start SRreveiw App
class SRreview(models.Model):
    TYPE_CHOICES = [
        ('대표이사 BP', "대표이사 BP"),
        ('기술지원담당 BP', "기술지원담당 BP"),
        ('운용지원담당 BP', "운용지원담당 BP"),
        ('경영지원담당 BP', "경영지원담당 BP"),
    ]
    type = models.CharField(max_length=10, verbose_name='구분', choices=TYPE_CHOICES, default='대표이사 BP')

    REGION_CHOICES = [
        ('안전보건', "안전보건"),
        ('Access', "Access"),
        ('AOC', "AOC"),
        ('Biz. 지원', "Biz. 지원"),
        ('Infra설비', "Infra설비"),
        ('SO', "SO"),
        ('전송', "전송"),
        ('기획운영', "기획운영"),
        ('기업문화', "기업문화"),
        ('수도권자산운영', "수도권자산운영"),
        ('지역자산운영', "지역자산운영"),
        ('강남Access', "강남Access"),
        ('강북Access', "강북Access"),
        ('인천Access', "인천Access"),
        ('경기Access', "경기Access"),
        ('경남Access', "경남Access"),
        ('경북Access', "경북Access"),
        ('전남Access', "전남Access"),
        ('전북Access', "전북Access"),
        ('충남Access', "충남Access"),
        ('충북Access', "충북Access"),
        ('강원Access', "강원Access"),
    ]
    region1 = models.CharField(max_length=20, blank=True, verbose_name='담당1', choices=REGION_CHOICES)
    team1 = models.CharField(max_length=20, blank=False, verbose_name='팀1')
    name1 = models.CharField(max_length=20, blank=False, verbose_name='이름1')
    region2 = models.CharField(max_length=20, blank=True, verbose_name='담당2', choices=REGION_CHOICES)
    team2 = models.CharField(max_length=20, blank=True, verbose_name='팀2')
    name2 = models.CharField(max_length=20, blank=True, verbose_name='이름2')
    region3 = models.CharField(max_length=20, blank=True, verbose_name='담당3', choices=REGION_CHOICES)
    team3 = models.CharField(max_length=20, blank=True, verbose_name='팀3')
    name3 = models.CharField(max_length=20, blank=True, verbose_name='이름3')

    dt = models.CharField(max_length=20, verbose_name='날짜')
    title = models.CharField(max_length=100, unique=True, verbose_name='사례명',
                             error_messages={'unique': '이미 존재하는 제목입니다.'})
    description = models.TextField(validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')], verbose_name='내용 및 추진성과')
    file_upload = models.FileField(verbose_name='첨부파일(문서)', upload_to='files/dtapp/SRreview', blank=True,
                                   validators=[file_size])
    image_upload = models.ImageField(verbose_name='첨부파일(이미지)', upload_to='files/dtapp/SRreview/image', blank=True,
                                     validators=[file_size])
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'BP 사례현황'


## end SRreveiw App


## start CEItree App
class Group(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'CEItree 목록(구분)'

    def __str__(self):
        return self.name


class Type(models.Model):
    work_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = 'CEItree 목록(세부구분)'

    def __str__(self):
        return self.name


class CeiTreeList(models.Model):
    work_group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='구분')
    work_type = models.ForeignKey(Type, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='세부구분')

    NETWORK_TYPE_CHOICES = [
        ('4G', "4G"),
        ('5G', "5G"),
        ('종합', "종합"),
    ]
    network = models.CharField(max_length=20, verbose_name='망 구분', choices=NETWORK_TYPE_CHOICES, default='4G')

    TYPE_CHOICES = [
        ('강남Access', "강남Access"),
        ('강북Access', "강북Access"),
        ('인천Access', "인천Access"),
        ('경기Access', "경기Access"),
        ('경남Access', "경남Access"),
        ('경북Access', "경북Access"),
        ('전남Access', "전남Access"),
        ('전북Access', "전북Access"),
        ('충남Access', "충남Access"),
        ('충북Access', "충북Access"),
        ('강원Access', "강원Access"),
        ('수도권Access관제팀', "수도권Access관제팀"),
        ('동부Access관제팀', "동부Access관제팀"),
        ('서부Access관제팀', "서부Access관제팀"),
        ('충청Access관제팀', "충청Access관제팀"),
        ('강원Access관제팀', "강원Access관제팀"),
        ('SO', "SO"),
    ]
    region = models.CharField(max_length=20, verbose_name='담당', choices=TYPE_CHOICES)

    dt_start = models.DateField(verbose_name='시작일')
    dt_end = models.DateField(verbose_name='종료일')
    cell = models.IntegerField(verbose_name='적용 Cell 수', validators=[MinValueValidator(1), MaxValueValidator(10000000)])
    title = models.CharField(max_length=100, unique=True, verbose_name='사례명',
                             error_messages={'unique': '이미 존재하는 제목입니다.'})
    content1 = models.TextField(validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')], verbose_name='내용')
    cei_hdv_before = models.DecimalField(verbose_name='HDV CEI(전)', blank=True, null=True, max_digits=5,
                                         decimal_places=2)
    # validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    cei_hdv_after = models.DecimalField(verbose_name='HDV CEI(후)', blank=True, null=True, max_digits=5,
                                        decimal_places=2)
    # validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    cei_data_before = models.DecimalField(verbose_name='Data CEI(전)', blank=True, null=True, max_digits=5,
                                          decimal_places=2)
    # validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    cei_data_after = models.DecimalField(verbose_name='Data CEI(후)', blank=True, null=True, max_digits=5,
                                         decimal_places=2)
    # validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    ber_hdv_before = models.DecimalField(verbose_name='HDV BER(전)', blank=True, null=True, max_digits=5,
                                         decimal_places=2)
    # validators=[MinValueValidator(0), MaxValueValidator(100)])
    ber_hdv_after = models.DecimalField(verbose_name='HDV BER(후)', blank=True, null=True, max_digits=5,
                                        decimal_places=2)
    # validators=[MinValueValidator(0), MaxValueValidator(100)])
    ber_data_before = models.DecimalField(verbose_name='Data BER(전)', blank=True, null=True, max_digits=5,
                                          decimal_places=2)
    # validators=[MinValueValidator(0), MaxValueValidator(100)])
    ber_data_after = models.DecimalField(verbose_name='Data BER(후)', blank=True, null=True, max_digits=5,
                                         decimal_places=2)
    # validators=[MinValueValidator(0), MaxValueValidator(100)])
    baduser_hdv_before = models.IntegerField(verbose_name='HDV Bad User(전)', blank=True, null=True)
    baduser_hdv_after = models.IntegerField(verbose_name='HDV Bad User(후)', blank=True, null=True)
    baduser_data_before = models.IntegerField(verbose_name='Data Bad User(전)', blank=True, null=True)
    baduser_data_after = models.IntegerField(verbose_name='Data Bad User(후)', blank=True, null=True)
    target_cei_before = models.DecimalField(verbose_name='목표 CEI(전)', max_digits=5, decimal_places=2,
                                            validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    target_cei_after = models.DecimalField(verbose_name='목표 CEI(후)', max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(44.44), MaxValueValidator(100)])

    TYPE_CHOICES2 = [
        ('X', "X"),
        ('O', "O"),
    ]
    bm_status = models.CharField(max_length=20, verbose_name='BM 적용여부', choices=TYPE_CHOICES2, default='X')

    file_upload = models.FileField(verbose_name='첨부파일(문서)', upload_to='files/dtapp/CEItree', blank=True,
                                   validators=[file_size])
    image_upload = models.ImageField(verbose_name='첨부파일(이미지)', upload_to='files/dtapp/CEItree/image', blank=True,
                                     validators=[file_size])
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'CEItree 사례현황'


class CeiTreeBMList(models.Model):
    title = models.ForeignKey(CeiTreeList, on_delete=models.SET_NULL, blank=True,
                              null=True, verbose_name='B/M 사례명')
    TYPE_CHOICES = [
        ('강남Access', "강남Access"),
        ('강북Access', "강북Access"),
        ('인천Access', "인천Access"),
        ('경기Access', "경기Access"),
        ('경남Access', "경남Access"),
        ('경북Access', "경북Access"),
        ('전남Access', "전남Access"),
        ('전북Access', "전북Access"),
        ('충남Access', "충남Access"),
        ('충북Access', "충북Access"),
        ('강원Access', "강원Access"),
        ('수도권Access관제팀', "수도권Access관제팀"),
        ('동부Access관제팀', "동부Access관제팀"),
        ('서부Access관제팀', "서부Access관제팀"),
        ('충청Access관제팀', "충청Access관제팀"),
        ('강원Access관제팀', "강원Access관제팀"),
        ('SO', "SO"),
    ]
    region = models.CharField(max_length=20, verbose_name='담당', choices=TYPE_CHOICES)

    dt_start = models.DateField(verbose_name='시작일')
    dt_end = models.DateField(verbose_name='종료일')
    cell = models.IntegerField(verbose_name='적용 Cell 수')
    title2 = models.CharField(max_length=100, verbose_name='제목')
    content1 = models.TextField(validators=[MinLengthValidator(10, '10글자 이상 작성해주세요.')], verbose_name='내용')
    cei_before = models.DecimalField(verbose_name='CEI(전)', max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    cei_after = models.DecimalField(verbose_name='CEI(후)', max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(44.44), MaxValueValidator(100)])
    ber_before = models.DecimalField(verbose_name='BER(전)', max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    ber_after = models.DecimalField(verbose_name='BER(후)', max_digits=5, decimal_places=2,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    file_upload = models.FileField(verbose_name='첨부파일(문서)', upload_to='files/dtapp/CEItree', blank=True,
                                   validators=[file_size])
    image_upload = models.ImageField(verbose_name='첨부파일(이미지)', upload_to='files/dtapp/CEItree/image', blank=True,
                                     validators=[file_size])
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title.title

    class Meta:
        verbose_name_plural = 'CEItree(B/M) 사례현황'
## end CEItree App







## start 전사 Process & Guied App
class Type1(models.Model):
    name = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'Process&Guied 목록(대분류)'
    def __str__(self):
        return self.name

class Type2(models.Model):
    type1 = models.ForeignKey(Type1, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'Process&Guied 목록(중분류)'
    def __str__(self):
        return self.name
class Type3(models.Model):
    type2 = models.ForeignKey(Type2, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'Process&Guied 목록(소분류)'
    def __str__(self):
        return self.name

class ProcessGuideList(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # REGION_TYPE_CHOICES = [
    #     ('기술지원', "기술지원"),
    #     ('운용지원', "운용지원"),
    # ]
    # region_type = models.CharField(max_length=10, verbose_name='지원담당', choices=REGION_TYPE_CHOICES, default='기술지원')

    type1 = models.ForeignKey(Type1, on_delete=models.CASCADE, verbose_name='대분류')
    type2 = models.ForeignKey(Type2, on_delete=models.CASCADE, verbose_name='중분류')
    type3 = models.ForeignKey(Type3, on_delete=models.CASCADE, verbose_name='소분류')
    type4 = models.CharField(max_length=40, verbose_name='세부분류')

    team = models.CharField(max_length=20, verbose_name='주관부서')
    title = models.CharField(max_length=100, unique=True, verbose_name='제목',
                             error_messages={'unique': '이미 존재하는 제목입니다.'})
    content = models.TextField(verbose_name='정립 기준')

    dt_start = models.DateField(verbose_name='유효기간(시작)')
    dt_end = models.DateField(verbose_name='유효기간(종료)', default='9999-12-31')

    file_upload = models.FileField(verbose_name='첨부파일(문서)', upload_to='files/dtapp/ProcessGuide', blank=True,
                                   validators=[file_size])

    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name_plural = 'Process&Guied 현황'

## end 전사 Process & Guied App

