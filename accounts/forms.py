from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserForm(UserCreationForm):        
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name","username", "email", "password1", "password2"]


class CustomUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "profile"]
