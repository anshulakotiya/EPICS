from django import forms

from .models import *


class uploadDocumentForm2(forms.ModelForm):
    class Meta:
        model = Documents
        fields = "__all__"


class uploadDocumentForm(forms.ModelForm):
    class Meta:
        model = UserDecease
        fields = "__all__"
        exclude ={'user'}
        widgets = {
            'description': forms.Textarea(),
        }
