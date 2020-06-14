from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "id", "track_id", "name", "artist_id", "artist_name", "album_id", "album_image_url", "album_name", 
            "popularity", "url", "preview_url", "release_date", "played_at", "added_at", "user"
        ]

class TrackListSerializer(serializers.ListSerializer):
    child = TrackSerializer()
