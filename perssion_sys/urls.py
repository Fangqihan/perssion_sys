
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^return_goods/', views.return_goods),
    url(r'^add_goods/', views.add_goods),
    url(r'^del_goods/', views.del_goods),
    url(r'^exchange/', views.exchange),
]
