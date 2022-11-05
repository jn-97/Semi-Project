from django import forms
from .models import Restaurant, Comment

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant

        fields = ['sorted','region','name','introduce','number','address', 'runtime', 'closing', 'image1', 'image2', 'image3', 'image4', 'image5']
        labels = {
            'sorted' : '한식, 중식, 양식, 일식',
            'region' : '지역',
            'name': '매장이름',
            'introduce': '매장소개',
            'number': '전화번호',
            'address': '주소',
            'runtime': '영업시간',
            'closing': '휴무일',
            'image1': '사진1',
            'image2': '사진2',
            'image3': '사진3',
            'image4': '사진4',
            'image5': '사진5',
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
        labels = {
            'grade': '평점',
            'content': '댓글',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs = {
            "placeholder": "댓글을 작성해 주세요",
        }
        self.fields["content"].help_text = None