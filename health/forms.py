from django import forms
from .models import *

class uploadDocumentForm(forms.ModelForm):
    class Meta:
        model = userDocuments
        fields = "__all__"