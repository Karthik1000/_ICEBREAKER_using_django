from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import GroupTable, MemberTable, CommentTable, UpdateTable
import requests
import json
from datetime import datetime

from iceBreaker.serializer import CommunitySerializer,MemberSerializer,CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status






@login_required(login_url="/register/login/")
def view_community(request):
    if request.method == 'POST':

        title = request.POST['title']
        address = request.POST['address']
        if address == '' and title != '':
            info = GroupTable.objects.filter(title__icontains=title)
        elif address != '' and title == '':
            info = GroupTable.objects.filter(address__icontains=address)
        elif address != '' and title != '':
            info = GroupTable.objects.filter(address__icontains=address, title__icontains=title)
        else:
            info = GroupTable.objects.all()
        c = info.count()
        return render(request, 'community/view-community.html', {'info':info, 'c':c})
    else:
        info = GroupTable.objects.all()
        c = info.count()

        return render(request, 'community/view-community.html', {'info':info, 'c':c})

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def make_group(request):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        lat = request.POST['lat']
        lon = request.POST['lon']
        date = request.POST['date']
        address = request.POST['address']


        s = GroupTable(title=title, date=date, lat=lat, lon=lon,type=type, number=0, founder=request.user, address=address)
        s.save()
        return HttpResponseRedirect('/community/my-group/')


    else:
        return render(request, 'community/make-group.html', {})



@login_required(login_url="/register/login/")
def my_group(request):
    if request.method == 'POST':
        content = GroupTable.objects.filter(founder=request.user)
        count = content.count()
        usr = request.user
        if 'checks[]' in request.POST:

            checks = request.POST.getlist('checks[]')
            for c in checks:
                c1 = int(c)
                GroupTable.objects.filter(pk=c1).delete()

                return render(request, 'community/my-group.html', {'content': content, 'usr': usr, 'count':count})

        else:

            return render(request, 'community/my-group.html', {'content': content, 'usr': usr, 'count':count})

    else:
        content=GroupTable.objects.filter(founder=request.user)
        count = content.count()
        usr = request.user
        return render(request, 'community/my-group.html', {'content':content, 'usr':usr,'count':count})


@login_required(login_url="/register/login/")
def joined_group(request):
    content = MemberTable.objects.filter(
        user=request.user
    ).only("group")
    return render(request, 'community/joined-group.html', {'content':content})

@login_required(login_url="/register/login/")
def profile_list(request):
    if request.method == 'POST':
        search = request.POST['search']
        search2 = request.POST['search2']
        if search2=='' and search!='':
            users = User.objects.filter(username__icontains=search)
        elif search2!='' and search=='':
            users = User.objects.filter(email__icontains=search2)
        elif search2 != '' and search != '':
            users = User.objects.filter(email__icontains=search2, username__icontains=search)
        else:
            users = User.objects.all()
        c = users.count()
        return render(request, 'community/all-profiles.html', {'users':users,'c':c,})

    else:
        users = User.objects.all()
        c = users.count()
        return render(request, 'community/all-profiles.html', {'users':users, 'c':c,})


@login_required(login_url="/register/login/")
def update_detail(request, u_id):

    group1 = GroupTable.objects.filter(pk=u_id)
    if group1.count() == 0:
        return render(request, 'community/nopage.html', {})
    #group = GroupTable.objects.get(pk=u_id)
    group = group1[0]
    if group.founder!= request.user:
        return render(request, 'community/nopage.html', {})

    content = UpdateTable.objects.filter(group=group)
    c = content.count()

    if request.method == 'POST':
        update = request.POST['update']
        if update=='':
            pass
            #return render(request, 'community/update-detail.html', {'content': content, 'group': group, 'c': c})
        else:
            u = UpdateTable(update=update, group=group)
            u.save()

            # message = "the group "+group.title+" has an update: "+update
            # users = MemberTable.objects.filter(group=group)
            #
            # #send email
            # for i in users:
            #     email = i.user.email
            #




            content = UpdateTable.objects.filter(group=group)
    else:

        return render(request, 'community/update-detail.html', {'content':content, 'group':group, 'c':c})
    return render(request, 'community/update-detail.html', {'content': content, 'group': group, 'c': c})


@login_required(login_url="/register/login/")
def group_detail(request, g_id):
    conten = GroupTable.objects.filter(pk=g_id)
    if conten.count() == 0:
        return render(request, 'community/nopage.html', {})
    group = conten[0]
    comments = CommentTable.objects.filter(group=group)
    updates = UpdateTable.objects.filter(group=group).reverse()

    # weather
    lat = group.lat
    lon = group.lon
    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&units=imperial&appid=313a98b055ed12b5f1319c0c2199951a'
    r = requests.get(url)
    data = json.loads(r.text)


    temp= str(data['main']['temp'])
    description= str(data['weather'][0]['description'])
    icon = data['weather'][0]['icon']



    if request.method == 'POST':
        #comment
        if 'choice' in request.POST:
            choice = request.POST['choice']
            if choice == "yes":
                joined =MemberTable.objects.filter(user=request.user, group=group)
                if joined.count()==0:  #not joined
                    join = MemberTable(user=request.user, group=group)
                    join.save()     #joined
                    group.number = group.number+1
                    group.save()
                    return render(request, 'community/group-detail.html', {'group':group, 'updates':updates, 'message':'you have joined', 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})
                else:
                    return render(request, 'community/group-detail.html', {'group':group, 'updates':updates, 'message':'you have already joined', 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})
            else:

                joined =MemberTable.objects.filter(user=request.user, group=group)
                if joined.count()>0:
                    joined.delete()
                    group.number = group.number-1
                    group.save()
                    return render(request, 'community/group-detail.html', {'group':group, 'updates':updates, 'message':'you are out of the group', 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})
                else:
                    return render(request, 'community/group-detail.html', {'group':group, 'updates':updates, 'message':'you never joined the group', 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})
        else:
            #group = GroupTable.objects.get(pk=g_id)
            #comments = CommentTable.objects.filter(group=group)


            comment = request.POST['comment']
            if comment != "":
                c = CommentTable(group=group, comment=comment, user=request.user)
                c.save()
            return render(request, 'community/group-detail.html',
                          {'group':group, 'message': 'you need to select 1 option', 'updates':updates, 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})



    else:
        #print(content.count())


        return render(request, 'community/group-detail.html', {'group':group, 'updates':updates, 'comments':comments, 'temp':temp, 'description':description, 'icon':icon})



@login_required(login_url="/register/login/")
def group_edit(request, g_id):
    if request.method == 'POST':
        title = request.POST['title']
        type = request.POST['type']
        lat = request.POST['lat']
        lon = request.POST['lon']
        date = request.POST['date']
        address = request.POST['address']
        #if title=="" || type==""

        s = GroupTable.objects.get(pk=g_id)
        s.title=title
        s.type=type
        s.lat=lat
        s.lon=lon
        s.date=date
        s.address=address
        #s = GroupTable(title=title, date=date, lat=lat, lon=lon,type=type, number=0, founder=request.user, address=address)
        s.save()
        return HttpResponseRedirect('/community/group-detail/'+g_id+'/')


    else:
        c=GroupTable.objects.filter(pk=g_id)
        if c.count()==0:
            return render(request, 'community/nopage.html', {})

        else:
            content= GroupTable.objects.get(pk=g_id)
            if content.founder==request.user:
                return render(request, 'community/group-edit.html', {'content':content})
            else:
                return render(request, 'community/nopage.html', {})

@login_required(login_url="/register/login/")
def profile_detail(request, u_id):
    #no need for filter and
    usr = User.objects.filter(pk=u_id)
    if usr.count()==0:
        return render(request, 'community/nopage.html', {})
    usr = User.objects.get(pk=u_id)
    if usr == request.user:
        return redirect('community:my_group')

    content = GroupTable.objects.filter(founder=usr)

    return render(request, 'community/profile.html', {'content':content, 'usr':usr})


class communityREST(APIView):
    def get(self,request):
        pro = GroupTable.objects.all()
        serializer = CommunitySerializer(pro, many = True)
        return Response(serializer.data)
    def put(self,request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class communityMemberREST(APIView):
    def get(self,request):
        pro = MemberTable.objects.all()
        serializer = MemberSerializer(pro, many = True)
        return Response(serializer.data)
    def put(self,request):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class communitycommentREST(APIView):
    def get(self,request):
        pro = CommentTable.objects.all()
        serializer = CommentSerializer(pro, many = True)
        return Response(serializer.data)
    def put(self,request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
