from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls')),
    path('api/v1/', include('apiv1.urls')),
]