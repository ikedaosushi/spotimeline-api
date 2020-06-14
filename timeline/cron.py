import logging
import spotipy
from datetime import datetime, timedelta
from social_django.utils import load_strategy
from django_cron import CronJobBase, Schedule
from timeline.models import Track
from datetime import datetime
from django.contrib.auth.models import User

class FetchTracks(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'track.fetch_tracks'

    def do(self):
        logging.info("start")
        try:
            self._run()
        except Exception as e:
            logging.error(f"Error occur {e}")
        logging.info("finish")

    def _run(self):
        for user in User.objects.all():
            try:
                self._run_by_user(user)
            except Exception as e:
                logging.error(f"Error occur on user: {user.name} {e}")

    def _run_by_user(self, user):
        if user.social_auth.exists():
            social = user.social_auth.get(provider='spotify')
            sp = self._get_spotipy(social)
            if Track.objects.filter(user=user).exists():
                latest = Track.objects.filter(user=user).order_by('-played_at')[0]
                tracks = sp.current_user_recently_played(after=int(latest.played_at.timestamp() * 1000))['items']
            else:
                tracks = sp.current_user_recently_played()['items']
            self._insert_tracks(tracks, user)

    def _get_spotipy(self, social):
        expired_time = datetime.fromtimestamp(social.extra_data['auth_time']) + timedelta(minutes=30)
        if expired_time < datetime.now():
            social.refresh_token(load_strategy())

        access_token = social.get_access_token(load_strategy())
        sp = spotipy.Spotify(auth=access_token)
        return sp

    def _insert_tracks(self, tracks, user):
        for track_dic in tracks[::-1]:
            track = Track(
                track_id=track_dic['track']['id'],
                name=track_dic['track']['name'], 
                artist_id=track_dic['track']['artists'][0]['id'],
                artist_name=track_dic['track']['artists'][0]['name'],
                album_id=track_dic['track']['album']['id'],
                album_name=track_dic['track']['album']['name'],
                album_image_url=track_dic['track']['album']['images'][0]['url'],
                popularity=track_dic['track']['popularity'],
                url=track_dic['track']['href'],
                preview_url=track_dic['track']['preview_url'],
                release_date=track_dic['track']['album']['release_date'],
                played_at=track_dic['played_at'],
                user=user
            )
            track.save()