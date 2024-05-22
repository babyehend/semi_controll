# 파이썬의 GPIO 입출력 제어를 통한 회로 동작을 구현한 파일
import time
import glob
import RPi.GPIO as GPIO

# 각 장치들이 연결되어 입출력을 제어할 핀 설정
# Motor driver PIN define
FAN_HMDS = 17       #Motor driver 1 - AIN1
PUMP_SPIN = 27      #Motor driver 1 - BIN1
PUMP1_DEVELOP = 14  #Motor driver 2 - AIN1
PUMP2_DEVELOP = 15  #Motor driver 2 - BIN1

# Relay module PIN define
MCRW_HMDS = 22      #RELAY module 1 - data
HEATPAD_BAKE = 21   #RELAY module 2 - data
FAN_DEVLP = 18      #RELAY module 3 - data
LIGHT_EX = 20       #RELAY module 4 - data

# Step motor driver PIN define
EN = 10
STEP = 9
DIR = 11
SPEED = 0.001

# Thermal module PIN define
THERMAL = 0
TEMP_SET = 40

# GPIO 핀 설정
GPIO.setwarnings(False) # 파일이 실행될때마다 출력되는 setup 오류를 없애는 설정
# GPIO PIN mode setting
GPIO.setmode(GPIO.BCM)
# Motor driver
GPIO.setup(PUMP_SPIN, GPIO.OUT)
GPIO.setup(FAN_HMDS, GPIO.OUT)
GPIO.setup(PUMP1_DEVELOP, GPIO.OUT)
GPIO.setup(PUMP2_DEVELOP, GPIO.OUT)

# Relay Module
GPIO.setup(MCRW_HMDS, GPIO.OUT)
GPIO.setup(HEATPAD_BAKE, GPIO.OUT)
GPIO.setup(FAN_DEVLP, GPIO.OUT)
GPIO.setup(LIGHT_EX, GPIO.OUT)

# Step motor driver
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

# Thermal Module
# 온도 센서는 값을 읽어와야 하기 때문에, 입력으로 설정.
GPIO.setup(THERMAL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# All PIN reset
GPIO.output(PUMP_SPIN, GPIO.LOW)
GPIO.output(FAN_HMDS, GPIO.LOW)
GPIO.output(PUMP1_DEVELOP, GPIO.LOW)
GPIO.output(PUMP2_DEVELOP, GPIO.LOW)
GPIO.output(MCRW_HMDS, GPIO.LOW)
GPIO.output(HEATPAD_BAKE, GPIO.LOW)
GPIO.output(FAN_DEVLP, GPIO.LOW)
GPIO.output(LIGHT_EX, GPIO.LOW)
GPIO.output(EN, GPIO.HIGH)
GPIO.output(STEP, GPIO.LOW)
GPIO.output(DIR, GPIO.LOW)

def set_spinspeed(value):
	SPEED = value

def set_temp(value):
	TEMP_SET = value

# ------------ Motor driver function --------------- #
def hmds_fan_work():
	GPIO.output(FAN_HMDS, GPIO.HIGH)
	time.sleep(8)
	GPIO.output(FAN_HMDS, GPIO.LOW)

def spin_pump_work():
	GPIO.output(PUMP_SPIN, GPIO.HIGH)
	time.sleep(1.5)
	GPIO.output(PUMP_SPIN, GPIO.LOW)

def develop_pump1_work():
	GPIO.output(PUMP1_DEVELOP, GPIO.HIGH)
	time.sleep(7)
	GPIO.output(PUMP1_DEVELOP, GPIO.LOW)
	
def develop_pump2_work():
	GPIO.output(PUMP2_DEVELOP, GPIO.HIGH)
	time.sleep(7)
	GPIO.output(PUMP2_DEVELOP, GPIO.LOW)
	
# ------------ Relay module function --------------- #
def hmds_vapor_work():
	GPIO.output(MCRW_HMDS, GPIO.HIGH)
	time.sleep(10)
	GPIO.output(MCRW_HMDS, GPIO.LOW)

def bake_heatpad_on():
	GPIO.output(HEATPAD_BAKE, GPIO.HIGH)

def bake_heatpad_off():
	GPIO.output(HEATPAD_BAKE, GPIO.LOW)

def develop_fan_work():
	GPIO.output(FAN_DEVLP, GPIO.HIGH)
	time.sleep(10)
	GPIO.output(FAN_DEVLP, GPIO.LOW)

def exposure_light_on():
	GPIO.output(LIGHT_EX, GPIO.HIGH)

def exposure_light_off():
	GPIO.output(LIGHT_EX, GPIO.LOW)
	
# ------------ Relay module function --------------- #
def spin_stepmotor_work():
	GPIO.output(EN, GPIO.LOW)
	for i in range(0,3000):
		GPIO.output(STEP, GPIO.HIGH)
		time.sleep(0.001)
		GPIO.output(STEP, GPIO.LOW)
		time.sleep(0.001)
	GPIO.output(EN, GPIO.HIGH)

# ------------ AUTO PROCESS function --------------- #
def auto_hmds():
	GPIO.output(MCRW_HMDS, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(FAN_HMDS, GPIO.HIGH)
	time.sleep(8)
	GPIO.output(MCRW_HMDS, GPIO.LOW)
	GPIO.output(FAN_HMDS, GPIO.LOW)

def auto_spin():
	spin_pump_work()
	time.sleep(1)
	spin_stepmotor_work()

def auto_develop():
	develop_pump1_work()
	time.sleep(0.5)
	develop_pump2_work()
	time.sleep(1)
	develop_fan_work()

def auto_exposure():
	exposure_light_on()
	time.sleep(10)
	exposure_light_off()

# 온도센서와 1-wire 통신 연결
# Thermal module directory
base_dir = '/sys/bus/w1/devices/'

while True:
	try:
		device_folder = glob.glob(base_dir + '28*')[0] # 온도센서 모듈을 찾아서 저장
		break
	except IndexError:
		time.sleep(0.5)
		continue

# 입력된 데이터가 저장되는 파일 경로 저장
device_file = device_folder + '/w1_slave'

# 저장된 데이터 파일에서 온도값을 추출하는 함수
def TempFileRead():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# 추출된 온도값을 실수형 데이터로 변환 하여 반환 하는 함수
def TempDataRead():
	lines = TempFileRead()
	while lines[0].strip()[-3:] != 'YES' :
		time.sleep(0.2)
		lines = TempFileRead()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos + 2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c