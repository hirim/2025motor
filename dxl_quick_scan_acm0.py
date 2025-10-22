# dxl_quick_scan_acm0.py
from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS

PORT = "/dev/ttyACM0"
BAUDS = [57600, 115200, 1000000]
PROTOCOLS = [1.0, 2.0]
CANDIDATE_IDS = list(range(0, 10)) + [10, 11, 30, 64, 100]  # 빠른 범위

def try_open(port, baud):
    ph = PortHandler(port)
    if not ph.openPort():
        return None
    if not ph.setBaudRate(baud):
        ph.closePort(); return None
    return ph

def scan():
    any_hit = False
    for baud in BAUDS:
        ph = try_open(PORT, baud)
        if not ph:
            continue
        for proto in PROTOCOLS:
            pk = PacketHandler(proto)
            for dxl_id in CANDIDATE_IDS:
                model, res, err = pk.ping(ph, dxl_id)
                if res == COMM_SUCCESS and err == 0:
                    any_hit = True
                    print(f"[FOUND] Port={PORT}  Baud={baud}  Proto={proto}  ID={dxl_id}  ModelNum={model}")
        ph.closePort()
    if not any_hit:
        print("모터 미검출: 전원/배선/TTL·RS-485/보레이트/프로토콜을 다시 확인하세요.")

if __name__ == "__main__":
    print("Scanning /dev/ttyACM0 ...")
    scan()
