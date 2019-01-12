from flask import Flask, jsonify, request
from bot_alexa import on_enter_state, on_input, STATE_NO_QUERY
from flaskapp import app

state = STATE_NO_QUERY
context = {}

def render_list(response):
  list_items = []
  for item in response['list']:
    list_items.append({
      'token': item['text'],
      'textContent': {
        'primaryText': {
          'type': 'PlainText',
          'text': item['text']
        }
      },
    })
  
  return {
    'version': '0.1',
    'response': {
      'outputSpeech': {
        'type': 'SSML',
        'ssml': f"""<speak><voice name="Russell">{response['text']}</voice></speak>""",
      },
      'directives': [
        {
          'type': 'Display.RenderTemplate',
          'template': {
            'type': 'ListTemplate1',
            'backButton': 'HIDDEN',
            'title': response['text'],
            'token': 'test',
            'listItems': list_items,
          }
        }
      ],
      'shouldEndSession': response.get('end', False),
    }
  }


@app.route('/alexa', methods=['GET', 'POST'])
def alexa_event():
    global state, context
    payload = request.get_json()
    print(payload)  # Print payload for debugging.
    output = ""
    directives = []
    if payload:
        request_type = payload['request']['type']
        if request_type == 'IntentRequest':
            query = payload['request']['intent']['slots']['query']['value']
            user_input = query
            #what does this do 
            if state != "END":
                state, context, output1 = on_input(state, user_input, context)
                output2 = on_enter_state(state, context)
                if output1 != None:
                    output += output1 + ' '
                if "text" in output2:
                    if output2["text"] != None:  
                        output += output2["text"]
                if "directives" in output2:
                    directives.append(output2["directives"])

        else:
            output = 'Hi, I\'m Eve, how can i help?'

      
        return jsonify({
        'version': '0.1',
        'response': {
          'outputSpeech': {
          'type': 'PlainText',
          'text': output,
          'directives': directives,
          },
          'shouldEndSession': False
        }
        })
    return ""

if __name__ == '__main__':
  app.run(debug = True)
