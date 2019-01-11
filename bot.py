import re
import random
from flask import jsonify

# STATES:
# None
# Artist
# Song
# Playlist
# Mood

TUTORS = ['d', 'f'] #need to have tutors are still later used
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
STATE_NO_INFO = 6

# What to do when we enter a state
def on_enter_state(state, context):
  if state == "NO QUERY":
    return no_query_on_enter_state(context)
  elif state == "LOCKED OUT":
    return locked_out_on_enter_state(context)
  elif state == 'LOCKED OUT LOCATION':
    return locked_out_location_on_enter_state(context)
  
  # start of music bot
  elif state == "STATE_MUSIC_CHOICE":
    return music_choice_on_enter_state(context)
  
  # More states here
  # elif state == ...

# What to do when we receive input while in a state
def on_input(state, user_input, context):
  # First up, if they're trying to quit, then quit.
  if user_input == 'quit':
    return 'NO QUERY', {}, 'Bye!'

  # Otherwise, check the state.
  if state == 'NO QUERY':
    return no_query_on_input(user_input, context)
  elif state == 'LOCKED OUT':
    return locked_out_on_input(user_input, context)
  elif state == 'LOCKED OUT LOCATION':
    return locked_out_location_on_input(user_input, context)
  
  #start of music bot
  elif state == "STATE_MUSIC_CHOICE":
    return music_choice_on_input(user_input, context)

# ---
# START STATE
# The big start state that knows where to send the user.
# ---

def no_query_on_enter_state(context):
  return 'Hi I\'m Eve how can I help? '

def no_query_on_input(user_input, context):
  # Check where they're locked out.
  match = re.search('music', user_input)
  if match:
    return 'STATE_MUSIC_CHOICE', {}, None

  match = re.match('I am locked out( in(?P<location>.*))?', user_input)
  if match:
    location = match.group('location')
    if location:
      return 'LOCKED OUT LOCATION', {'location': location}, None
    else:
      return 'LOCKED OUT', {}, None

  # If we didn't match any regex, go back to this start state and try again.
  else:
    return 'NO QUERY', {}, 'Sorry, I don\'t understand!'


# ---
# OTHER STATES
# ---

# TODO: Replace these states with your project's cool states

# LOCKED OUT state
def locked_out_on_enter_state(context):
  return 'Where are you locked out?'

def locked_out_on_input(user_input, context):
  # Store the full response text as the location.
  location = user_input
  return 'LOCKED OUT LOCATION', {'location': location}, None


# LOCKED OUT LOCATION state
def locked_out_location_on_enter_state(context):
  location = context['location']
  tutor = random.choice(TUTORS)
  return f'{tutor} will be at {location} right away!'

def locked_out_location_on_input(user_input, context):
  return 'NO QUERY', {}, 'Bye!'



# --- More states go here! --- #


def music_choice_on_enter_state(context):
  return jsonify({
    "text": "How do you want to choose your music? ",
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
                    "name": "Choice", "text": "Mood", "type": "button", "value": "mood"
                },{
                    "name": "Choice", "text": "Genre", "type": "button",  "value": "genre"
                },{
                    "name": "Choice", "text": "I'm not sure", "type": "button", "value": "IDK"
                },
            ]
        }
    ]
})

def music_choice_on_input(user_input, context):
  music = user_input
  return 'NO QUERY', {'music': music}, None




