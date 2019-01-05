from django import forms
from django.contrib import admin
from . import models

class productform(forms.ModelForm):
    class Meta:
        model = models.product
        fields = ['product_title','product_type','overview','description','image','quantity','cost']
