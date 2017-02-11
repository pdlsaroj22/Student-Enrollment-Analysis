
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('Application.urls')),
    url(r'^Application/', include('Application.urls')),

]
