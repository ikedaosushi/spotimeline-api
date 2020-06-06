from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Track
        fields = [
            "name", "artist_name", "album_name", "popularity", "url", 
            "preview_url", "release_date", "played_at", "added_at", "username",
        ]

class TrackListSerializer(serializers.ListSerializer):
    child = TrackSerializer()
