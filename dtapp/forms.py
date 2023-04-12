from django import forms
from .models import SRreview, CeiTreeList, CeiTreeBMList, Type, ProcessGuideList, Type2, Type3


## SRreview App
class SRreviewForm(forms.ModelForm):
    class Meta:
        model = SRreview
        fields = ['type', 'region1', 'team1', 'name1', 'region2', 'team2', 'name2', 'region3', 'team3', 'name3', 'dt',
                  'title', 'description', 'image_upload', 'file_upload']
        widgets = {
            'type': forms.RadioSelect(attrs={'class': ''}),
            'region1': forms.Select(attrs={'class': 'form-control', 'placeholder': '공적(1순위)'}),
            'team1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(1순위)'}),
            'name1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(1순위)'}),
            'region2': forms.Select(attrs={'class': 'form-control', 'placeholder': '공적(2순위)'}),
            'team2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(2순위)'}),
            'name2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(2순위)'}),
            'region3': forms.Select(attrs={'class': 'form-control', 'placeholder': '공적(3순위)'}),
            'team3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(3순위)'}),
            'name3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '공적(3순위)'}),
            'dt': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}, format='%Y-%m'),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 5}),
        }


## CEItree App
class ceiTreeListForm(forms.ModelForm):
    class Meta:
        model = CeiTreeList
        fields = ['network', 'work_group', 'work_type', 'region', 'dt_start', 'dt_end', 'cell', 'title', 'content1',
                  'cei_hdv_before', 'cei_hdv_after', 'cei_data_before', 'cei_data_after',
                  'ber_hdv_before', 'ber_hdv_after', 'ber_data_before', 'ber_data_after',
                  'baduser_hdv_before', 'baduser_hdv_after', 'baduser_data_before', 'baduser_data_after',
                  'target_cei_before', 'target_cei_after',
                  'bm_status', 'image_upload', 'file_upload']
        widgets = {
            'network': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-size': '6'}),
            'work_group': forms.Select(attrs={'class': 'form-control'}),
            'work_type': forms.Select(attrs={'class': 'form-control'}),
            'dt_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dt_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cell': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'content1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 5}),
            'cei_hdv_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'cei_hdv_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'cei_data_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'cei_data_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_hdv_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_hdv_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_data_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_data_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'baduser_hdv_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'baduser_hdv_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'baduser_data_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'baduser_data_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_cei_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_cei_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'bm_status': forms.Select(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['work_type'].queryset = Type.objects.none()

            if 'work_group' in self.data:
                try:
                    work_group_id = int(self.data.get('work_group'))
                    self.fields['work_type'].queryset = Type.objects.filter(work_group_id=work_group_id).order_by(
                        'name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty Type queryset


class ceiTreeBMListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ceiTreeBMListForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True

    class Meta:
        model = CeiTreeBMList
        fields = ['region', 'dt_start', 'dt_end', 'cell', 'title', 'title2', 'content1', 'cei_before', 'cei_after',
                  'ber_before', 'ber_after', 'image_upload', 'file_upload']
        widgets = {
            'region': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-size': '6'}),
            'dt_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dt_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cell': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-size': '6'}),
            'title2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'content1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 5}),
            'cei_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'cei_after': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'ber_after': forms.NumberInput(attrs={'class': 'form-control'}),

        }



## 전사 Process & Guide App
class ProcessGuideListForm(forms.ModelForm):
    class Meta:
        model = ProcessGuideList
        fields = ['team', 'type1', 'type2', 'type3', 'type4', 'title', 'content', 'dt_start', 'dt_end',
                  'file_upload']
        widgets = {
            # 'region_type': forms.RadioSelect(attrs={'class': ''}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '팀명을 입력하세요.'}),
            'type1': forms.Select(attrs={'class': 'form-control'}),
            'type2': forms.Select(attrs={'class': 'form-control'}),
            'type3': forms.Select(attrs={'class': 'form-control'}),
            'type4': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요.'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'ex) 00년 0월 SKO ORTM 회의체, 00년 0월 SKT AAR 등', 'rows': 2}),

            'dt_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dt_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['type2'].queryset = Type2.objects.none()
            self.fields['type3'].queryset = Type3.objects.none()

            if 'type1' in self.data:
                try:
                    type1_id = int(self.data.get('type1'))
                    self.fields['type2'].queryset = Type2.objects.filter(type1_id=type1_id).order_by('name')
                except (ValueError, TypeError):
                    pass

            if 'type2' in self.data:
                try:
                    type2_id = int(self.data.get('type2'))
                    self.fields['type3'].queryset = Type3.objects.filter(type2_id=type2_id).order_by('name')
                except (ValueError, TypeError):
                    pass
