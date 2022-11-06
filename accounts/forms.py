from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserForm(UserCreationForm):        
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name","last_name", "email", "password1", "password2"]


class CustomUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["last_name", "first_name", "email", "contact","address","city","country","about_me","profile"]
        labels = {
            "profile": "프로필",
            "contact": "연락처",
            "address": "주소",
            "city": "도시",
            "country": "국가",
            "about_me": "자기소개",
        }
