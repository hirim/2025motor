from dynamixel_sdk import *

PORT_NAME = '/dev/ttyACM0'
BAUDRATE = 57600

portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(2.0)

if not portHandler.openPort():
    print("포트 열기 실패")
if not portHandler.setBaudRate(BAUDRATE):
    print("보드레이트 설정 실패")

dxl_id = 1  # 테스트할 모터 ID
dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, dxl_id)
print(dxl_comm_result, dxl_error, dxl_model_number)
