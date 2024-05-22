"""
2024년 1학기 - 상명대학교 전작공학과 4학년 < 캡스톤 디자인 1 > 과목 프로젝트 프로그램
캡스톤 디자인 1
 - 팀명 : Semiconductor
 - 주제 : 노광장비의 구현과 동작 시뮬레이션
 - 팀원 : 박건호(조장), 정도윤(프로그램), 김정빈(설비제작), 김태형(설비제작)

프로그램 목적 :
 - 설계된 노광장비의 회로들을 인터페이스를 통해 제어, 상태를 관찰한다
 - 장비의 상태를 전기적으로 확인하고 조작한다.
 - 이를 통해 장비를 유지보수 할수있는 환경을 확보한다.

프로그램 구성 :
 - Dart를 기반으로한 Flutter 프레임워크를 통한 인터페이스(앱) 구현
    -> 상태 패널을 통한 회로와 장치의 상태 표시, 버튼을 통한 장치의 동작을 제어
 - Python 언어의 앱 프레임워크 Flask 를 통해 로컬 서버 구현
    -> 장치들의 데이터를 저장, 상태와 변화를 앱과 라즈베리파이 사이에서 확인하고 제어한다.
 - Python 에서 제공하는 라즈베리파이 I/O 제어 모듈을 통한 입출력 제어 ex) RPi.GPIO 라이브러리
"""
from flask import Flask, request
from flask_restful import Api
import time
import threading
import gpio_ctrl as gc
import servo_module as sm

app = Flask(__name__)
api = Api(app)

# 온도센서의 데이터를 일정시간마다(interval) 읽어오도록 함수를 실행시켜줄 
# Threading 모듈을 이용한 Class
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function  = function
        self.args = args
        self.kwargs = kwargs
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
# 로컬 서버에 저장될 각 장치들의 상태 값들의 문자열을 상수로 선언
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
# 스탭모터의 회전 속도를 각 설정값에 맞게 반환 할 수 있도록 딕셔너리 선언
# 각 값들은 스탭모터의 동작 지연 시간을 가진다.

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
# 각 설정에 따라 히트 패드의 최대 온도 설정을 위한 임계값을 가지는 딕셔너리

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

# 버튼의 동작을 확인 하기 위한 문자열 출력 함수
# - 동작상의 의미는 없다.
def auto_process_on():
    print("AUTO PROCESS ON")

def auto_process_off():
    print("AUTO PROCESS OFF")

state_auto = {
    AUTO : OFF,
}

# 로컬 서버에 저장되는 모든 장치들의 상태 딕셔너리 변수
state_main = {
    AUTO_STATE : state_auto,
    HMDS : state_hmds,
    SPIN : state_spin,
    BAKE : state_bake,
    DEVELOP : state_develop,
    EXPOSURE : state_expo,
}

# ---------------------- 온도 데이터 갱신 ---------------------------- #
# 온도값을 읽어 t 값에 설정하고 임계값 설정에 따라 히트패드의 동작을 조절하는 함수
# 온도센서의 값을 읽는 TempDataRead 함수는 gpio_ctrl.py ( as gc ) 에 선언 되어 있다.
def set_temperature():
    temp_c = gc.TempDataRead()
    t = float(temp_c)
    print(f"t : {t}") # 확인을 위해 저장된 온도값 출력
    state_main[BAKE][TEMP] = str(t)
    # 임계값 설정에 따른 히트패드 동작 조건문
    if t >= HEAT_VALUE[state_main[BAKE][MODE[0]]] :
        gc.bake_heatpad_off()
    else :
        gc.bake_heatpad_on()

# 온도 값 갱신 주기를 1초로 설정
interval_s = 1

# 반복 주기와 반복 함수를 인자로 주는 객체 선언
rt = RepeatedTimer(interval_s, set_temperature)

# 각 공정 단계별 문 상태 데이터 변경시 그에 맞는 서보모터를 동작시키는 함수 
def activate_door(sect, state) :
    i = l_sector.index(sect)
    j = l_state_door.index(state)
    if i == 1:
        sm.spin_door_move(l_state_door.index(state))
    else :
        sm.door_move(l_sector.index(sect), l_state_door.index(state))

# 각 공정의 장치를 가동시키는 함수
def activate_motor(sect, dev) :
    print(sect, dev, "activation")
    if sect == HMDS:
        gc.auto_hmds()
    elif sect == SPIN:
        gc.auto_spin()
    elif sect == DEVELOP:
        if dev == DEV[0] :
            gc.develop_fan_work()
        elif dev == DEV[1] :
            gc.develop_pump1_work()
        elif dev == DEV[2] :
            gc.develop_pump2_work()
    elif sect == EXPOSURE:
        gc.auto_exposure()
    
# 자동 공정을 시작하도록 하는 함수
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

    sm.door_move(0,0)

    # HMDS start
    gc.auto_hmds()
    time.sleep(3)
    # HMDS end
    sm.door_move(0,1)

    sm.hmds_out()
    time.sleep(2)

    # Wafer SPIN COATING in
    sm.spin_in()
    time.sleep(3)
    # SPIN COATING start
    sm.spin_door_move(0)
    gc.auto_spin()
    time.sleep(3)
    # SPIN COATING end
    sm.spin_door_move(1)
    sm.spin_out()
    time.sleep(2)

    # Wafer Soft BAKE in
    sm.bake_in()
    time.sleep(3)
    sm.door_move(2,0)
    # Hard BAKE start
    time.sleep(10)
    sm.door_move(2,1)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = HARD
    time.sleep(2)

    # Wafer EXPOSURE in
    sm.exposure_in()
    time.sleep(3)
    sm.door_move(4,0)
    # EXPOSURE start
    gc.auto_exposure()
    time.sleep(3)
    sm.door_move(4,1)
    # EXPOSURE end
    sm.exposure_out()
    time.sleep(2)

    # Wafer PostEx BAKE in
    sm.bake_in()
    time.sleep(3)
    sm.door_move(2,0)
    # Hard BAKE start
    time.sleep(10)
    sm.door_move(2,1)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = SOFT
    time.sleep(2)

    # Wafer DEVELOP in
    sm.develop_in()
    time.sleep(3)
    sm.door_move(3,0)
    # DEVELOP start
    gc.auto_develop()
    time.sleep(3)
    sm.door_move(3,1)
    # DEVELOP end
    sm.develop_out()
    time.sleep(2)

    # Wafer Hard BAKE in
    sm.bake_in()
    time.sleep(3)
    sm.door_move(2,0)
    # Hard BAKE start
    time.sleep(10)
    sm.door_move(2,1)
    # Hard BAKE end
    sm.bake_out()
    state_bake[MODE[0]] = POSTEX
    time.sleep(2)

# 스탭 모터의 회전 속도, 히트 패드의 임계 온도값 설정이 변경됬을때, 값을 변경하는 함수
def change_setting(sect, state):
    print(sect, 'value changes to', state)
    if sect == SPIN:
        gc.set_spinspeed(SPIN_SPEED[state])
    else :
        gc.set_temp(HEAT_VALUE[state])

# 로컬서버의 데이터가 변환되면 실행되어 알맞은 동작을 하게 하는 함수
def run_device(sect, dev, state) :
    # 변화된 데이터의 dev 값에 따라 동작 함수를 구분
    if dev == DOOR :
        # 문의 상태가 변화
        activate_door(sect, state)
    elif dev in DEV:
        # 장치의 상태가 변화
        activate_motor(sect, dev)
    elif dev in MODE:
        # 장치의 설정값이 변화
        change_setting(sect, state)
    elif dev == AUTO :
        # 자동 공정의 상태 변화
        if state == ON :
            activate_autoprocess(state)
        else :
            sm.arm_deinit()

# 플라스크 앱의 기본 페이지에 state_main 데이터를 반환 / 저장
@app.route('/')
def init_state() :
    return state_main

# 앱종료가 실행되면 로컬 서버를 종료하기 위해 정의한 종료 페이지
# 구동 미구현
@app.route('/exit')
def deinit_state() :
    exit()

# 앱의 메인 페이지에서 'GET' 메소드 호출에 대한 동작 정의
# 현재 state_main 값을 반환 하여 데이터 갱신
@app.route('/', methods=['GET'])
def get_state() :
    return state_main

# 'PATCH' 메소드 호출에 대한 동작 정의
@app.route('/', methods=['PATCH'])
# 서버의 데이터를 수정하는 함수 정의
def update_state():
    data = request.json # 'PATCH' 함수에 의해 입력된 data를 저장
    # Update the state data based on the PATCH request data
    for key, value in data.items():
        # json 형식의 데이터는 dict 타입이므로 key, value 로 구분 해서 읽어들임
        state_main[key].update(value) # 읽어 들인 변화를 기존 데이터 변수에 적용
        i = list(value.keys())[0]     # 변환 데이터를 세부적으로 다시 분리 ( dict 의 value 값으로 dict 타입을 주고 있기 때문 )
        j = list(value.values())[0]
        run_device(key, i, j)         # 세분화한 데이터를 인자로 상태 변화에 따른 함수 실행
    # Update other states similarly
    return state_main

# 플라스크 앱을 실행 시키는 함수
if __name__ == '__main__' :
    # 앱 실행과 동시에 반복 객체의 실행 함수 호출
    rt.start()
    app.run(debug=True)
