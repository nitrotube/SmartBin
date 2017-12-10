from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    file_name = forms.CharField(max_length=50)
    class Meta:
        model = Image
        fields = ['image']


