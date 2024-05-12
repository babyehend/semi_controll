import time
import glob
import RPi.GPIO as GPIO

# Motor driver PIN define
STBY_PWM = 4 	    #HIGHT Input PIN for all STBY & PWMS
PUMP_HMDS = 17      #Motor driver 1 - AIN1
FAN_HMDS = 22       #Motor driver 1 - BIN1
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

# Thermal module PIN define
THERMAL = 0

# GPIO PIN mode setting
GPIO.setmode(GPIO.BCM)
# Motor driver
GPIO.setup(STBY_PWM, GPIO.OUT)
GPIO.setup(PUMP_HMDS, GPIO.OUT)
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
GPIO.setup(THERMAL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# All PIN reset
GPIO.output(STBY_PWM, GPIO.LOW)
GPIO.output(PUMP_HMDS, GPIO.LOW)
GPIO.output(FAN_HMDS, GPIO.LOW)
GPIO.output(PUMP1_DEVELOP, GPIO.LOW)
GPIO.output(PUMP2_DEVELOP, GPIO.LOW)
GPIO.output(MCRW_HMDS, GPIO.LOW)
GPIO.output(HEATPAD_BAKE, GPIO.LOW)
GPIO.output(FAN_DEVLP, GPIO.LOW)
GPIO.output(LIGHT_EX, GPIO.LOW)
GPIO.output(EN, GPIO.LOW)
GPIO.output(STEP, GPIO.LOW)
GPIO.output(DIR, GPIO.LOW)

# ------------ Motor driver function --------------- #
def hmds_pump_work():
	GPIO.output(PUMP_HMDS, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(PUMP_HMDS, GPIO.LOW)

def hmds_fan_work():
	GPIO.output(FAN_HMDS, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(FAN_HMDS, GPIO.LOW)

def develop_pump1_work():
	GPIO.output(PUMP1_DEVELOP, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(PUMP1_DEVELOP, GPIO.LOW)
	
def develop_pump2_work():
	GPIO.output(PUMP2_DEVELOP, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(PUMP2_DEVELOP, GPIO.LOW)
	
# ------------ Relay module function --------------- #
def hmds_vapor_work():
	GPIO.output(MCRW_HMDS, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(MCRW_HMDS, GPIO.LOW)

def bake_heatpad_work():
	GPIO.output(HEATPAD_BAKE, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(HEATPAD_BAKE, GPIO.LOW)

def develop_fan_work():
	GPIO.output(FAN_DEVLP, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(FAN_DEVLP, GPIO.LOW)

def exposure_light_work():
	GPIO.output(LIGHT_EX, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(LIGHT_EX, GPIO.LOW)
	
# ------------ Relay module function --------------- #
def spin_stepmotor_work():
	GPIO.output(MCRW_HMDS, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(MCRW_HMDS, GPIO.LOW)


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

# =================== 로봇팔 동작 =====================
try:
	hmds_vapor_work()
	while True:
		print('--------------------------------------')
		print("Temp :", TempDataRead(), "'C")
		time.sleep(1)
except KeyboardInterrupt :
	GPIO.cleanup()

# You can also specify the movement fractionally.
"""
class ServoFractionMove():
	def init_motor(num):
		pre_loc = 0.0
		fraction = pre_loc
		post_loc = 0.5
		while fraction < post_loc:
			armMotor[num].fraction = fraction
			fraction += 0.01
			time.sleep(0.03)
		pre_loc = post_loc
		
	def servo_work(input_angle, num):
		post_loc = 1.0 * ( input_angle / 180 )
		fraction = pre_loc
		while fraction < post_loc:
			armMotor[num].fraction = fraction
			fraction += 0.01
			time.sleep(0.03)
		pre_loc = post_loc
"""