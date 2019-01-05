from django.conf.urls import url
from . import views

app_name = 'register'

urlpatterns = [
    #url('post/', views.post_list, name='post_list'),
    #url('', views.user_login, name='user_login'),
    url('login/', views.user_login, name='user_login'),
    url('logout/', views.user_logout, name='user_logout'),
    url('register/', views.user_register, name='user_register'),
    url('new_user_reg/', views.new_user_reg, name='new_user_reg'),
    url('profile/', views.edit_profile, name='edit_profile'),
    url('password/', views.change_password, name='change_password'),
    url('api/', views.profileREST.as_view()),
    #url('social/', views.social, name='social'),
    #url('home/', views.home, name='home'),


]
