from django import forms


class FormDeleteUser(forms.Form):
    user_name = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
