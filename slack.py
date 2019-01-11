from flask import Flask, jsonify, request
from bot import on_enter_state, on_input

app = Flask(__name__)

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
      if output1 != None:
        output += output1
      if output2 != None:
        output += output2
      output["response_type"] = "in_channel"
      return jsonify(output)
  return ""
if __name__ == '__main__':
  app.run(debug = True)
