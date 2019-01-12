import spotipy
from spotipy.oauth2 import SpotifyClientCredentials # weird bugfix
import requests
import io

client = SpotifyClientCredentials(client_id='899ab90bac17478eb78194a4e028804f', client_secret='3963b9b9dd244a188814c61196981a8b')
spotify = spotipy.Spotify(client_credentials_manager=client)

# TODO: Interface Alexa + find which objects to return to make Alexa happy

# ALL FUNCS RETURN DICT WITH FORMAT { 'songname': '30secondmp3url' }

def track_by_name(track):
    results = spotify.search(q=f'track: {track}', type='track', limit=50)['tracks']['items']

    for track in results:
        if track['preview_url']:
            return (track['preview_url'], track['name'])

def tracks_by_artist(artist, limit=50):
    results = spotify.search(q=f'artist: {artist}', type='track', limit=limit)['tracks']['items']

    tracks = {}

    for track in results:
        if track['preview_url']:
            tracks[track['name']] = track['preview_url']

    return tracks

def tracks_by_playlist(playlist, limit=50):
    results = spotify.search(q=f'{playlist}', type='playlist', limit=limit)
    import pprint
    pprint.pprint(results)
    tracks = {}

# song = requests.get(track_by_name('wannabe spice girls'))

# headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

# response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})

# print(response.json())
