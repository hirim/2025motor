# dxl_ping_debug.py
from dynamixel_sdk import PortHandler, PacketHandler, COMM_SUCCESS
import sys

PORT = "/dev/ttyACM0"  # 필요하면 /dev/ttyUSB0 로 바꿔서 테스트
BAUDS = [57600, 115200, 1000000, 2000000]
PROTOS = [1.0, 2.0]
IDS = list(range(0, 12)) + [30, 64, 100]

def try_open(port, baud):
    ph = PortHandler(port)
    if not ph.openPort():
        print(f"[OPEN FAIL] port={port}")
        return None
    if not ph.setBaudRate(baud):
        print(f"[BAUD FAIL]  port={port}, baud={baud}")
        ph.closePort()
        return None
    return ph

def main():
    any_hit = False
    for baud in BAUDS:
        ph = try_open(PORT, baud)
        if not ph:
            continue
        for proto in PROTOS:
            pk = PacketHandler(proto)
            print(f"\n=== Try proto={proto}, baud={baud} ===")
            for dxl_id in IDS:
                model, res, err = pk.ping(ph, dxl_id)
                if res == COMM_SUCCESS and err == 0:
                    print(f"[FOUND] ID={dxl_id}  ModelNum={model}")
                    any_hit = True
                else:
                    # 실패 이유를 텍스트로 출력
                    res_txt = pk.getTxRxResult(res)
                    err_txt = pk.getRxPacketError(err)
                    print(f"  id={dxl_id} -> res='{res_txt}', err='{err_txt}'")
        ph.closePort()

    if not any_hit:
        print("\n[NO DETECTION]")
        print("- 전원/배선(TTL vs RS-485)/케이블/포트 권한을 다시 확인하세요.")
        print("- 모터 모델의 기본 보레이트/프로토콜 후보를 늘려 시도하세요.")
        print("- 단일 모터만 연결하고 테스트 (ID 충돌 방지).")

if __name__ == "__main__":
    main()
