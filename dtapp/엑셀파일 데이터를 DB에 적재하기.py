import pandas as pd
from dtapp.models import Type3
# from auth_ons.models import User

df = pd.read_excel(r"C:\Users\user\PycharmProjects\Admin\dtapp\프로세스_가이드_분류.xlsx",
                   sheet_name='Sheet1', skiprows=1)

for idx, itm in df.iterrows():
    # print(f"{itm['수여자']} SR" )

    Type3.objects.create(
        region=itm['담당'],
        team=itm['팀'],
        dt=itm['월'],
        type=f"{itm['수여자']} SR",
        title=itm['내용'],
        description=itm['세부내용'],
        # author=User.objects.filter(first_name='성기범').get()
    )