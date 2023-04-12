from django import forms

from .models import projectPost

## Project App
class projectForm(forms.ModelForm):
    class Meta:
        model = projectPost
        fields = [
            "type",
            "status",
            "dt_start",
            "dt_end",
            "title",
            "content1",
            "content2",
            "content3",
            "file_upload",
        ]
        widgets = {
            'type': forms.RadioSelect,
            'status': forms.RadioSelect,
            'dt_start' : forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'dt_end' : forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '과제명을 입력하세요.'}),
            'content1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 3}),
            'content2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 3}),
            'content3': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요.', 'rows': 3}),
        }
