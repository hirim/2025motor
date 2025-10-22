# dxl_keyboard_control.py
from dynamixel_sdk import *
import sys, tty, termios, ctypes

PORT = "/dev/ttyACM0"
BAUDS = [57600, 1000000]
PROTOCOLS = [1.0, 2.0]
CANDIDATE_IDS = [1, 0, 2, 3]

def s32(val): return ctypes.c_int32(val).value & 0xFFFFFFFF

P1_ADDR_TORQUE_ENABLE = 24
P1_ADDR_MOVING_SPEED  = 32
P2_ADDR_TORQUE_ENABLE = 64
P2_ADDR_OPERATING_MODE= 11
P2_ADDR_GOAL_VELOCITY = 104

def getch():
    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
    try:
        tty.setraw(fd); ch=sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def try_open(port, baud):
    ph = PortHandler(port)
    if not ph.openPort(): return None
    if not ph.setBaudRate(baud): ph.closePort(); return None
    return ph

def find_motor():
    for proto in PROTOCOLS:
        for baud in BAUDS:
            ph = try_open(PORT, baud)
            if not ph: continue
            pk = PacketHandler(proto)
            for dxl_id in CANDIDATE_IDS:
                model, res, err = pk.ping(ph, dxl_id)
                if res == COMM_SUCCESS and err == 0:
                    return ph, pk, proto, baud, dxl_id, model
            ph.closePort()
    return None, None, None, None, None, None

def main():
    ph, pk, proto, baud, dxl_id, model = find_motor()
    if not ph:
        print("모터를 찾지 못했습니다. 전원/포트/보레이트를 확인하세요.")
        return
    print(f"연결됨: Proto={proto}, Baud={baud}, ID={dxl_id}, Model={model}")

    if proto == 2.0:
        pk.write1ByteTxRx(ph, dxl_id, P2_ADDR_TORQUE_ENABLE, 0)
        pk.write1ByteTxRx(ph, dxl_id, P2_ADDR_OPERATING_MODE, 11)
        pk.write1ByteTxRx(ph, dxl_id, P2_ADDR_TORQUE_ENABLE, 1)
    else:
        pk.write1ByteTxRx(ph, dxl_id, P1_ADDR_TORQUE_ENABLE, 1)

    print("[w]전진 [x]후진 [s]정지 [q]종료")
    try:
        while True:
            k = getch()
            if k == 'w':
                if proto == 1.0:
                    pk.write2ByteTxRx(ph, dxl_id, P1_ADDR_MOVING_SPEED, 300)
                else:
                    pk.write4ByteTxRx(ph, dxl_id, P2_ADDR_GOAL_VELOCITY, s32(+100))
                print("전진")
            elif k == 'x':
                if proto == 1.0:
                    pk.write2ByteTxRx(ph, dxl_id, P1_ADDR_MOVING_SPEED, 1024+300)
                else:
                    pk.write4ByteTxRx(ph, dxl_id, P2_ADDR_GOAL_VELOCITY, s32(-100))
                print("후진")
            elif k == 's':
                if proto == 1.0:
                    pk.write2ByteTxRx(ph, dxl_id, P1_ADDR_MOVING_SPEED, 0)
                else:
                    pk.write4ByteTxRx(ph, dxl_id, P2_ADDR_GOAL_VELOCITY, 0)
                print("정지")
            elif k == 'q':
                print("종료"); break
    finally:
        if proto == 1.0:
            pk.write1ByteTxRx(ph, dxl_id, P1_ADDR_TORQUE_ENABLE, 0)
        else:
            pk.write1ByteTxRx(ph, dxl_id, P2_ADDR_TORQUE_ENABLE, 0)
        ph.closePort()

if __name__ == "__main__":
    main()
