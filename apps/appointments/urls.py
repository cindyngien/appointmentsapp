from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^login$', views.login, name='login'),
  url(r'^register$', views.register, name='register'),
  url(r'^logoff$', views.logoff, name='logoff'),
  url(r'^appointments$', views.home, name='home'),
  url(r'^create$', views.create, name='create'),
  url(r'^appointments/(?P<app_id>\d+)$', views.edit, name='edit'),
  url(r'^update/(?P<app_id>\d+)$', views.update, name='update'),
  url(r'^delete/(?P<app_id>\d+)$', views.delete, name='delete'),
]
