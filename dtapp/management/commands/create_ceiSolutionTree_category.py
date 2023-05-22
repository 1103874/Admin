import pandas as pd
from dtapp.models import Group, Type
import os


def create_group(name):

    Group.objects.create(
        name=name,
    )

    print(f'구분: {name}')

def create_type(group, name):

    Type.objects.create(
        work_group=Group.objects.get(name=group),
        name=name,
    )

    print(f'구분: {group}, 세부구분: {name}')



# django project root경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR : ', BASE_DIR)

# 직무 데이터 읽기
df = pd.read_excel(r'C:\Users\user\PycharmProjects\Admin\dtapp\management\commands\CEI_Solution_Tree_분류.xlsx')

Group.objects.all().delete()
for itm in df['구분'].drop_duplicates().tolist() :
    create_group(itm)


Type.objects.all().delete()
for idx, itm in df[['구분', '세부구분']].drop_duplicates().iterrows() :
    create_type(itm['구분'], itm['세부구분'])

