from django import forms
from .models import UploadedFile

class FileUploadForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=True, label="Custom Message")

    class Meta:
        model = UploadedFile
        fields = ['file', 'message']
