from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "user_name",
            "first_name",
            "last_name",
            "profile_img",
            "bio",
        )


class CustomUserChangeForm(UserChangeForm, forms.Form):

    class Meta:
        model = CustomUser
        fields = (
            "user_name",
            "first_name",
            "last_name",
            "email",
            "profile_img",
            "bio",
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields["password"]
