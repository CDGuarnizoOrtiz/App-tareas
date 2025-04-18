from django import forms
from .models import tasks

class tasksform(forms.ModelForm):
    class Meta:
        model = tasks
        fields = ['title','description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        