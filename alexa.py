from flask import Flask, jsonify, request
from bot import on_enter_state, on_input
from flaskapp import app

state = 'NO QUERY'
context = {}

@app.route('/alexa', methods=['GET', 'POST'])
def alexa_event():
    global state, context
    payload = request.get_json()
    print(payload)  # Print payload for debugging.
    output = ""
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
                    output += output1
                if output2 != None:
                    output += output2
        else:
            output = 'Hi, I\'m Eve, how can i help?'

      
        return jsonify({
        'version': '0.1',
        'response': {
          'outputSpeech': {
          'type': 'PlainText',
          'text': output,
          },
          'shouldEndSession': False
        }
        })
    return ""

if __name__ == '__main__':
  app.run(debug = True)
