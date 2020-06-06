from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import (response, permissions, views, generics, status)
import spotipy

from user_profile.models import Follow
from user_profile.serializer import UserSerializer, FollowSerializer
from timeline.models import Track
from timeline.serializer import TrackListSerializer

from .authentication import CsrfExemptSessionAuthentication

def ping(request):
    return JsonResponse({"message": "pong"})

def auth_ping(request):
    me = request.user
    if not me.is_anonymous: 
        token, created = Token.objects.get_or_create(user=me)
        return JsonResponse({"message": f"pong. you're {me.username}", "token": token.key})
    else:
        return JsonResponse({"message": "pong. you're not authorized"})

class TimelineViewSet(views.APIView, LoginRequiredMixin):
    def get(self, request):
        me = request.user
        queryset = Track.objects.filter(user__in=[follow.following_user for follow in Follow.objects.filter(user=me)])
        serializer = TrackListSerializer(queryset)
        return response.Response(serializer.data, status.HTTP_200_OK)


class MeViewSet(views.APIView, LoginRequiredMixin):
    def get(self, request):
        me = request.user
        access_token = me.social_auth.get(provider='spotify').extra_data['access_token']
        sp = spotipy.Spotify(auth=access_token)
        
        return response.Response(sp.current_user(), status.HTTP_200_OK)

class CurrentPlayingViewSet(views.APIView, LoginRequiredMixin):
    def get(self, request):
        me = request.user
        access_token = me.social_auth.get(provider='spotify').extra_data['access_token']
        sp = spotipy.Spotify(auth=access_token)
        
        return response.Response(sp.currently_playing(), status.HTTP_200_OK)


class FollowCreateAPIView(views.APIView, LoginRequiredMixin):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    def post(self, request, *args, **kwargs):
        me = request.user
        following_user = User.objects.get(username=request.data['username'])
        data = dict(
            user=me.pk, following_user=following_user.pk
        )
        serializer = FollowSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data, status.HTTP_201_CREATED)