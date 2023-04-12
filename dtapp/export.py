import pandas as pd
from django.http import HttpResponse

from dtapp.models import CeiTreeList, CeiTreeBMList

## CEI Tree Excel Export
def export_cei_tree(request):
    cei_tree_data = CeiTreeList.objects.values("title", "region", "dt_start", "dt_end", "cell", "content1", "work_group_id__name", "work_type_id__name", "target_cei_before", "target_cei_after", "cei_hdv_before", "cei_hdv_after", "cei_data_before", "cei_data_after", "ber_hdv_before", "ber_hdv_after", "ber_data_before", "ber_data_after", "baduser_hdv_before", "baduser_hdv_after", "baduser_data_before", "baduser_data_after", "bm_status", "dt_created")
    cei_tree_df = pd.DataFrame(list(cei_tree_data))
    cei_tree_df = cei_tree_df[['title', 'region', 'dt_start', 'dt_end', 'cell', 'content1', 'work_group_id__name', 'work_type_id__name', "target_cei_before", "target_cei_after", 'cei_hdv_before', 'cei_hdv_after', 'cei_data_before', 'cei_data_after', 'ber_hdv_before', 'ber_hdv_after', 'ber_data_before', 'ber_data_after', 'baduser_hdv_before', 'baduser_hdv_after', 'baduser_data_before', 'baduser_data_after', 'bm_status', 'dt_created']]

    # Convert date/time columns to datetime64[ns] and remove timezone information
    cei_tree_df['dt_created'] = cei_tree_df['dt_created'].astype('datetime64[ns]').dt.tz_localize(None).dt.strftime('%Y-%m-%d')

    # Add cei_gap and ber_gap columns
    cei_tree_df['cei_hdv_gap'] = cei_tree_df['cei_hdv_after'] - cei_tree_df['cei_hdv_before']
    cei_tree_df['cei_data_gap'] = cei_tree_df['cei_data_after'] - cei_tree_df['cei_data_before']
    cei_tree_df['ber_hdv_gap'] = cei_tree_df['ber_hdv_after'] - cei_tree_df['ber_hdv_before']
    cei_tree_df['ber_data_gap'] = cei_tree_df['ber_data_after'] - cei_tree_df['ber_data_before']
    cei_tree_df['baduser_hdv_gap'] = cei_tree_df['baduser_hdv_after'] - cei_tree_df['baduser_hdv_before']
    cei_tree_df['baduser_data_gap'] = cei_tree_df['baduser_data_after'] - cei_tree_df['baduser_data_before']
    cei_tree_df['target_cei_gap'] = cei_tree_df['target_cei_after'] - cei_tree_df['target_cei_before']

    cei_tree_df = cei_tree_df[['title', 'region', 'dt_start', 'dt_end', 'cell', 'content1', 'work_group_id__name', 'work_type_id__name', 'target_cei_before', 'target_cei_after', 'target_cei_gap', 'cei_hdv_before', 'cei_hdv_after', 'cei_hdv_gap', 'cei_data_before', 'cei_data_after', 'cei_data_gap', 'ber_hdv_before', 'ber_hdv_after', 'ber_hdv_gap', 'ber_data_before', 'ber_data_after', 'ber_data_gap', 'baduser_hdv_before', 'baduser_hdv_after', 'baduser_hdv_gap', 'baduser_data_before', 'baduser_data_after', 'baduser_data_gap', 'bm_status', 'dt_created']]

    cei_tree_df.columns= ['사례명', '담당', '시작일', '종료일', 'cell 수량', '내용', '구분', '세부구분', 'target_cei_before', 'target_cei_after', 'target_cei_gap', 'cei_hdv_before', 'cei_hdv_after', 'cei_hdv_gap', 'cei_data_before', 'cei_data_after', 'cei_data_gap', 'ber_hdv_before', 'ber_hdv_after', 'ber_hdv_gap', 'ber_data_before', 'ber_data_after', 'ber_data_gap', 'baduser_hdv_before', 'baduser_hdv_after', 'baduser_hdv_gap', 'baduser_data_before', 'baduser_data_after', 'baduser_data_gap', 'bm_status', '작성일']

    cei_tree_df.insert(0, 'No', range(1, 1 + len(cei_tree_df)))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="cei_tree.xlsx"'
    cei_tree_df.to_excel(response, index=False)
    return response

def export_cei_tree_BM(request):
    cei_tree_data = CeiTreeBMList.objects.values("title_id__title", "title_id__work_group_id__name", "title_id__work_type_id__name", "region", "author_id__username", "dt_start", "dt_end", "cell", "title2", "content1", "cei_before", "cei_after", "ber_before", "ber_after")
    cei_tree_df = pd.DataFrame(list(cei_tree_data))
    cei_tree_df = cei_tree_df[['title_id__title', 'title_id__work_group_id__name', 'title_id__work_type_id__name', 'region', "author_id__username", 'dt_start', 'dt_end', 'cell', 'title2', 'content1', 'cei_before', 'cei_after', 'ber_before', 'ber_after']]

    # Add cei_gap and ber_gap columns
    cei_tree_df['cei_gap'] = cei_tree_df['cei_after'] - cei_tree_df['cei_before']
    cei_tree_df['ber_gap'] = cei_tree_df['ber_after'] - cei_tree_df['ber_before']

    # 추가된 cei_gap, ber_gap 컬럼을 포함하여 df 순서 재구성
    cei_tree_df = cei_tree_df[['title_id__title', 'title_id__work_group_id__name', 'title_id__work_type_id__name', 'region', "author_id__username", 'dt_start', 'dt_end', 'cell', 'title2', 'content1', 'cei_before', 'cei_after', "cei_gap", 'ber_before', 'ber_after', "ber_gap"]]

    # 컬럼명 변경
    cei_tree_df.columns= ['B/M 사례', '구분', '세부구분', '담당', '담당자', '시작일', '종료일', 'cell 수량', '제목', '내용', 'cei_before', 'cei_after', 'cei_gap', 'ber_before', 'ber_after', 'ber_gap']
    # 첫 컬럼에 No 추가
    cei_tree_df.insert(0, 'No', range(1, 1 + len(cei_tree_df)))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="cei_tree_BM.xlsx"'
    cei_tree_df.to_excel(response, index=False)
    return response