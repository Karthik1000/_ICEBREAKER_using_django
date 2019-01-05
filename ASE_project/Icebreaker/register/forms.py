from django import forms
from .models import Profile
from django.contrib.auth.models import User
#from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
#NOCAPTCHA
from captcha.fields import ReCaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs = {'placeholder':'username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs = {'placeholder':'password'}))

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required='required',widget=forms.TextInput(attrs = {'placeholder':'UserName','size':50,'style': 'font-size:large'}))
    first_name = forms.CharField(max_length=50, required='required' ,widget=forms.TextInput(attrs = {'placeholder':'First Name','size':50,'style': 'font-size:large'}))
    last_name = forms.CharField(max_length=50, required='required' ,widget=forms.TextInput(attrs = {'placeholder':'Last Name','size':50,'style': 'font-size:large'}))
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs = {'placeholder':'Email','size':50,'style': 'font-size:large'}))
    password1 = forms.CharField(max_length=50,required='required',widget=forms.PasswordInput(attrs = {'placeholder':'password','size':50,'style': 'font-size:large'}))
    password2 = forms.CharField(max_length=50,required='required', widget=forms.PasswordInput(attrs = {'placeholder':'Confirm password','size':50,'style': 'font-size:large'}))
    #captcha = ReCaptchaField(public_key='6LcfkX8UAAAAAKXo5Bw7MtTvDn4Gqb6SDJ_R-qVk',private_key='6LcfkX8UAAAAAJ8R-2yR5V5Jx7jSCsCjCaeKTvWH',)
    captcha = ReCaptchaField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email = email).exclude(username = username).exists():
            raise forms.ValidationError(u'Email Already Registered')
        return email
    """
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password did not match')
        return confirm_password

class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ProfileEditForm(forms.ModelForm):
    #photo = forms.ImageField(upload_to='images/',null=True, blank=True)

    #github_link = forms.URLField(max_length=200,null=True,widget=forms.TextInput(attrs = {'placeholder':'UserName','size':50}))
    #facebook_link = forms.URLField(max_length=200,null=True,widget=forms.TextInput(attrs = {'placeholder':'UserName','size':50}))
    #linkedIn_link = forms.URLField(max_length=200,null=True,widget=forms.TextInput(attrs = {'placeholder':'UserName','size':50}))
    class Meta:
        model = Profile
        exclude =('user',)
