from flask import Flask, request
from flask_restful import Api
import time
import threading
import gpio_ctrl as gc
import servo_module as sm

app = Flask(__name__)
api = Api(app)

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


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

SLOW = 'SLOW'
MIDDLE = 'MIDDLE'
FAST = 'FAST'
SPIN_SPEED = {
    SLOW : 0.003,
    MIDDLE : 0.002,
    FAST : 0.001,
}

# TEMP STATE
TEMP = 'TEMP'
SOFT = 'SOFT'
HARD = 'HARD'
POSTEX = 'POSTEX'
HEAT_VALUE = {
    SOFT : 30,
    HARD : 40,
    POSTEX : 35
}

t = 0

# DEVICE NAME
DOOR = 'DOOR'
DEV = ['DEV1','DEV2','DEV3']
MODE = ['HEAT_VALUE', 'SPIN_SPEED']

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
    MODE[1] : MIDDLE
}
# SECTOR 3 - BAKE FUNCS
state_bake = {
    DOOR : CLOSE,
    MODE[0] : SOFT,
    TEMP : str(t)
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

def set_temperature(temp_C):
    t = temp_C
    print("t : {t}")
    if t >= HEAT_VALUE[state_bake[MODE[0]]] :
        gc.bake_heatpad_off
    else :
        gc.bake_heatpad_on


interval_s = 1

rt = RepeatedTimer(interval_s, gc.TempDataRead)
rt.function = set_temperature()

def activate_door(sect, state) :
    print(sect, "Door", state)
    # sm.door_move(l_sector.index(sect), l_state_door.index(state))

def activate_motor(sect, dev) :
    print(sect, dev, "activation")
    if sect == HMDS:
        if dev == DEV[0] :
            gc.hmds_fan_work()
        elif dev == DEV[1] :
            gc.hmds_vapor_work()

def activate_autoprocess(state):
    print('Auto process', state)
    state_bake[MODE[0]] = SOFT
    # Wafer Stage out
    sm.stage_out()
    time.sleep(2)
    # Robotarm Standby

    # Wafer HMDS in
    sm.hmds_in()
    time.sleep(3)
    # HMDS start
    gc.auto_hmds()
    time.sleep(3)
    # HMDS end
    sm.hmds_out()
    time.sleep(2)

    # Wafer Soft BAKE in
    sm.bake_in()
    time.sleep(3)
    # Hard BAKE start
    time.sleep(10)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = HARD
    time.sleep(2)

    # Wafer SPIN COATING in
    sm.spin_in()
    time.sleep(3)
    # SPIN COATING start
    gc.auto_spin()
    time.sleep(3)
    # SPIN COATING end
    sm.spin_out()
    time.sleep(2)

# Wafer Hard BAKE in
    sm.bake_in()
    time.sleep(3)
    # Hard BAKE start
    time.sleep(10)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = POSTEX
    time.sleep(2)

    # Wafer DEVELOP in
    sm.develop_in()
    time.sleep(3)
    # DEVELOP start
    gc.auto_develop()
    time.sleep(3)
    # DEVELOP end
    sm.develop_out()
    time.sleep(2)

    # Wafer PostEx BAKE in
    sm.bake_in()
    time.sleep(3)
    # Hard BAKE start
    time.sleep(10)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = SOFT
    time.sleep(2)

    # Wafer EXPOSURE in
    sm.exposure_in()
    time.sleep(3)
    # EXPOSURE start
    gc.auto_exposure()
    time.sleep(3)
    # EXPOSURE end
    sm.exposure_out()
    time.sleep(2)

    # Wafer Stage out
    sm.stage_in()
    time.sleep(2)
    # Robotarm Standby

def change_setting(sect, state):
    print(sect, 'value changes to', state)
    if sect == SPIN:
        gc.set_spinspeed(SPIN_SPEED[state])
        pass
    else :
        gc.set_temp(HEAT_VALUE[state])
        pass

def run_device(sect, dev, state) :
    if dev == DOOR :
        activate_door(sect, state)
    elif dev in DEV:
        activate_motor(sect, dev)
    elif dev in MODE:
        change_setting(sect, state)
    elif dev == AUTO :
        if state == ON :
            activate_autoprocess(state)

@app.route('/')
def init_state() :
    rt.start()
    return state_main

@app.route('/exit')
def deinit_state() :
    exit()

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
