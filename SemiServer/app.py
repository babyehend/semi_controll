from flask import Flask, request, jsonify
from flask_restful import Api
import gpio_ctrl as gc
import servo_module as sm
import serial_RasbPiToAVR as sr

app = Flask(__name__)
api = Api(app)

# ----------- DEFINE PARAMETER -------------#
# PROCESS NAME
HMDS = 'HMDS'
SPIN = 'SPIN'
BAKE = 'BAKE'
AUTO = 'AUTO'
DEVELOP = 'DEVELOP'
EXPOSURE = 'EXPOSURE'
AUTO_STATE = 'AUTO_STATE'

# STATE NAME
ON = 'ON'
OFF = 'OFF'

OPEN = 'OPEN'
CLOSE = 'CLOSE'

# TEMP STATE
TEMP = 'TEMP'
SOFT = 'SOFT'
HADR = 'HADR'
POSTEX = 'POSTEX'

# DEVICE NAME
DOOR = 'DOOR'
DEV = ['DEV1','DEV2','DEV3']
MODE = ['HEAT']

# TEMP DATA SHEET - {dict}
temp_sheet = {
    SOFT : 50,
    HADR : 80,
    POSTEX : 90
}

# each category list to get index - used for funcs
l_sector = [HMDS, SPIN, BAKE, DEVELOP, EXPOSURE, AUTO_STATE]
l_state_motor = [OFF, ON]
l_state_door = [CLOSE, OPEN]


# SECTOR 1 - HMDS FUNCS
state_hmds = {
    DOOR : CLOSE,
    DEV[0] : OFF, #HUMIDIATOR WAVE
}
# SECTOR 2 - SPIN FUNCS
state_spin = {
    DOOR : CLOSE,
    DEV[0] : OFF, #STEP MOTOR
}
# SECTOR 3 - BAKE FUNCS
state_bake = {
    DOOR : CLOSE,
    MODE[0] : SOFT,
    TEMP : '50'
}

# SECTOR 4 - DEVELOP FUNCS
state_develop = {
    DOOR : CLOSE,
    DEV[0] : OFF, #DC MOTOR
    DEV[1] : OFF, #PUMP MOTOR 2
    DEV[2] : OFF, #PUMP MOTOR 2
}

# SECTOR 5 - EXPOSURE FUNCS
state_expo = {
    DOOR : CLOSE,
    DEV[0] : OFF, #LED
}
# AUTO PROCESS

def auto_process_on():
    print("AUTO PROCESS ON")

def auto_process_off():
    print("AUTO PROCESS OFF")

state_auto = {
    AUTO : OFF,
}

run_auto = {
    AUTO : { ON : auto_process_on, OFF : auto_process_off },
}

state_main = {
    AUTO_STATE : state_auto,
    HMDS : state_hmds,
    SPIN : state_spin,
    BAKE : state_bake,
    DEVELOP : state_develop,
    EXPOSURE : state_expo,
}

def activate_door(sect, state) :
    print(sect, "Door", state)
    sm.door_move(l_sector.index(sect), l_state_door.index(state))

def activate_motor(sect, dev) :
    print(sect, dev, "activation")
    sr.put_data(sect=sect, dev=dev)

def run_device(sect, dev, state) :
    if dev == DOOR :
        activate_door(sect, state)
    elif dev in DEV:
        activate_motor(sect, dev)
    elif dev in MODE:
        pass

@app.route('/')
def init_state() :
    return state_main

@app.route('/', methods=['GET'])
def get_state() :
    return state_main

@app.route('/', methods=['PATCH'])
def update_state():
    data = request.json
    # Update the state data based on the PATCH request data
    for key, value in data.items():
        state_main[key].update(value)
        i = list(value.keys())[0]
        j = list(value.values())[0]
        run_device(key, i, j)
    # Update other states similarly
    return state_main

if __name__ == '__main__' :
    app.run(debug=True)
