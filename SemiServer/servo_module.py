import time
import board
from adafruit_motor import servo		#adafruit servo controll lib
from adafruit_pca9685 import PCA9685	#adafruit pca9685 controll lib


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
#armMotor 0 - LEFT = 180, RIGHT = 0
# 가장 하단의 수평축 서보모터
#armMotor 1 - FORWARD = 180 , BACKWARD = 0
# 수직축의 가장 하단 모터
#armMotor 2 - FORWARD = 160, BACKWARD = 0
# 수직축 중간 모터 - 프레임의 간섭이 있기 때문에 동작 입력은 160을 최대로 한다
#armMotor 3 - FORWARD = 180, BACKWARD = 0
# 수직축 상단 모터
#armMotor 4 - CCwise = 0, Clockwise = 180
#Horizontal : angle = 15, vertical = 115
# 집게 위상 모터 - 위상 특성상 수직 또는 수평만을 사용할 확률이 높아 특정해놓음
#armMotor 5 - FASTEN = 120, LOOSEN = 40
# 집게 모터 - 지나치게 높은 값은집게 구조 특성상 모터에 무리를 줌
armMotor = [servo.Servo(pca.channels[i], min_pulse=544, max_pulse=2400) for i in range(0,7)]
armMotor1 = [servo.Servo(pca.channels[i], min_pulse=415, max_pulse=2420) for i in range(0,6)]
# dootMotor - 설비의 문을 제어하는 서보모터가 연결되어있는 객체
#  - mg995 servo motor : 360 도 회전이 가능한 서보모터
# -90 ~ 90 / 0 = 정지 / 1 ~ 90 = 정방향 회전 / -90 ~ -1 = 역방향 회전
# 총 5개의 설비, 5개의 객체 / 0 : HMDS, 1 : SPIN, 2 : BAKE, 3 : DEVELOP, 4 : EXPOSURE
doorMotor = [servo.Servo(pca.channels[i+10], min_pulse=500, max_pulse=2600) for i in range(0,5)]


# 로봇팔 초기 구동 함수
# 기본적인 위상으로 초기화
def arm_init():
	armMotor[0].angle = 90
	time.sleep(0.2)
	armMotor[1].angle = 50
	time.sleep(0.2)
	armMotor[2].angle = 100
	time.sleep(0.2)
	armMotor[4].angle = 140
	time.sleep(0.2)
	armMotor[5].angle = 15
	time.sleep(0.2)
	armMotor[6].angle = 40
	time.sleep(0.2)
# 로봇팔 자동 제어 1단계 : 웨이퍼 스테이지
def servo_work(start_angle, end_angle, num):
	if start_angle < end_angle:
		fraction = start_angle
		while fraction <  end_angle:
			armMotor[num].angle = fraction
			fraction += 5
			time.sleep(0.1)
	else:
		fraction = start_angle
		while fraction > end_angle:
			armMotor[num].angle = fraction
			fraction -= 5
			time.sleep(0.1)

# fraction

def arm_phase1():
# 설비 문 제어
	armMotor[0].angle = 180
	time.sleep(0.2)
	armMotor[1].angle = 140
	time.sleep(0.2)
	armMotor[2].angle = 160
	time.sleep(0.2)
	armMotor[4].angle = 60
	time.sleep(0.2)
	armMotor[5].angle = 115
	time.sleep(0.2)
	armMotor[6].angle = 120
	time.sleep(0.2)
	armMotor[1].angle = 50
	time.sleep(0.2)
	armMotor[2].angle = 90
	time.sleep(0.2)
	armMotor[4].angle = 110
	time.sleep(0.2)
	armMotor[5].angle = 15
	time.sleep(0.2)

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


# =================== 로봇팔 동작 =====================
arm_init()
time.sleep(1)
armMotor1[0].angle = 180
time.sleep(1)
armMotor[5].angle = 115
time.sleep(1)
armMotor[2].angle = 70
time.sleep(1)
armMotor[4].angle = 55
time.sleep(1)
servo_work(50,165,1)
time.sleep(1)
armMotor[6].angle = 140 #종이여서 꽉물었어
time.sleep(1)
armMotor[4].angle = 90
time.sleep(1)
servo_work(165,90,1)
time.sleep(1)

# pca 모듈 종료 함수
