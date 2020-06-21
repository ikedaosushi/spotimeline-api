from django.urls import include, path
from rest_framework import routers
from .views import ping, TimelineViewSet, FollowCreateAPIView, MeViewSet, CurrentPlayingViewSet, UserListAPIView

urlpatterns = [
    path("ping", ping), 
    path('timeline', TimelineViewSet.as_view()),
    path('me', MeViewSet.as_view()),
    path('me/current', CurrentPlayingViewSet.as_view()),
    path('follow', FollowCreateAPIView.as_view()),
    path('user', UserListAPIView.as_view()),
    path('auth/login/', include('rest_social_auth.urls_token')),
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # # path('auth/', include('djoser.urls.jwt')),
]