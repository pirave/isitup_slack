from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^isitup/$', views.check_isitup),
    url(r'^ttc/$', views.check_ttc),
]
