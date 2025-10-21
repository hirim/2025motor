import sys
import tty
import termios
from dynamixel_sdk import *

# ========================
# 1. 설정
# ========================
DXL_ID_LEFT = 1
DXL_ID_RIGHT = 2

PORT_NAME = '/dev/ttyACM0'  # 변경된 포트
BAUDRATE = 57600
MAX_SPEED = 200  # 속도 단위

# ========================
# 2. 초기화
# ========================
portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(2.0)  # Protocol 2.0

if not portHandler.openPort():
    print("포트 열기 실패")
    sys.exit()

if not portHandler.setBaudRate(BAUDRATE):
    print("보드레이트 설정 실패")
    sys.exit()

# ========================
# 3. 모터 모드 초기화 (Wheel 모드)
# ========================
for dxl_id in [DXL_ID_LEFT, DXL_ID_RIGHT]:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, 11, 1)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"모터 {dxl_id} 모드 설정 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
