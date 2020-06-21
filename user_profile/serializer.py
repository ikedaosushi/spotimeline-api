from datetime import datetime, timedelta

from social_django.utils import load_strategy
from django.contrib.auth.models import User
from rest_framework import serializers
import spotipy

from .models import Follow

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_display_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'user_display_name']

    def get_user_display_name(self, user):
        social = user.social_auth.get(provider='spotify')
        sp = self._get_spotipy(social)
        return str(sp.current_user())

    def _get_spotipy(self, social):
        expired_time = datetime.fromtimestamp(social.extra_data['auth_time']) + timedelta(minutes=30)
        if expired_time < datetime.now():
            social.refresh_token(load_strategy())

        access_token = social.get_access_token(load_strategy())
        sp = spotipy.Spotify(auth=access_token)
        return sp

class UserListSerializer(serializers.ListSerializer):
    child = UserSerializer()

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"