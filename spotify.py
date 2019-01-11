import spotipy
from spotipy.oauth2 import SpotifyClientCredentials # weird bugfix
import pprint

client = SpotifyClientCredentials(client_id='899ab90bac17478eb78194a4e028804f', client_secret='3963b9b9dd244a188814c61196981a8b')
spotify = spotipy.Spotify(client_credentials_manager=client)

# TODO: Interface Alexa + find which objects to return to make Alexa happy

# ALL FUNCS RETURN SONG NAME AS STRING OR LIST OF STRINGS

def track_by_name(track):
    return spotify.search(q=f'track: {track}', type='track', limit=1)

def tracks_by_artist(artist, limit=5):
    results = spotify.search(q=f'artist: {artist}', type='track', limit=limit)['tracks']['items']

    tracks = []

    for track in results:
        tracks.append(track['name'])

    return tracks

def tracks_by_album(album, limit=5):
    results = spotify.search(q=f'album: {album}', type='track', limit=limit)['tracks']['items']
    
    tracks = []

    for track in results:
        tracks.append(track['name'])

    return tracks