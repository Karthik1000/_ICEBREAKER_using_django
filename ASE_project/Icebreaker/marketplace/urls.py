from django.urls import path
from django.conf.urls import url
from . import views

app_name='marketplace'

urlpatterns = [
    url(r'^blog/$',views.products_all, name="products_blog"),
    url(r'^(?P<slug>[0-9]+)/$', views.product_details, name="product_details"),
    url(r'^my_products/$', views.my_products, name="my_products"),
    url(r'^add/$',views.add_product, name="add_product"),
    url(r'edit_product/(?P<id>\d+)/$', views.edit_product, name="edit_product"),
    url(r'del_product/(?P<id>\d+)/$', views.delete_product, name="delete_product"),
    url(r'^test/$',views.test, name="test"), #basic template
    url(r'add_to_cart/(?P<id>\d+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'add_quantity/(?P<id>\d+)/$', views.add_quantity, name="add_quantity"),
    url(r'remove_quantity/(?P<id>\d+)/$', views.remove_quantity, name="remove_quantity"),
    url(r'del_quantity/(?P<id>\d+)/$', views.delete, name="del_quantity"),
    url(r'checkout/$', views.checkout, name="checkout"),
    #url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction, name='update_records'),
    url(r'add_tocart/$', views.add_tocart, name="add_tocart"),
]
