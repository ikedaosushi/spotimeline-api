from urllib.parse import urlencode
import string
import random
import base64

import requests

from django.shortcuts import redirect
from django.conf import settings
from django.http.response import JsonResponse

# SPOTIFY_API_BASE_URL = "https://api.spotify.com"
# API_VERSION = "v1"
# SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

SPOTIFY_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_API_TOKEN_URL = "https://accounts.spotify.com/api/token"

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def index(request):
    print(request.user)
    return JsonResponse(dict(hello="world"))


def login(request):
    scope = "user-read-private user-read-email user-read-currently-playing"
    state = randomString(16)
    request.session['sp_auth_state'] = state

    payload = dict(
        response_type="code",
        client_id=settings.SPOTIFY_CLIENT_ID,
        scope=scope,
        redirect_uri=settings.SPOTIFY_REDIRECT_URL,
        state=state
    )
    redirect_url = f"{SPOTIFY_AUTHORIZE_URL}?{urlencode(payload)}"
    return redirect(redirect_url)


def callback(request):
    params = request.GET

    code = params.get('code')
    state = params.get('state')
    stored_state = request.session.get('sp_auth_state')

    if state != stored_state:
        raise Exception("Not match state")

    payload = dict(
        code=code,
        redirect_uri=settings.SPOTIFY_REDIRECT_URL,
        grant_type='authorization_code',
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    res = requests.post(SPOTIFY_API_TOKEN_URL, data=payload).json()
    return JsonResponse(res)

    # access_token = res["access_token"]
    # refresh_token = res["refresh_token"]
    # token_type = res["token_type"]
    # expires_in = res["expires_in"]

    # authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    # profile_data = requests.get(user_profile_api_endpoint, headers=authorization_header).json()

    # # Get user playlist data
    # playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    # playlist_data = requests.get(playlist_api_endpoint, headers=authorization_header).json()

    # # Combine profile and playlist data to display
    # display_arr = [profile_data] + playlist_data["items"]
