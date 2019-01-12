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
            return track['preview_url']

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



# -----------------------------------
# ----- TEMP BOT IMPLEMENTATION -----
# -----------------------------------

STATE_NO_QUERY = 0
STATE_MUSIC_CHOICE = 1
STATE_SONG = 2
STATE_ARTIST = 3
STATE_GENRE = 4
STATE_MOOD = 5
STATE_PLAYLIST = 6
STATE_NO_INFO = 7

def on_input(state, user_input, context):
    if user_input == 'quit':
        return STATE_NO_QUERY, {}, 'BYE'
    
    if state == STATE_ARTIST:
        return track_artist_on_enter_state(context)


def track_artist_on_enter_state(context):
    return track_by_name(context)

def artist_on_enter_state(context):
    return 'Which song?'



# def upload(file, channel)
#   options = {
#     token: @team.bot["bot_access_token"],
#     file: File.new("./tmp/composed/#{file.timestamp}", 'rb'),
#     filename: "composed_" + file.name,
#     title: "Composed " + file.title,
#     channels: channel
#   }

#   res = RestClient.post 'https://slack.com/api/files.upload', options
#   json_response = JSON.parse(res.body)

#   # Return the uploaded file's ID
#   thread_ts = json_response["file"]["shares"]["private"][channel]["ts"]
#   file_id = json_response["file"]["id"]
# end

song = requests.get(track_by_name('wannabe spice girls'))

headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})

print(response.json())