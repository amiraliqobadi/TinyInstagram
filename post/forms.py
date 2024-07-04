from django import forms
from .models import Post
from multiupload.fields import MultiFileField


class UploadForm(forms.ModelForm):
    images = MultiFileField(min_num=1, max_num=5, required=True)

    class Meta:
        model = Post
        fields = [
            "description",
        ]
