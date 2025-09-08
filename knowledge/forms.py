from django import forms
from .models import Process

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['category', 'title', 'slug', 'description', 'steps_md', 'is_published']