import time
import glob
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# Thermal Module setting
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Relay Module setting
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

TempFileRead()

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

# 릴레이 모듈 제어 함수
def relay_test():
	for i in range(1,3):
		GPIO.output(23, True)
		time.sleep(2)
		GPIO.output(23, False)
		time.sleep(2)

# =================== 로봇팔 동작 =====================
try:
	while True:
		print('--------------------------------------')
		print("Temp :", TempDataRead(), "'C")
		time.sleep(1)
except KeyboardInterrupt :
	GPIO.cleanup()
