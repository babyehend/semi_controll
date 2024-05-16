import time
import glob
import RPi.GPIO as GPIO

# Motor driver PIN define
FAN_HMDS = 17       #Motor driver 1 - AIN1
PUMP_SPIN = 22      #Motor driver 1 - BIN1
PUMP1_DEVELOP = 19  #Motor driver 2 - AIN1
PUMP2_DEVELOP = 26  #Motor driver 2 - BIN1

# Relay module PIN define
MCRW_HMDS = 14      #RELAY module 1 - data
HEATPAD_BAKE = 15   #RELAY module 2 - data
FAN_DEVLP = 18      #RELAY module 3 - data
LIGHT_EX = 23       #RELAY module 4 - data

# Step motor driver PIN define
EN = 12
STEP = 20
DIR = 21
SPEED = 0.001

# Thermal module PIN define
THERMAL = 0
TEMP_SET = 40

GPIO.setwarnings(False)
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
#GPIO.setup(THERMAL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
		time.sleep(SPEED)
		GPIO.output(STEP, GPIO.LOW)
		time.sleep(SPEED)
		if i > 400 :
			SPEED = 0.002
			print("current delay : ", SPEED)
		if i > 1200 :
			SPEED = 0.001
			print("current delay : ", SPEED)
		if i > 2400 :
			SPEED = 0.003
			print("current delay : ", SPEED)
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

# Thermal module directory
base_dir = '/sys/bus/w1/devices/'

while True:
	try:
		device_folder = glob.glob(base_dir + '28*')[0]
		break
	except IndexError:
		time.sleep(0.5)
		continue

device_file = device_folder + '/w1_slave'

def TempFileRead():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

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
	
"""
try:
	while True:
		temp_cur = TempDataRead()
		print(temp_cur)
		if temp_cur >= TEMP_SET :
			bake_heatpad_off()
		else :
			bake_heatpad_on()
		time.sleep(1)
except KeyboardInterrupt :
	print("auto start")
"""