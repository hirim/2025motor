# dynamixel_wxs_control.py
from dynamixel_sdk import *
import time
import sys
import termios
import tty

# 장치 설정
DEVICENAME = '/dev/ttyUSB0'   # 라즈베리파이 포트 이름 확인 (예: /dev/ttyUSB0)
BAUDRATE = 57600
DXL_ID = 1
PROTOCOL_VERSION = 1.0        # 모델에 따라 다름 (XM 시리즈는 2.0)

# 제어 테이블 주소 (AX-12A 예시)
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_SPEED = 32
ADDR_MX_MOVING_SPEED = 32
ADDR_MX_PRESENT_SPEED = 38

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 10

# 포트와 패킷 핸들러 초기화
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 포트 열기
if not portHandler.openPort():
    print("포트를 열 수 없습니다.")
    quit()

# 통신 속도 설정
if not portHandler.setBaudRate(BAUDRATE):
    print("통신 속도를 설정할 수 없습니다.")
    quit()

# 토크 활성화
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)

# 입력 함수 (키보드 입력)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

print("다이나믹셀 제어 시작")
print("[w] 전진, [x] 후진, [s] 정지/종료")

try:
    while True:
        key = getch()
        if key == 'w':
            # 전진
            speed = 200  # 양수 속도
            packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_MOVING_SPEED, speed)
            print("전진 중...")
        elif key == 'x':
            # 후진
            speed = 1024 + 200  # 방향비트 설정 (10bit: 방향, 10bit: 속도)
            packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_MOVING_SPEED, speed)
            print("후진 중...")
        elif key == 's':
            # 정지 및 종료
            packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_MOVING_SPEED, 0)
            print("정지합니다.")
            break
        else:
            print("유효하지 않은 입력입니다.")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# 토크 비활성화 및 포트 종료
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("프로그램 종료.")
