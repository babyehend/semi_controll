import time
import serial

# 시리얼 포트와 Baud rate 설정
serial_port = '/dev/ttyAMA3'  # Atmega128A의 시리얼 포트
baud_rate = 9600  # Atmega128A와 동일한 Baud rate로 설정

# 시리얼 통신 연결 설정
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def get_data():
    ser.is_open()
    try:
        while True:
            # Atmega128A로부터 데이터 수신
            received_data = ser.readline().decode().strip()
            print("Received:", received_data)

    except KeyboardInterrupt:
        # Ctrl+C를 누르면 프로그램 종료
        ser.close()
        print("Serial connection closed.")

def put_data():
    ser.is_open()
    try:
        while True:
            # Atmega128A로부터 데이터 수신
            send_data = ser.write(b'Hello')
            print("Send:", send_data)

    except KeyboardInterrupt:
        # Ctrl+C를 누르면 프로그램 종료
        ser.close()
        print("Serial connection closed.")

get_data()
time.sleep(1)
put_data()