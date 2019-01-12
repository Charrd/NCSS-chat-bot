from flask import Flask, jsonify, request
from bot import on_enter_state, on_input
from flaskapp import app
import json

state = 'NO QUERY'
context = {}

@app.route('/slack/slash', methods=['GET', 'POST'])
def slack_event():
  global state, context
  payload = request.values
  print(payload)  # Print payload for debugging.
  output = ""
  if payload:
    text = payload.get('text')
    payload = payload.get('payload')
    # todo: finish this slack interface!
    while state != "END":
      if text:
        print('Type: text')
        state, context, output1 = on_input(state, text, context)
      elif payload:
        print('Type: payload')
        json_payload = json.loads(payload)
        actions = json_payload.get('actions')
        first_action = actions[0]
        value = first_action.get("value")
        state, context, output1 = on_input(state, value, context)
      output2 = on_enter_state(state, context)
      if type(output2) is dict:
        print("return Type: dict")
        output = output2
        return jsonify(output)

      elif type(output2) is str or output2 == None:
        print("return Type: string")
        output = ''
        if output1 != None:
          output += output1
        if output2 != None:
          output += output2
        return jsonify({
          "response_type": "in_channel",
          'text': output
        })
  return ""
if __name__ == '__main__':
  app.run(debug = True)
