import sys
import tty
import termios
from dynamixel_sdk import *

# ========================
# 1. 설정
# ========================
# 다이나믹셀 ID
DXL_ID_LEFT = 1
DXL_ID_RIGHT = 2

# 포트와 보드레이트
PORT_NAME = '/dev/ttyUSB0'
BAUDRATE = 57600

# 최대 속도
MAX_SPEED = 200  # 단위: 다이나믹셀 속도 단위

# ========================
# 2. 초기화
# ========================
portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(2.0)  # Protocol 2.0 사용

if not portHandler.openPort():
    print("포트 열기 실패")
    sys.exit()

if not portHandler.setBaudRate(BAUDRATE):
    print("보드레이트 설정 실패")
    sys.exit()

# ========================
# 3. 모터 제어 함수
# ========================
def set_motor_speed(dxl_id, speed):
    # 속도 방향 처리: + = 전진, - = 후진
    speed_val = int(abs(speed))
    if speed < 0:
        speed_val |= 0x400  # 후진 방향 비트
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, dxl_id, 104, speed_val
    )
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# ========================
# 4. 키보드 입력 함수
# ========================
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# ========================
# 5. 메인 루프
# ========================
print("w: 전진, x: 후진, a: 좌회전, d: 우회전, s: 정지/종료")

try:
    while True:
        key = getch()
        if key == 'w':
            set_motor_speed(DXL_ID_LEFT, MAX_SPEED)
            set_motor_speed(DXL_ID_RIGHT, MAX_SPEED)
        elif key == 'x':
            set_motor_speed(DXL_ID_LEFT, -MAX_SPEED)
            set_motor_speed(DXL_ID_RIGHT, -MAX_SPEED)
        elif key == 'a':
            set_motor_speed(DXL_ID_LEFT, -MAX_SPEED//2)
            set_motor_speed(DXL_ID_RIGHT, MAX_SPEED//2)
        elif key == 'd':
            set_motor_speed(DXL_ID_LEFT, MAX_SPEED//2)
            set_motor_speed(DXL_ID_RIGHT, -MAX_SPEED//2)
        elif key == 's':
            set_motor_speed(DXL_ID_LEFT, 0)
            set_motor_speed(DXL_ID_RIGHT, 0)
            print("프로그램 종료")
            break

except KeyboardInterrupt:
    set_motor_speed(DXL_ID_LEFT, 0)
    set_motor_speed(DXL_ID_RIGHT, 0)
    print("프로그램 종료")
