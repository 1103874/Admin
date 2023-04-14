import pandas as pd
from dtapp.models import Type1, Type3, Type2
import os


def create_type1(name):

    Type1.objects.create(
        name=name,
    )

    print(f'Type1: {name}')

def create_type2(type2, name):

    Type2.objects.create(
        type1=Type1.objects.get(name=type2),
        name=name,
    )

    print(f'Type1: {type2}, Type2: {name}')


def create_type3(type1, type3, name):

    Type3.objects.create(

        type2=Type2.objects.get(type1__name=type1,  name=type3),
        name=name,
    )

    print(f'Type2: {type3}, Type3: {name}')





# django project root경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR : ', BASE_DIR)

# 직무 데이터 읽기
df = pd.read_excel(r'C:\Users\user\PycharmProjects\Admin\dtapp\프로세스_가이드_분류.xlsx')

Type1.objects.all().delete()

for itm in df['대분류'].drop_duplicates().tolist() :
    create_type1(itm)
#
Type2.objects.all().delete()

for idx, itm in df[['대분류', '중분류']].drop_duplicates().iterrows() :
    print(itm['대분류'], itm['중분류'])
    create_type2(itm['대분류'], itm['중분류'])

Type3.objects.all().delete()

for idx, itm in df[['대분류','중분류', '소분류']].drop_duplicates().iterrows() :
    print(itm['대분류'], itm['중분류'], itm['소분류'])
    create_type3(itm['대분류'], itm['중분류'], itm['소분류'])
