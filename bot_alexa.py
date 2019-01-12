import re
import random
from flask import jsonify
import json
import spotify
import requests

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
  elif state == STATE_PLAY:
    return song_play_on_enter_state(context)


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

  elif state == STATE_PLAY:
    return STATE_NO_QUERY, {}, 'Ok! playing music'

  raise NotImplementedError(f"Invalid state for on input {state}")
# START STATE
# The big start state that knows where to send the user.
# ---

def no_query_on_enter_state(context):
  return 'Hi I\'m Eve how can I help? '

def no_query_on_input(user_input, context):
  search = re.search('music', user_input)
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
    "text": "What song do you want? "
    }

def music_choice_on_input(user_input, context):
  song = spotify.track_by_name(user_input)
  return STATE_PLAY, {'song': song} , None

def song_play_on_enter_state(context):
  return {"directives": {

        "type": "AudioPlayer.Play",

        "playBehavior": "REPLACE_ALL",

        "audioItem": {

          "stream": {

            "token": "string",

            "url": context['song'],

            "offsetInMilliseconds": 10

          }

        }

      }}