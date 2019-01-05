from django.conf.urls import url
from . import views

app_name = 'testimony'

urlpatterns = [
    url(r'home/', views.Home_view, name="home"),
    url(r'profiles/', views.all_profiles, name="profile"),
    url(r'test/', views.Testimony_view, name="testi"),
]
