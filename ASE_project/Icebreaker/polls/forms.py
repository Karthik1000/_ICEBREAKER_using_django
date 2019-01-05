from django import forms
from .models import *


class Queryform(forms.ModelForm):
    class Meta:
        model = Question
        fields = [

            'question_text', 'name', 'email'
        ]
