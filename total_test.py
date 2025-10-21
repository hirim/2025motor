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
    if "dialout" not in gro
