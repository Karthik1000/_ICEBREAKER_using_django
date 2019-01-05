from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile,Temp
from .forms import UserLoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.urls import reverse

from django.utils.encoding import force_bytes,force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#from new_project.tokens import account_activation_token
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.contrib import messages
from datetime import datetime
import random
from django.contrib.auth.models import User
#from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.db.models import Q
###password change
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
#captchafields
import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

####
from startFundraiser.models import Campaign
from startFundraiser.forms import BackersForm
###
from iceBreaker.serializer import ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



def account_activation_sent(request):
    print('-------------in account_activation_sent-------------')
    return render(request, 'register/account_activation_sent.html')

def user_login(request):

    if request.method == 'POST':
        try:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']

                user = authenticate(username=username, password=password)

                if user:
                    if user.is_active:
                        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                        #return redirect('project:post_list')
                        return redirect("http://127.0.0.1:8000/")

                    else:
                        return render(request, 'register/error.html')

                else:
                    return render(request, 'register/error.html')
        except Exception as e:
            print(e)
            return render(request, 'register/error.html')
    else:
        form = UserLoginForm()


    contexts = {'form':form}

    return render(request, 'register/login.html', contexts)

def user_logout(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/")

#fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
def email_verify(form):
    rand_numb = random.randint(100000, 999999)
    b = str(rand_numb)
    email = [form.data['email']]
    response = send_mail("Hello rock77", b, "yagnakarthik100@gmail.com", email)
    return b

def user_register(request):
    if request.method == 'POST':

        #social = request.POST['social']
        #print(type(social),social)

        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            try:
                b = email_verify(form)
                print(b)
            except Exception as e:
                print(e)
            username = form.data['username']
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            email = form.data['email']
            password1 = form.data['password1']
            names = Temp.objects.values_list('temp_user',flat=True)
            if username in names:
                return HttpResponse('this is cannot be used for now ')
            else:
                Temp.objects.create(temp_user=username,otp=b)
            context1 = {
                'username':username,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'password1':password1,
                'b':b,
            }

            #new_user.save()
            #Profile.objects.create(user = new_user)
            return render(request,'register/verify.html', context1)
    else:

        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'register/register.html', context) #

def new_user_reg(request):
    if request.method == 'POST':
        otp1=request.POST['typed_otp']
        otp4=int(otp1)
        username = request.POST['username']
        otp2=Temp.objects.get(temp_user=username).otp
        otp3=int(otp2)
        if otp3 == otp4:
            global num
            num=1
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            new_user = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
            new_user.set_password(request.POST['password1'])
            new_user.save()
            Profile.objects.create(user = new_user)
            login(request,new_user,backend='django.contrib.auth.backends.ModelBackend')
        else:
            return HttpResponse('Please go back check your otp')
    return redirect("http://127.0.0.1:8000/")



@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            user_form = UserEditForm(data=request.POST or None, instance=request.user)
            profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return render(request, "startFundraiser/home.html")
        except Exception as e:
            print(e)

    else:


        pro = request.user
        projects = Campaign.objects.filter(user = pro)

        #else:
        #    project2 = projects
        if Profile.objects.filter(user = pro):
            #Profile.objects.create(user = pro)

            user_form = UserEditForm(instance=request.user)
        #print(request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        else:
            Profile.objects.create(user = pro)
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        #if num < 1:
        #    Profile.objects.create(user = request.user)

        #    num +=1
        #else:
        #    Profile.objects.filter(user = request.user)
        #    profile_form = ProfileEditForm(instance=request.user.profile)
        #print(profile_form)




    return render(request, 'register/edit_profile.html',{'user_form': user_form,'profile_form': profile_form,'projects':projects,})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('register:edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'register/chnage_password.html', {
        'form': form
    })

class profileREST(APIView):
    def get(self,request):
        pro = Profile.objects.all()
        serializer = ProfileSerializer(pro, many = True)
        return Response(serializer.data)
    def put(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
