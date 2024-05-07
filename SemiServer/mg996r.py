#PDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import RPi.GPIO as GPIO
from adafruit_motor import servo		#adafruit servo controll lib
from adafruit_pca9685 import PCA9685	#adafruit pca9685 controll lib

OPEN = 'OPEN'
CLOSE = 'CLOSE'

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

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c 통신을 위한 객체 생성 - board 라이브러리의 I2C 클래스 이용

pca = PCA9685(i2c)
# i2c 통신을 사용하는 pca9685 객체 생성
# pca = PCA9685(i2c, reference_clock_speed=25630710)
# 인자값을 추가로 주어 클럭 속도를 임의로 설정 가능
pca.frequency = 50
# pca 모듈의 주파수 설정

# 서보 머터를 위한 객체를 생성
# 최대 16개의 서보모터를 연결할 수 있는 보드
# 0 ~ 15 까지의 포트 존재
# 로봇팔의 서보 모터 - mg996R - min_pulse = 544, max_pulse=2400
#servo 0 - LEFT = 180, RIGHT = 0
# 가장 하단의 수평축 서보모터
servo0 = servo.Servo(pca.channels[0], min_pulse=544, max_pulse=2400)
#servo 1 - FORWARD = 180 , BACKWARD = 0
# 수직축의 가장 하단 모터
servo1 = servo.Servo(pca.channels[1], min_pulse=544, max_pulse=2400)
#servo 2 - FORWARD = 160, BACKWARD = 0
# 수직축 중간 모터 - 프레임의 간섭이 있기 때문에 동작 입력은 160을 최대로 한다
servo2 = servo.Servo(pca.channels[2], min_pulse=544, max_pulse=2400)
#servo 3 - FORWARD = 180, BACKWARD = 0
# 수직축 상단 모터
servo3 = servo.Servo(pca.channels[3], min_pulse=544, max_pulse=2400)
#servo 4 - CCwise = 0, Clockwise = 180
#Horizontal : angle = 15, vertical = 115
# 집게 위상 모터 - 위상 특성상 수직 또는 수평만을 사용할 확률이 높아 특정해놓음
servo4 = servo.Servo(pca.channels[4], min_pulse=544, max_pulse=2400)
#servo 5 - FASTEN = 120, LOOSEN = 40
# 집게 모터 - 지나치게 높은 값은집게 구조 특성상 모터에 무리를 줌
servo5 = servo.Servo(pca.channels[5], min_pulse=544, max_pulse=2400)

# mg995 모터 실험용 객체
doorMotor = [servo.Servo(pca.channels[i+10], min_pulse=500, max_pulse=2600) for i in range(0,5)]


# 로봇팔 초기 구동 함수
# 기본적인 위상으로 초기화
def arm_init():
	servo0.angle = 90
	servo1.angle = 50
	servo2.angle = 100
	servo3.angle = 140
	servo4.angle = 15
	servo5.angle = 40
	time.sleep(2)

# 로봇팔 자동 제어 1단계 : 웨이퍼 스테이지
def arm_phase1():
	servo0.angle = 180
	servo1.angle = 140
	time.sleep(2)
	servo2.angle = 160
	servo3.angle = 60
	servo4.angle = 115
	time.sleep(2)
	servo5.angle = 120
	time.sleep(1)
	servo1.angle = 50
	servo2.angle = 90
	servo3.angle = 110
	time.sleep(2)
	servo4.angle = 15

# 설비 문 제어
def door_move(loc, state) :
    i = loc
    print(loc, i)
    print('Hello')
    if state:
        print('World')
        doorMotor[i].angle = 150
        time.sleep(3)
    else :
        print('Morld')
        doorMotor[i].angle = 60
        time.sleep(3)

    print('ByeBye')
    doorMotor[i].angle = 90

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


# pca 모듈 종료 함수
