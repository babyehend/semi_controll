from flask import Flask, request, jsonify
from flask_restful import Api
from mg996r import door_move

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
SOFT = 'SOFT'
HADR = 'HADR'
POSTEX = 'POSTEX'

# DEVICE NAME
DOOR = 'DOOR'
DEV1 = 'DEV1'
DEV2 = 'DEV2'
DEV3 = 'DEV3'

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
def door_open_hmds():
    print("HMDS Door Open")

def door_close_hmds():
    print("HMDS Door Close")

def dev1_on_hmds():
    print("HMDS air dispenser ON")

def dev1_off_hmds():
    print("HMDS air dispenser OFF")

state_hmds = {
    DOOR : CLOSE,
    DEV1 : OFF, #HUMIDIATOR WAVE
}

run_hmds = {
    DOOR : {OPEN : door_open_hmds, CLOSE : door_close_hmds},
    DEV1 : {ON : dev1_on_hmds, OFF : dev1_off_hmds},
}

# SECTOR 2 - SPIN FUNCS

def door_open_spin():
    print("SPIN Door Open")

def door_close_spin():
    print("SPIN Door Close")

def dev1_on_spin():
    print("SPIN ON")

def dev1_off_spin():
    print("SPIN OFF")

state_spin = {
    DOOR : CLOSE,
    DEV1 : OFF, #STEP MOTOR
}

run_spin = {
    DOOR : {OPEN : door_open_spin, CLOSE : door_close_spin},
    DEV1 : {ON : dev1_on_spin, OFF : dev1_off_spin},
}

# SECTOR 3 - BAKE FUNCS
def door_open_bake():
    print("BAKE Door Open")

def door_close_bake():
    print("BAKE Door Close")

def dev1_on_bake():
    print("BAKE heat pad ON")

def dev1_off_bake():
    print("BAKE heat pad OFF")

def dev1_set_bake():
    print("BAKE temp set : none")

temp_mode_bake = 0;

state_bake = {
    DOOR : CLOSE,
    DEV1 : SOFT,
    'TEMP' : '50', #HEAT PAD
}

run_bake = {
    DOOR : {OPEN : door_open_bake, CLOSE : door_close_bake},
    DEV1 : {SOFT : dev1_set_bake, HADR : dev1_set_bake, POSTEX : dev1_set_bake},
}

# SECTOR 4 - DEVELOP FUNCS
def door_open_develop():
    print("DEVELOP Door Open")

def door_close_develop():
    print("DEVELOP Door Close")

def dev1_on_develop():
    print("DEVELOP DEV1 ON")

def dev1_off_develop():
    print("DEVELOP DEV1 OFF")

def dev2_on_develop():
    print("DEVELOP DEV2 ON")

def dev2_off_develop():
    print("DEVELOP DEV2 OFF")

def dev3_on_develop():
    print("DEVELOP DEV3 ON")

def dev3_off_develop():
    print("DEVELOP DEV3 OFF")

state_develop = {
    DOOR : CLOSE,
    DEV1 : OFF, #DC MOTOR
    DEV2 : OFF, #PUMP MOTOR 1
    DEV3 : OFF, #PUMP MOTOR 2
}

run_develop = {
    DOOR : {OPEN : door_open_develop, CLOSE : door_close_develop},
    DEV1 : {ON : dev1_on_develop, OFF : dev1_off_develop},
    DEV2 : {ON : dev2_on_develop, OFF : dev2_off_develop},
    DEV3 : {ON : dev3_on_develop, OFF : dev3_off_develop},
}

# SECTOR 5 - EXPOSURE FUNCS
def door_open_exposure():
    print("EXPOSURE Door Open")

def door_close_exposure():
    print("EXPOSURE Door Close")

def dev1_on_exposure():
    print("LIGHT ON")

def dev1_off_exposure():
    print("LIGHT OFF")

state_expo = {
    DOOR : CLOSE,
    DEV1 : OFF, #LED
}

run_expo = {
    DOOR : {OPEN : door_open_exposure, CLOSE : door_close_exposure},
    DEV1 : {ON : dev1_on_exposure, OFF : dev1_off_exposure},
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

run_main = {
    AUTO_STATE : run_auto,
    HMDS : run_hmds,
    SPIN : run_spin,
    BAKE : run_bake,
    DEVELOP : run_develop,
    EXPOSURE : run_expo,
}

def run_by_state(sect, dev, state) :
    run_main[sect][dev][state]()

def activate_door(sect, state) :
    print(sect, "Door", state)

def activate_dev(sect, state) :
    print(sect, 'Device', state)

def run_device(sect, dev, state) :
    if dev == DOOR :
        activate_door(sect, state)
        print(l_sector.index(sect))
        print(type(l_sector.index(sect)))
        door_move(l_sector.index(sect), l_state_door.index(state))
    else:
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
        # run_by_state(key, i, j)
        run_device(key, i, j)
    # Update other states similarly
    return state_main

if __name__ == '__main__' :
    app.run(debug=True)
