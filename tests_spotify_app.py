import allure
from spotify_api_tests.app import spotify_user
from allure_commons.types import Severity
from spotify_api_tests.utils.helpers import load_json_schema
from spotify_api_tests.model.spotify import SpotifyWithSession
from jsonschema import validate
from spotify_api_tests.data.artists import ArtistList
from spotify_api_tests.data.tracks import TrackList

USER_INFO_ENDPOINT = '/v1/me'
FOLLOW_ARTIST_ENDPOINT = '/v1/me/following'
TRACK_ENDPOINT = '/v1/me/tracks'


@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('User Info')
@allure.severity(Severity.MINOR)
@allure.title('User can get its info')
def test_user_info_received(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Get user information'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token,
            "Content-Type": "application/json"
        }
        user_info_response = spotify_session.get_user_info(USER_INFO_ENDPOINT, headers=user_headers)

    with allure.step('Validate JSON schema'):
        validate(instance=user_info_response.json(), schema=load_json_schema('get_user_info.json'))

    with allure.step('Check content in answer'):
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
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token

        }
        user_params = {
            "type": "artist",
            "ids": ArtistList.Lou_Reed.value[1]
        }
        follow_artist_response = spotify_session.follow_artist(FOLLOW_ARTIST_ENDPOINT, headers=user_headers, params=user_params)
        assert follow_artist_response.status_code == 204
    with allure.step('Check that a user follows Lou Reed'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token
        }
        user_params = {
            "type": "artist",
        }
        followed_artists_response = spotify_session.get_followed_artists(FOLLOW_ARTIST_ENDPOINT, headers=user_headers, params=user_params)
        validate(instance=followed_artists_response.json(), schema=load_json_schema('get_followed_artists.json'))
        assert followed_artists_response.status_code == 200
        assert followed_artists_response.json()['artists']['items'][0]['name'] == ArtistList.Lou_Reed.value[0]
    with allure.step('Unfollow Lou Reed'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token

        }
        user_params = {
            "type": "artist",
            "ids": ArtistList.Lou_Reed.value[1]
        }
        follow_artist_response = spotify_session.unfollow_artist(FOLLOW_ARTIST_ENDPOINT, headers=user_headers, params=user_params)
        assert follow_artist_response.status_code == 204
    with allure.step('Check that a user no longer follows Lou Reed'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token
        }
        user_params = {
            "type": "artist",
        }
        followed_artists_response = spotify_session.get_followed_artists(FOLLOW_ARTIST_ENDPOINT, headers=user_headers, params=user_params)
        validate(instance=followed_artists_response.json(), schema=load_json_schema('get_no_followed_artists.json'))
        assert followed_artists_response.status_code == 200
        assert len(followed_artists_response.json()['artists']['items']) == 0

@allure.tag("API")
@allure.label('owner', 'azavialov')
@allure.feature('API')
@allure.story('Adding tracks')
@allure.severity(Severity.CRITICAL)
@allure.title('User can add and remove tracks from collection')
def test_user_adds_tracks(obtain_user_token):
    spotify_session = SpotifyWithSession()

    with allure.step('Add Master of Puppets'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token,
            "Content-Type": "application/json"
        }
        user_params = {
            "ids": TrackList.Master_of_Puppets.value[1]
        }
        add_track_response = spotify_session.add_track(TRACK_ENDPOINT, headers=user_headers, params=user_params)
        assert add_track_response.status_code == 200
    with allure.step('Check that a user has favorite track added'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token
        }
        favorite_response = spotify_session.get_favorite_tracks(TRACK_ENDPOINT, headers=user_headers)
        assert favorite_response.status_code == 200
        validate(instance=favorite_response.json(), schema=load_json_schema('get_favorite_tracks.json'))
        assert favorite_response.json()['items'][0]['track']['id'] == TrackList.Master_of_Puppets.value[1]
        assert favorite_response.json()['items'][0]['track']['name'] == TrackList.Master_of_Puppets.value[0]
    with allure.step('Remove favorite track'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token,
            "Content-Type": "application/json"
        }
        user_params = {
            "ids": TrackList.Master_of_Puppets.value[1]
        }
        add_track_response = spotify_session.remove_track(TRACK_ENDPOINT, headers=user_headers, params=user_params)
        assert add_track_response.status_code == 200
    with allure.step('Check that a user has no favorite tracks'):
        user_headers = {
            "Authorization": "Bearer " + obtain_user_token
        }
        favorite_response = spotify_session.get_favorite_tracks(TRACK_ENDPOINT, headers=user_headers)
        assert favorite_response.status_code == 200
        validate(instance=favorite_response.json(), schema=load_json_schema('get_no_favorite_tracks.json'))
        assert len(favorite_response.json()['items']) == 0



