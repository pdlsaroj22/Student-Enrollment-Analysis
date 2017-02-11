from django.conf.urls import url
from . import views

app_name = 'Application'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^(?P<id>[0-9]+)/$', views.studentDetail, name='student'),
    url(r'^(?P<id>[0-9]+)/$', views.instructorDetail, name='instructor'),
    url(r'^Student', views.update, name='update'),
    url(r'^Student/updatePassword$', views.updatePassword, name='password'),
    url(r'^logout$', views.logout, name='logout')
    # url(r'^Application/(?P<pk>[0-9]+)/$', views.login, name='login')
]
