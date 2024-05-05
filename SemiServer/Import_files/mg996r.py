# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import RPi.GPIO as GPIO
from adafruit_motor import servo		#adafruit servo controll lib
from adafruit_pca9685 import PCA9685	#adafruit pca9685 controll lib

"""
def setPinConfig(EN, INA, INB):
	GPIO.setup(EN, GPIO.OUT)
	GPIO.setup(INA, GPIO.OUT)
	GPIO.setup(INB, GPIO.OUT)
	pwm = GPIO.PWM(EN, 100)
	pwm.start(0)
	return pwm

def setMotorControl(pwm, speed, stat):
	pwm.ChangeDutyCycle(speed)

	if stat == ON:
		GPIO.output(IN1, HIGH)
		GPIO.output(IN2, LOW)
	elif stat == OFF:
		GPIO.output(IN1, LOW)
		GPIO.output(IN2, LOW)

GPIO.setmode(GPIO.BCM)

L1 = setPinConfig(ENA, IN1, IN2)
# -- end --
"""
OPEN = 'OPEN'
CLOSE = 'CLOSE'

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
doorMotor = list(servo.Servo(pca.channels[range(0,5) + 10], min_pulse=600, max_pulse=2400))

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
	if state == OPEN:
		doorMotor[loc].angle = 1800
		time.sleep(3)
	elif state == CLOSE:
		doorMotor[loc].angle = 1200
	doorMotor[loc].angle = 1500

# =================== 로봇팔 동작 =====================

# pca 모듈 종료 함수
pca.deinit()
