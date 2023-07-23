import allure
from spotify_api_tests.app import spotify_user
from allure_commons.types import Severity
from spotify_api_tests.utils.helpers import load_json_schema
from spotify_api_tests.model.spotify import SpotifyWithSession
from jsonschema import validate
from spotify_api_tests.data.artists import ArtistList
from spotify_api_tests.model.spotify_playlist import SpotifyPlaylist
from spotify_api_tests.data.tracks import TrackList
from datetime import datetime

USER_INFO_ENDPOINT = '/v1/me'
FOLLOW_ARTIST_ENDPOINT = '/v1/me/following'
TRACK_ENDPOINT = '/v1/me/tracks'
PLAYLIST_ENDPOINT = f'/v1/users/{spotify_user.id}/playlists'
TOP_ARTISTS_ENDPOINT = '/v1/me/top/artists'


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('User Info')
@allure.severity(Severity.MINOR)
@allure.title('User can get its info')
def test_user_info_received(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Get user information'):
        user_info_response = spotify_session.get_user_info(USER_INFO_ENDPOINT, headers=obtain_user_token)

        assert user_info_response.status_code == 200
        assert user_info_response.json()['display_name'] == spotify_user.name
        assert user_info_response.json()['email'] == spotify_user.email
        assert user_info_response.json()['id'] == spotify_user.id


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('Following artists')
@allure.severity(Severity.NORMAL)
@allure.title('User can follow and unfollow artists')
def test_user_follows_artists(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Follow Lou Reed'):
        user_params = {
            "type": "artist",
            "ids": ArtistList.Lou_Reed.value[1]
        }
        follow_artist_response = spotify_session.follow_artist(FOLLOW_ARTIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        assert follow_artist_response.status_code == 204
    with allure.step('Check that a user follows Lou Reed'):
        user_params = {
            "type": "artist",
        }
        followed_artists_response = spotify_session.get_followed_artists(FOLLOW_ARTIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=followed_artists_response.json(), schema=load_json_schema('get_followed_artists.json'))
        assert followed_artists_response.status_code == 200
        assert followed_artists_response.json()['artists']['items'][0]['name'] == ArtistList.Lou_Reed.value[0]
    with allure.step('Unfollow Lou Reed'):
        user_params = {
            "type": "artist",
            "ids": ArtistList.Lou_Reed.value[1]
        }
        follow_artist_response = spotify_session.unfollow_artist(FOLLOW_ARTIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        assert follow_artist_response.status_code == 204
    with allure.step('Check that a user no longer follows Lou Reed'):
        user_params = {
            "type": "artist",
        }
        followed_artists_response = spotify_session.get_followed_artists(FOLLOW_ARTIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=followed_artists_response.json(), schema=load_json_schema('get_no_followed_artists.json'))
        assert followed_artists_response.status_code == 200
        assert len(followed_artists_response.json()['artists']['items']) == 0


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('Adding tracks')
@allure.severity(Severity.CRITICAL)
@allure.title('User can add and remove tracks from collection')
def test_user_adds_tracks_to_favorites(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Add Master of Puppets'):
        user_params = {
            "ids": TrackList.Master_of_Puppets.value[1]
        }
        add_track_response = spotify_session.add_track(TRACK_ENDPOINT, headers=obtain_user_token, params=user_params)
        assert add_track_response.status_code == 200
    with allure.step('Check that a user has favorite track added'):
        favorite_response_add = spotify_session.get_favorite_tracks(TRACK_ENDPOINT, headers=obtain_user_token)

        validate(instance=favorite_response_add.json(), schema=load_json_schema('get_favorite_tracks.json'))
        assert favorite_response_add.status_code == 200
        assert favorite_response_add.json()['items'][0]['track']['id'] == TrackList.Master_of_Puppets.value[1]
        assert favorite_response_add.json()['items'][0]['track']['name'] == TrackList.Master_of_Puppets.value[0]
    with allure.step('Remove favorite track'):
        user_params = {
            "ids": TrackList.Master_of_Puppets.value[1]
        }
        remove_track_response = spotify_session.remove_track(TRACK_ENDPOINT, headers=obtain_user_token, params=user_params)

        assert remove_track_response.status_code == 200
    with allure.step('Check that a user has no favorite tracks'):
        favorite_response_remove = spotify_session.get_favorite_tracks(TRACK_ENDPOINT, headers=obtain_user_token)

        validate(instance=favorite_response_remove.json(), schema=load_json_schema('get_no_favorite_tracks.json'))
        assert favorite_response_remove.status_code == 200
        assert len(favorite_response_remove.json()['items']) == 0


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('Adding tracks to a playlist and deleting from playlist')
@allure.severity(Severity.BLOCKER)
@allure.title('User can add tracks from playlist')
def test_user_adds_tracks(obtain_user_token):
    spotify_session = SpotifyWithSession()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y%H:%M:%S")
    playlist = SpotifyPlaylist(f'test_playlist_name-{dt_string}', 'test_playlist_description')
    song_id = f'spotify:track:{TrackList.Master_of_Puppets.value[1]}'

    with allure.step('Add new playlist'):
        user_params = {
            "user_id": spotify_user.id
        }
        add_playlist_response = spotify_session.add_playlist(playlist, PLAYLIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=add_playlist_response.json(), schema=load_json_schema('post_create_playlist.json'))
        assert add_playlist_response.json()['name'] == playlist.name
        assert add_playlist_response.json()['description'] == playlist.description
        assert add_playlist_response.json()['public'] == playlist.public
        assert add_playlist_response.status_code == 201

        playlist_id = add_playlist_response.json()['id']
        TRACK_PLAYLIST_ENDPOINT = f'/v1/playlists/{playlist_id}/tracks'

    with allure.step('Check that a user can add tracks to a playlist'):
        user_params = {
            "playlist_id": playlist_id,
            "uris": f'spotify:track:{TrackList.Master_of_Puppets.value[1]}'
        }
        add_to_playlist_response = spotify_session.add_track_to_playlist(TRACK_PLAYLIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=add_to_playlist_response.json(), schema=load_json_schema('post_add_track_to_playlist.json'))
        assert add_to_playlist_response.status_code == 201
    with allure.step('Check that a track appears in the playlist'):
        user_params = {
            "playlist_id": playlist_id,
        }
        get_tracks_in_playlist_response = spotify_session.get_playlist_items(TRACK_PLAYLIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=get_tracks_in_playlist_response.json(), schema=load_json_schema('get_tracks_in_playlist.json'))
        assert get_tracks_in_playlist_response.status_code == 200
        assert get_tracks_in_playlist_response.json()['total'] == 1
        assert get_tracks_in_playlist_response.json()['items'][0]['track']['id'] == TrackList.Master_of_Puppets.value[1]
        assert get_tracks_in_playlist_response.json()['items'][0]['track']['name'] == TrackList.Master_of_Puppets.value[0]
    with allure.step('Check that a user can delete tracks from a playlist'):
        user_params = {
            "playlist_id": playlist_id,
        }

        remove_from_playlist_response = spotify_session.remove_track_from_playlist(song_id, TRACK_PLAYLIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=remove_from_playlist_response.json(), schema=load_json_schema('post_delete_track_from_playlist.json'))
        assert remove_from_playlist_response.status_code == 200

        get_tracks_in_playlist_response = spotify_session.get_playlist_items(TRACK_PLAYLIST_ENDPOINT, headers=obtain_user_token, params=user_params)

        validate(instance=get_tracks_in_playlist_response.json(), schema=load_json_schema('get_no_tracks_in_playlist.json'))
        assert get_tracks_in_playlist_response.status_code == 200
        assert get_tracks_in_playlist_response.json()['total'] == 0


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('User can get list of its top artists')
@allure.severity(Severity.MINOR)
@allure.title('User can get list of its top artists with appropriate permission')
def test_user_can_see_top_artists(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Check list of top artists'):
        get_top_items_response = spotify_session.get_top_items(TOP_ARTISTS_ENDPOINT, headers=obtain_user_token)

        validate(instance=get_top_items_response.json(), schema=load_json_schema('get_top_artists.json'))
        assert get_top_items_response.status_code == 200






