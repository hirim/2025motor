#!/usr/bin/env python3
import os
import subprocess
from dynamixel_sdk import *

PORT_NAME = '/dev/ttyACM0'
BAUDRATES = [57600, 1000000]

def check_port():
    print("🔍 [1] 포트 확인 중...")
    result = subprocess.getoutput("ls /dev/ttyACM* 2>/dev/null")
    if PORT_NAME not in result:
        print("❌ OpenCR 포트가 감지되지 않았습니다.")
        print("👉 USB 케이블 및 전원 연결을 확인하세요.")
        return False
    print(f"✅ 포트 확인 완료: {PORT_NAME}")
    return True

def check_permissions():
    print("\n🔍 [2] 포트 권한 확인 중...")
    user = subprocess.getoutput("whoami").strip()
    groups = subprocess.getoutput(f"groups {user}")
    if "dialout" not in groups:
        print("⚠️ 현재 사용자가 dialout 그룹에 없습니다.")
        print(f"👉 아래 명령을 실행하고 재로그인하세요:\n   sudo usermod -a -G dialout {user}")
        return False
    print("✅ dialout 그룹 권한 정상")
    return True

def try_ping():
    print("\n🔍 [3] 다이나믹셀 통신 테스트 중...")
    for baud in BAUDRATES:
        print(f"⏱ 보드레이트 {baud} 테스트 중...")
        portHandler = PortHandler(PORT_NAME)
        packetHandler = PacketHandler(2.0)
        if not portHandler.openPort():
            print("❌ 포트를 열 수 없습니다.")
            continue
        if not portHandler.setBaudRate(baud):
            print(f"❌ 보드레이트 {baud} 설정 실패")
            portHandler.closePort()
            continue

        found = False
        for dxl_id in range(1, 10):
            dxl_model, dxl_comm, dxl_error = packetHandler.ping(portHandler, dxl_id)
            if dxl_comm == COMM_SUCCESS and dxl_error == 0:
                print(f"✅ 모터 발견: ID={dxl_id}, 모델번호={dxl_model}, 보드레이트={baud}")
                found = True
        portHandler.closePort()

        if found:
            return True

    print("❌ 다이나믹셀 통신 실패")
    print("👉 점검 사항:")
    print("   1. 다이나믹셀 전원(12V) 연결 확인")
    print("   2. OpenCR DYNAMIXEL 포트 연결 상태 확인")
    print("   3. 케이블 방향 및 ID 설정 확인")
    return False

def main():
    print("=== 🔧 OpenCR + 다이나믹셀 자동 점검 시작 ===\n")
    if not check_port(): return
    check_permissions()
    try_ping()
    print("\n=== ✅ 점검 완료 ===")

if __name__ == "__main__":
    main()
