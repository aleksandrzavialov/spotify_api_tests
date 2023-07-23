import logging

import requests
from spotify_api_tests.utils.helpers import spotify_session


class SpotifyWithSession:
    def __init__(self):
        self.spotify_session = spotify_session

    def get_user_info(self, endpoint, headers):
        return spotify_session.get(endpoint, headers=headers)

    def follow_artist(self, endpoint, headers, params):
        response = spotify_session.put(
            url=endpoint,
            headers=headers,
            params=params)
        return response

    def get_followed_artists(self, endpoint, headers, params):
        return spotify_session.get(endpoint, headers=headers, params=params)

    def unfollow_artist(self, endpoint, headers, params):
        response = spotify_session.delete(
            url=endpoint,
            headers=headers,
            params=params)
        return response

    def add_track(self, endpoint, headers, params):
        response = spotify_session.put(
            url=endpoint,
            headers=headers,
            params=params)
        return response

    def get_favorite_tracks(self, endpoint, headers):
        return spotify_session.get(endpoint, headers=headers)

    def remove_track(self, endpoint, headers, params):
        response = spotify_session.delete(
            url=endpoint,
            headers=headers,
            params=params)
        return response