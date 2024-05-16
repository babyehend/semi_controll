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
armMotor1 = [servo.Servo(pca.channels[i], min_pulse=415, max_pulse=2430) for i in range(0,6)]
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
	armMotor[5].angle = 87
	time.sleep(0.2)
	armMotor[6].angle = 100
	time.sleep(0.2)
# 로봇팔 자동 제어 1단계 : 웨이퍼 스테이지
def servo_work(start_angle, end_angle, num):
	if start_angle < end_angle:
		fraction = start_angle
		while fraction <  end_angle:
			armMotor[num].angle = fraction
			fraction += 2
			time.sleep(0.1)
	else:
		fraction = start_angle
		while fraction > end_angle:
			armMotor[num].angle = fraction
			fraction -= 2
			time.sleep(0.1)

# fraction

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

# ------------------------ 로봇팔 단계별 동작 함수 ----------------------------
# pass 를 지우고 그 자리에 해당 동작에 대한 함수를 붙여 넣는다.

# def stage_in():
# 	# 모든 공정이 끝난후 웨이퍼를 웨이퍼 스테이지 다시 넣는 부분
# 	pass

def stage_out():
	arm_init()
	time.sleep(1)
	armMotor1[0].angle = 179
	time.sleep(1)
	armMotor1[5].angle = 5
	time.sleep(1)
	servo_work(50,110,1)
	time.sleep(1)
	armMotor[2].angle = 50
	time.sleep(1)
	armMotor[4].angle = 50
	time.sleep(1)
	servo_work(110,170,1)
	time.sleep(1)
	armMotor[1].angle = 172
	time.sleep(1)
	armMotor[6].angle = 150
	time.sleep(1)

	#init부분에서 가져오는 부분
	armMotor[4].angle = 20
	time.sleep(1)
	servo_work(55,10,2)
	time.sleep(1)
	servo_work(20,0,4)
	time.sleep(1)
	servo_work(10,0,2)
	time.sleep(1)
	servo_work(165,90,1)
	time.sleep(1)
	servo_work(30,90,2)
	time.sleep(1)
	# 여기까지가 웨이퍼 캐리어에서 가져옴 

	armMotor[2].angle = 40
	time.sleep(1)
	armMotor[0].angle = 90
	time.sleep(1)
	armMotor[4].angle = 90
	time.sleep(1)
	# 서있는 모습
	servo_work(90,40,1)
	time.sleep(1)
	servo_work(40,70,2)
	time.sleep(1)
	servo_work(90,120,4)
	time.sleep(1)
	servo_work(40,15,1)
	time.sleep(1)
	servo_work(70,125,2)
	time.sleep(1)
	servo_work(120,150,4)
	time.sleep(1)
	armMotor[5].angle = 87
	time.sleep(0.5)
	# --------------- stage out 끝 -----------------------

def hmds_in():
	# 웨이퍼를 가진 상태에서 hmds로 이동, 
	# 문을 열고 hmds 덱 위에 웨이퍼를 두고 나와 문을 닫는 부분
	armMotor[0].angle = 90
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	armMotor[6].angle = 150
	time.sleep(0.5)

	# 여기까지
	# HMDS 들어가기위한 각도 맞추기 
	armMotor[0].angle = 162
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	armMotor[2].angle = 115
	time.sleep(0.5)
	armMotor[1].angle = 30
	time.sleep(0.5)

	#전진 
	for i in range(20):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[4].angle += 4
	time.sleep(0.2)
	for i in range(8):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[4].angle -= 5
	time.sleep(0.2)
	for i in range(8):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[0].angle -= 3
	time.sleep(0.2)
	armMotor[4].angle -= 3
	time.sleep(0.2)

	for i in range(6):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)
	armMotor[4].angle -= 5
	time.sleep(1)

	for i in range(6):
		armMotor[1].angle += 1.8
		time.sleep(0.2)
		armMotor[2].angle -= 1.4
		time.sleep(0.2)

	armMotor[0].angle -= 4
	time.sleep(0.2)

	for i in range(6):
		armMotor[1].angle += 1.8
		time.sleep(0.2)
		armMotor[2].angle -= 1.4
		time.sleep(0.2)

	armMotor[1].angle += 5

	for i in range(20):
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[4].angle +=  5

	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1.4
		time.sleep(0.2)

	armMotor[4].angle += 5
	time.sleep(0.5)

	armMotor[0].angle -= 2
	time.sleep(0.5)
	for i in range(10):
		armMotor[1].angle += 1
		time.sleep(0.5)
		armMotor[2].angle -= 1
		time.sleep(0.5)

	for i in range(10):
		armMotor[1].angle += 1
		time.sleep(0.5)
		armMotor[2].angle -= 1
		time.sleep(0.5)

	armMotor[6].angle = 80
	time.sleep(0.5)

	# 빠꾸
	for i in range(10):
		armMotor[4].angle += 1
		time.sleep(0.2)

	for i in range(20):
		armMotor[4].angle += 1
		time.sleep(0.2)
		armMotor[1].angle -= 0.5
		time.sleep(0.2)

	for i in range(20):
		armMotor[4].angle += 1
		time.sleep(0.2)
		armMotor[1].angle -= 1
		time.sleep(0.2)
	# 웨이퍼 넣고 로봇팔 빠지기 까지 
	# HMDS 여기까지 

def hmds_out():
	# hmds 공정이 종료된후, 문을 열고 웨이퍼를 가지고 나와 문을 다시 닫는 부분
	# 이후는 HMDS 꺼내기
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,107,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,60,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,108,1)
	time.sleep(0.5)
	armMotor[6].angle = 100
	time.sleep(0.5)
	for i in range(25):
		armMotor[2].angle -= 1.4
		if armMotor[2].angle < 0:
			armMotor[2].angle = 0
		time.sleep(0.2)
		if i == 15:
			armMotor[0].angle = 150
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[0].angle = 152
	time.sleep(0.5)
	armMotor[1].angle = 108
	time.sleep(0.5)
	armMotor[2].angle = 60
	time.sleep(0.5)
	armMotor[4].angle = 107
	time.sleep(0.5)

	for i in range(20):
		armMotor[4].angle += 1
		time.sleep(0.2)
		armMotor[1].angle -= 0.5
		time.sleep(0.2)


	for i in range(40):
		if armMotor[2].angle <= 106:
			armMotor[2].angle += 2
			time.sleep(0.2)
		armMotor[1].angle -= 1
		time.sleep(0.2)
	#꺼냄
	#공정전 init
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,110,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)

def spin_in():
	# 웨이퍼를 가진 상태에서 spin coating 으로 이동, 
	# 문을 열고 덱 위에 웨이퍼를 두고 나와 문을 닫는 부분
	#Spin Coating
	#전진 
	armMotor[0].angle = 112
	time.sleep(0.5)

	for i in range(16):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)


	for i in range(30):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[4].angle -= 3
	time.sleep(0.5)


	for i in range(10):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	for i in range(7):
		armMotor[2].angle += 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)
	armMotor[4].angle -= 3
	time.sleep(1)

	for i in range(13):
		armMotor[2].angle -= 1.5
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[6].angle = 90
	# 놓기 까지
	# 로봇팔 퇴장 
	armMotor[1].angle -= 1
	time.sleep(0.2)
	armMotor[2].angle += 1
	time.sleep(0.2)

	for i in range(16):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		armMotor[1].angle -= 1.5
		time.sleep(0.2)

def spin_out():
	# spin coating 공정이 끝난 후, 
	# 문을 열고 덱 위에 웨이퍼를 들고 나와 문을 닫는 부분
	#spincoating에서 로봇팔이 빠지는 위치
	armMotor[6].angle = 90
	time.sleep(0.2)
	armMotor[0].angle = 112
	time.sleep(0.2)
	armMotor[5].angle = 87
	time.sleep(0.5)
	armMotor[1].angle = 100
	time.sleep(0.2)
	armMotor[2].angle = 51
	time.sleep(0.2)
	armMotor[4].angle = 129
	time.sleep(0.2)
	time.sleep(3)

	armMotor[2].angle += 8
	time.sleep(0.2)
	armMotor[1].angle += 6 
	time.sleep(0.2)

	for i in range(7):
		armMotor[4].angle -= 5 
		time.sleep(0.2)
		armMotor[1].angle += 3 
		time.sleep(0.2)

	armMotor[2].angle -= 4
	time.sleep(0.2)
	armMotor[4].angle -= 4
	time.sleep(0.2)
	armMotor[1].angle += 4
	time.sleep(0.2)
	armMotor[2].angle -= 4
	time.sleep(0.2)
	armMotor[4].angle += 4
	time.sleep(0.2)
	armMotor[6].angle = 150
	time.sleep(0.2)
	#집기 성공

	for i in range(20):
		armMotor[1].angle -= 3 
		time.sleep(0.2)
		if (armMotor[4].angle + 5 < 180):
			armMotor[4].angle += 5 
		time.sleep(0.2)

	servo_work(72,40,1)

	#다시 init
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,70,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,90,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)

def bake_in():
	# 웨이퍼를 가진 상태에서 bake 로 이동, 
	# 문을 열고 덱 위에 웨이퍼를 두고 나와 문을 닫는 부분
	# Bake	
	#전진 
	armMotor[0].angle = 65
	time.sleep(0.2)
	for i in range(20):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(30):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[4].angle -= 3
	time.sleep(0.5)

	for i in range(10):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	for i in range(7):
		armMotor[2].angle += 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)
	armMotor[4].angle -= 3
	time.sleep(1)

	for i in range(13):
		armMotor[2].angle -= 1.5
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[6].angle = 90 #장소도착 집게 벌리기

	armMotor[1].angle -= 1
	time.sleep(0.2)
	armMotor[2].angle += 1
	time.sleep(0.2)

	for i in range(16):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		armMotor[1].angle -= 1.5
		time.sleep(0.2)
	#이 이후로 퇴장 
	
def bake_out():
	# bake 공정이 끝난 후, 
	# 문을 열고 덱 위에 웨이퍼를 들고 나와 문을 닫는 부분
	armMotor[2].angle += 6 
	time.sleep(0.2)
	armMotor[1].angle += 6 
	time.sleep(0.2)

	for i in range(8):
		armMotor[4].angle -= 5 
		time.sleep(0.2)
		armMotor[1].angle += 3 
		time.sleep(0.2)

	armMotor[6].angle = 150
	time.sleep(0.2)
	#집기 성공
	for i in range(18): 
		armMotor[1].angle -= 3 
		time.sleep(0.2)
		armMotor[4].angle += 5 
		time.sleep(0.2)

	servo_work(72,40,1)

	# 다시 init
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,70,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,90,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)

def develop_in():
	# 웨이퍼를 가진 상태에서 develop 로 이동, 
	# 문을 열고 덱 위에 웨이퍼를 두고 나와 문을 닫는 부분
	#develop
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,70,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,90,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)

	armMotor[0].angle = 28
	time.sleep(0.2)
	armMotor[4].angle += 3
	time.sleep(0.2)
	#전진 
	for i in range(20):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[4].angle -= 2
	time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[4].angle -= 2
	time.sleep(0.2)
	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)
	##########################################

	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)


	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(30):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(8):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	armMotor[6].angle = 90
	#여기까지 로봇팔 넣어주기 
	# 여기까지 웨이퍼 가져다 놓음 
	# 로봇팔 잠시 퇴장  
	armMotor[1].angle -= 1
	time.sleep(0.2)
	armMotor[2].angle += 1
	time.sleep(0.2)
		
	for i in range(30):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		armMotor[1].angle -= 1.3
		time.sleep(0.2)

def develop_out():
	# develop 공정이 끝난 후, 
	# 문을 열고 덱 위에 웨이퍼를 들고 나와 문을 닫는 부분
	# 로봇팔 가지로 가기 
	armMotor[0].angle = 28
	time.sleep(0.2)
	armMotor[1].angle = 92
	time.sleep(0.2)
	armMotor[2].angle = 75
	time.sleep(0.2)
	armMotor[4].angle = 118
	time.sleep(0.2)

	for i in range(30):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[4].angle -= 4
	time.sleep(0.2)
	armMotor[6].angle = 150
	time.sleep(0.2)

	for i in range(90):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		armMotor[1].angle -= 1.3
		time.sleep(0.2)

	# 들어가서 다시 잡는거 다시 만들기 
	#다시 init
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,70,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,90,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)
	armMotor[1].angle = 15
	time.sleep(0.2)
	armMotor[2].angle = 125
	time.sleep(0.2)
	time.sleep(0.2)
	armMotor[5].angle = 87
	time.sleep(0.2)
	armMotor[6].angle = 150
	time.sleep(0.2)

def exposure_in():
	# 웨이퍼를 가진 상태에서 exposure 로 이동, 
	# 문을 열고 덱 위에 웨이퍼를 두고 나와 문을 닫는 부분
	armMotor1[0].angle = 0
	time.sleep(0.5)
	
	for i in range(20):
		armMotor[2].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1
		time.sleep(0.2)
		armMotor[4].angle -= 1
		time.sleep(0.2)
		armMotor[1].angle += 1
		time.sleep(0.2)

	for i in range(30):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[4].angle -= 3
	time.sleep(0.5)

	for i in range(10):
		armMotor[2].angle -= 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)



	for i in range(7):
		armMotor[2].angle += 1.4
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)
	armMotor[4].angle -= 3
	time.sleep(1)

	for i in range(13):
		armMotor[2].angle -= 1.5
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	for i in range(15):
		armMotor[2].angle -= 1.5
		time.sleep(0.2)
		armMotor[1].angle += 1.5
		time.sleep(0.2)

	armMotor[6].angle = 90
	time.sleep(0.2)
	#여기서 로봇팔 두고 잠시 퇴장 

	armMotor[4].angle -= 4
	time.sleep(0.2)
	for i in range(20):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		if i == 10:
			armMotor[2].angle += 2
		armMotor[1].angle -= 1.5
		time.sleep(0.2)

def exposure_out():
	# exposure 공정이 끝난 후, 
	# 문을 열고 덱 위에 웨이퍼를 들고 나와 문을 닫는 부분
	armMotor[6].angle = 90
	time.sleep(0.2)
	armMotor[1].angle = 111
	time.sleep(0.2)
	armMotor[2].angle = 31
	time.sleep(0.2)
	armMotor[4].angle = 129
	time.sleep(0.2)
	armMotor[5].angle = 87
	time.sleep(0.5)


	armMotor[4].angle -= 4
	for i in range(12):
		armMotor[1].angle += 1
		time.sleep(0.2)
		armMotor[2].angle += 1
		time.sleep(0.2)
	armMotor[4].angle += 4
	time.sleep(0.2)

	for i in range(20):
		armMotor[1].angle += 1
		time.sleep(0.2)
		armMotor[2].angle -= 1
		time.sleep(0.2)

	armMotor[2].angle -= 2
	time.sleep(0.2)
	armMotor[1].angle += 4
	time.sleep(0.2)
	armMotor[2].angle -= 2
	time.sleep(0.2)
	armMotor[1].angle += 4
	time.sleep(0.2)
	armMotor[6].angle = 150
	time.sleep(0.2)
	armMotor[4].angle -= 4
	time.sleep(0.2)
	for i in range(30):
		armMotor[2].angle += 2
		time.sleep(0.2)
		armMotor[1].angle -= 1.5
		time.sleep(0.2)

	for i in range(10):
		armMotor[2].angle += 1.5
		time.sleep(0.2)
		armMotor[1].angle -= 1.5
		time.sleep(0.2)

	for i in range(15):
		armMotor[2].angle += 2
		time.sleep(0.2)
		armMotor[1].angle -= 1.5
		time.sleep(0.2)

	#다시 init
	armMotor[6].angle = 150
	time.sleep(0.5)
	armMotor[5].angle = 87
	time.sleep(0.5)
	servo_work(armMotor[4].angle,70,4)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,90,2)
	time.sleep(0.5)
	servo_work(armMotor[1].angle,15,1)
	time.sleep(0.5)
	servo_work(armMotor[2].angle,125,2)
	time.sleep(0.5)
	servo_work(armMotor[4].angle,150,4)
	time.sleep(0.5)
	armMotor[1].angle = 15
	time.sleep(0.2)
	armMotor[2].angle = 125
	time.sleep(0.2)
	time.sleep(0.2)
	armMotor[5].angle = 87
	time.sleep(0.2)
	armMotor[6].angle = 150
	time.sleep(0.2)



# =================== 로봇팔 동작 =====================
# 처음 로봇팔 동작
#웨이퍼 스테이지
