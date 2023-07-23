from spotify_api_tests.utils.helpers import spotify_session
from spotify_api_tests.model.spotify_playlist import SpotifyPlaylist


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

    def add_playlist(self, playlist: SpotifyPlaylist, endpoint, headers, params):
        response = spotify_session.post(
            url=endpoint,
            headers=headers,
            params=params,
            json={
                'name': f'{playlist.name}',
                'description': f'{playlist.description}',
                'public': f'{playlist.public}'
            }
        )
        return response

    def add_track_to_playlist(self, endpoint, headers, params):
        response = spotify_session.post(
            url=endpoint,
            headers=headers,
            params=params,
        )
        return response

    def get_playlist_items(self, endpoint, headers, params):
        return spotify_session.get(endpoint, headers=headers, params=params)

    def remove_track_from_playlist(self, song_id, endpoint, headers, params):
        response = spotify_session.delete(
            url=endpoint,
            headers=headers,
            params=params,
            json={
                'tracks': [
                    {
                        "uri": song_id
                    }
                ]
            }
        )
        return response

    def get_top_items(self, endpoint, headers):
        return spotify_session.get(endpoint, headers=headers)

