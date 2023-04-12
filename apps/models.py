from django.db import models

# Create your models here.

class regionType(models.Model):
    region_name = models.CharField(max_length=10, verbose_name='담당 구분')
    def __str__(self):
        return self.region_name
    class Meta :
        verbose_name_plural = '담당 구분(목록 생성)'