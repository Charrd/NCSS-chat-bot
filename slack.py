from flask import Flask, jsonify, request
from bot import on_enter_state, on_input
from flaskapp import app

state = 'NO QUERY'
context = {}

@app.route('/slack/slash', methods=['GET', 'POST'])
def slack_event():
  global state, context
  payload = request.values
  print(payload)  # Print payload for debugging.
  output = ""
  if payload:
    user_input = payload.get('text')
    # todo: finish this slack interface!
    while state != "END":
      state, context, output1 = on_input(state, user_input, context)
      output2 = on_enter_state(state, context)
      if type(output2) is dict:
        output = output2

      elif type(output2) is str or output2 == None:
        output = ''
        if output1 != None:
          output += output1
        if output2 != None:
          output += output2
      return jsonify(output)
  return ""
if __name__ == '__main__':
  app.run(debug = True)
