from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('', include('api.urls')),
]
