from django import forms
from .models import Testimony
from django.contrib.auth.models import User


class TestimonyForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required='required',widget=forms.TextInput(attrs = {'placeholder':'Name','size':50,'style': 'font-size:large'}))
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    to_name = forms.CharField(max_length=30, required='required',widget=forms.TextInput(attrs = {'placeholder':'To_Name','size':50,'style': 'font-size:large'}))
    commented = forms.CharField(max_length=30, required='required', help_text='Optional.',widget=forms.TextInput(attrs = {'placeholder':'Comments','size':50,'style': 'font-size:large'}))
    #profile_pic = forms.ImageField()

    class Meta:
        model = Testimony
        fields = ('name', 'to_name','commented')
