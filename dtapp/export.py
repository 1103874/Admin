import pandas as pd
from django.http import HttpResponse

from dtapp.models import CeiTreeList, ProcessGuideList


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


## Process & Guide Excel Export
def export_processGuide(request):
    processGuide_data = ProcessGuideList.objects.values("type2__name", "team", "type1__name", "type3__name", "type4", "title", "content2", "content", "author__first_name", "dt_created")
    processGuide_df = pd.DataFrame(list(processGuide_data))

    # Convert date/time columns to datetime64[ns] and remove timezone information
    processGuide_df = processGuide_df[['type2__name', 'team', 'type1__name', 'type3__name', 'type4', 'title', 'content2', 'content', 'author__first_name', 'dt_created']]
    processGuide_df['dt_created'] = processGuide_df['dt_created'].astype('datetime64[ns]').dt.tz_localize(None).dt.strftime('%Y-%m-%d')

    processGuide_df.columns= ['지원담당', '주관부서', '구분', '분류', '세부분류', '제목', '내용', '정립기준', '담당자', '등록일']

    processGuide_df.insert(0, 'No', range(1, 1 + len(processGuide_df)))

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Guide&Process.xlsx"'
    processGuide_df.to_excel(response, index=False)
    return response