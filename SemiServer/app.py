from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

state_hmds = {
    'DOOR' : 'CLOSE',
    'DEV1' : 'OFF', #HUMIDIATOR WAVE
}

state_spin = {
    'DOOR' : 'CLOSE',
    'DEV1' : 'OFF', #STEP MOTOR
}

state_bake = {
    'DOOR' : 'CLOSE',
    'DEV1' : 'SOFT',
    'TEMP' : '0', #HEAT PAD
}

state_dev = {
    'DOOR' : 'CLOSE',
    'DEV1' : 'OFF', #DC MOTOR
    'DEV2' : 'OFF', #PUMP MOTOR 1
    'DEV3' : 'OFF', #PUMP MOTOR 2
}

state_expo = {
    'DOOR' : 'CLOSE',
    'DEV1' : 'OFF', #LED
}

state_auto = {
    'AUTO' : 'OFF',
}

state_main = {
    'AUTO_STATE' : state_auto,
    'HMDS' : state_hmds,
    'SPIN' : state_spin,
    'BAKE' : state_bake,
    'DEVELOP' : state_dev,
    'EXPOSURE' : state_expo,
}

@app.route('/', methods=['GET'])
def hello_world() :
    return state_main

@app.route('/', methods=['PATCH'])
def update_state():
    data = request.json
    # Update the state data based on the PATCH request data
    for key, value in data.items():
        state_main[key].update(value)
    # Update other states similarly
    return state_main

if __name__ == '__main__' :
    app.run(debug=True)