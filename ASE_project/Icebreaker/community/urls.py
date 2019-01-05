from .views import view_community, make_group, my_group, group_detail, group_edit, joined_group, profile_detail, update_detail, profile_list,communityREST,communityMemberREST,communitycommentREST
from django.conf.urls import url

app_name='community'
urlpatterns = [
    url(r'^view-groups/$', view_community, name='view_group'),        #done
    url(r'^make-group/$', make_group, name='make_group'),        #done
    url(r'^my-group/$', my_group, name='my_group'),        #done
    url(r'^joined-group/$', joined_group, name='joined_group'),  # done
    url(r'^all-profiles/$', profile_list, name='profile_list'),

    url(r'^group-detail/(?P<g_id>[0-9]+)/$', group_detail, name='group_detail'),  # done
    url(r'^group-detail/(?P<g_id>[0-9]+)/edit/$', group_edit, name='group_edit'),  # done
    url(r'^profile/(?P<u_id>[0-9]+)/$', profile_detail, name='profile_detail'),  # done
    url(r'^(?P<u_id>[0-9]+)/updates/$', update_detail, name='update_detail'),  #

    #url(r'^page-not-found/$', page_not_found),  # done
    url('capi/', communityREST.as_view()),
    url('capim/', communityMemberREST.as_view()),

]
