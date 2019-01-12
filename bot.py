import re
import random
from flask import jsonify
import json
import spotify
import requests
from spotify import track_by_name

# STATES:
# None
# Artist
# Song
# Playlist
# Mood

# ---
# REGISTER THE STATES
# Connects our states (eg. 'LOCKED OUT') with our functions (eg. locked_out_on_enter_state)
# ---

STATE_NO_QUERY = 0
STATE_MUSIC_CHOICE = 1
STATE_SONG = 2
STATE_ARTIST = 3
STATE_GENRE = 4
STATE_MOOD = 5
STATE_PLAYLIST = 6
STATE_NO_INFO = 7
STATE_PARTY_TYPE = 8
STATE_PLAY = 9

# What to do when we enter a state
def on_enter_state(state, context):
  if state == STATE_NO_QUERY:
    return no_query_on_enter_state(context)

  # start of music bot
  elif state == STATE_MUSIC_CHOICE:
    return music_choice_on_enter_state(context)
  elif state == STATE_PLAYLIST:
    return playlist_on_enter_state(context) 
  elif state == STATE_ARTIST:
    return artist_on_enter_state(context)
  elif state == STATE_GENRE:
    return genre_on_enter_state(context)
  elif state == STATE_SONG:
    return song_on_enter_state(context)
  elif state == STATE_NO_INFO:
    return IDK_on_enter_state(context)
  elif state == STATE_PARTY_TYPE:
    return party_type_on_enter_state(context)
  # More states here
  # elif state == ...
  raise NotImplementedError(f"Invalid state for on enter {state}")

# What to do when we receive input while in a state
def on_input(state, user_input, context):
  # First up, if they're trying to quit, then quit.
  if user_input == 'quit':
    return STATE_NO_QUERY, {}, 'Bye! \n'

  # Otherwise, check the state.
  if state == STATE_NO_QUERY:
    return no_query_on_input(user_input, context)
  
  #start of music bot
  elif state == STATE_MUSIC_CHOICE:
    return music_choice_on_input(user_input, context)
  elif state == STATE_PLAYLIST:
    return playlist_on_input(user_input, context)
  elif state == STATE_ARTIST:
    return artist_on_input(user_input, context)
  elif state == STATE_GENRE:
    return genre_on_input(user_input, context)
  elif state == STATE_SONG:
    return song_on_input(user_input, context)
  elif state == STATE_NO_INFO:
    return IDK_on_input(user_input, context)
  elif state == STATE_PARTY_TYPE:
    return party_type_on_input(user_input, context)


  raise NotImplementedError(f"Invalid state for on input {state}")
# START STATE
# The big start state that knows where to send the user.
# ---

def no_query_on_enter_state(context):
  return 'Hi I\'m Eve how can I help? '

def no_query_on_input(user_input, context):
  search = re.search('music', user_input, re.I)
  if search:
    return STATE_MUSIC_CHOICE, {}, None


  # If we didn't match any regex, go back to this start state and try again.
  else:
    return STATE_NO_QUERY, {}, 'Sorry, I don\'t understand!'


# ------------
# OTHER STATES
# ------------




# --- More states go here! --- #

def music_choice_on_enter_state(context):
  return {
    "text": "How do you want to choose your music? ",
    "slack_params": {
      "response_type": "in_channel",
      "attachments": [
        {
            "callback_id": "Choice",
            "text": "What music",
            "actions": [
                {
                    "name": "Choice", "text": "Playlist", "type": "button", "value": "playlist"
                },{
                    "name": "Choice", "text": "Artist", "type": "button", "value": "artist"
                },{
                    "name": "Choice", "text": "Song", "type": "button", "value": "song"
                },{
                    "name": "Choice", "text": "Genre", "type": "button",  "value": "genre"
                },{
                    "name": "Choice", "text": "I'm not sure", "type": "button", "value": "IDK"
                },
            ]
          }
      ]
    },


#alexa version to be edited??
  "alexa_params": {
    
    }
}

def music_choice_on_input(user_input, context):
  music = user_input
  if music == 'playlist':
    state = STATE_PLAYLIST
  elif music == 'artist':
    state = STATE_ARTIST
  elif music == 'song':
    state = STATE_SONG
  elif music == 'genre':
    state = STATE_GENRE
  elif music == 'IDK':
    state = STATE_NO_INFO
  return state, {'music': music}, None

def playlist_on_enter_state(context):
  return {'text' : "please type a playlist",
          'slack_params': {}
  }
def artist_on_enter_state(context):
  return {'text':"please type an artist",
          'slack_params': {}
  }
def song_on_enter_state(context):
  return {'text':"please type a song",
          'slack_params': {}
  }
def genre_on_enter_state(context):
  return {'text':"please type a genre",
          'slack_params': {}
  }
def IDK_on_enter_state(context):
  return {
    "text": "What type of party? ",
    "slack_params": {"response_type": "in_channel",
      "attachments": [
          {
              "callback_id": "party_select",
              "text": "Select Party",
              "fallback": "You didn’t select a party :(.",
              "actions": [
                  {
                      "name": "party",
                      "type": "select",
                      "options": [
                              {'text' : 'Dinner Party', 'value' : 'dinner'}, 
                              {'text': 'Birthday Party', 'value' : 'birthday'}, 
                              {'text' : 'Pool Party', "value": 'pool'}, 
                              {'text' : 'Dance Party', 'value' : 'dance'}, 
                              {'text': 'House Party', 'value': 'house'}
                              ]
                  }
              ]
          }
      ]
    }
}





def playlist_on_input(user_input, context):
  song = requests.get(track_by_name('wannabe spice girls'))

  headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

  response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})
  return STATE_NO_QUERY, {} , 'Playing \'Wannabe\' by Spice Girls as you asked...\n'

def artist_on_input(user_input, context):
  song = requests.get(track_by_name('wannabe spice girls'))

  headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

  response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})
  return STATE_NO_QUERY, {} , 'Playing \'Wannabe\' by Spice Girls as you asked...\n'

def song_on_input(user_input, context):
  song = requests.get(track_by_name(user_input))

  headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

  response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})
  return STATE_NO_QUERY, {} , 'Playing...\n'

def genre_on_input(user_input, context):
  song = requests.get(track_by_name('wannabe spice girls'))

  headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

  response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})
  return STATE_NO_QUERY, {} , 'Playing \'Wannabe\' by Spice Girls as you asked...\n'

def IDK_on_input(user_input, context):
  song = requests.get(track_by_name('wannabe spice girls'))

  headers = {'Authorization': 'Bearer xoxb-498969795956-521435106288-iXazpPMO1WCj08WEoWVwCAHH'}

  response = requests.post('https://api.slack.com/api/files.upload', files={'file': song.content}, headers=headers, data={'channels': '#general', 'filetype': 'mp3'})
  return STATE_NO_QUERY, {} , 'Playing \'Wannabe\' by Spice Girls as you asked...'


def party_type_on_enter_state(context):
  party_type = context["party_type"]
  return f"please select: _buttons coming soon!_"

def party_type_on_input(user_input, context):
  return STATE_NO_QUERY, {}, "thanks for selecting"
