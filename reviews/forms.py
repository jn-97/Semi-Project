from django import forms
from .models import Restaurant, Comment

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['sorted', 'name', 'runtime', 'closing', 'image']
        labels = {
            'sorted' : '분류',
            'name': '매장이름',
            'runtime': '영업시간',
            'closing': '휴무일',
            'image': '사진'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["closing"].widget.attrs = {
            "placeholder": "예시 : 정기휴무-매주(일)",
        }
        self.fields["closing"].help_text = None
        
        self.fields["runtime"].widget.attrs = {
            "placeholder": "예시 : 08:00 ~ 21:30",
        }
        self.fields["runtime"].help_text = None
    


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            "restaurant",
            "user"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs = {
            "placeholder": "댓글을 작성해 주세요",
        }
        self.fields["content"].help_text = None