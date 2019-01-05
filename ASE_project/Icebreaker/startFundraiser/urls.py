from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views
# from startFundraiser.views import CampaignCreateView
from django.urls import path

app_name = 'startFundraiser'




urlpatterns = [
    path('', views.home, name='home'),
     url(r'^start_campaign/$', views.start_campaign, name='start_campaign'),
    path('edit/<int:pk>', views.campaign_edit, name='campaign_edit'),

    path('delete/<int:pk>', views.campaign_delete, name='campaign_delete'),
    url(r'^all_campaigns/$', views.campaigns, name='campaigns'),
    url(r'^campaigns/creative/$', views.creative, name='creative'),
    url(r'^campaigns/social/$', views.social, name='social'),
    url(r'^campaigns/tech/$', views.tech, name='tech'),

    url(r'^campaign/(?P<campaign_id>[0-9]+)/$', views.detail, name='campaign_detail'),
    url(r'^campaign/(?P<pk>\d+)/update/$', views.add_update, name='add_update'),
    url(r'^campaign/(?P<pk>\d+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^campaign/(?P<pk>\d+)/faq/$', views.add_faq, name='add_faq'),
    url(r'^campaign/(?P<pk>\d+)/rewards/$', views.add_rewards, name='campaign_rewards'),
    #url(r'^campaign/(?P<pk>\d+)/claim/$', views.claim_reward, name='claim'),
    url(r'^index/$', views.index, name='index'),
    url(r'^posts/$', views.blog_post, name='blog_post'),
    url(r'^campaign/(?P<pk>\d+)/support/$', views.pay, name='campaign_support'),
    url(r'^checkout/(?P<pk>\d+)/$', views.checkout, name='checkout'),
    url(r'^checkout1/(?P<id>\d+)/$', views.checkout1, name='checkout1'),
    url(r'^like/$', views.like_camp, name='like_camp'),
]
