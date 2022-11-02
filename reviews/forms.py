from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'grade', 'image']
        labels = {
            'title': '제목',
            'content': '내용',
            'grade': '평점',
            'image': '사진',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            "review",
            "user",
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