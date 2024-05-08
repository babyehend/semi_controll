import time
import serial

sector = {'HMDS' : 'A', 'SPIN' : 'B', 'DEVELOP' : 'C', 'EXPOSURE' : 'D'}
device = {'DEV1' : '1', 'DEV2' : '2', 'DEV3' : '3'}

# 시리얼 포트와 Baud rate 설정
serial_port = '/dev/ttyAMA2'  # Atmega128A의 시리얼 포트
baud_rate = 9600  # Atmega128A와 동일한 Baud rate로 설정

# 시리얼 통신 연결 설정
ser = serial.Serial(port=serial_port, baudrate=baud_rate,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=0)

def get_data():
    try:
        while True:
            # Atmega128A로부터 데이터 수신
            received_data = ser.readline().decode().strip()
            if received_data  : print("Received:", received_data)

    except KeyboardInterrupt:
        # Ctrl+C를 누르면 프로그램 종료
        print("Serial connection closed.")

def put_data(sect, dev):
    try:
        print("Try Sending")
        if sect in list(sector.keys()):
            ser.write(sector[sect], encoding='ascii')
            ser.write(device[dev], encoding='ascii')

    except KeyboardInterrupt:
        # Ctrl+C를 누르면 프로그램 종료
        print("Serial connection closed.")

put_data()
