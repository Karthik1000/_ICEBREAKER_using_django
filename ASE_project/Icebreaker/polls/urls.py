from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'polls'
urlpatterns = [



    path('polls/<int:qid>/', views.detail, name='detail'),

    path('query/', views.query_view, name='query_view'),

    path('adminpage/', views.adminpage, name='adminpage'),

    path('sendmail/', views.sendmail, name='sendmail'),

    path('login/', auth_views.LoginView.as_view(template_name='polls/ibadmin.html'), name='admin'),

    #path('result/',views.result,name='result'),

   # path('sendmail/', views.sendmail, name='sendmail'),



]