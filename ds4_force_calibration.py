#!/usr/bin/env python3
"""
Вручную запрашивает feature report калибровки (ID 0x05) у DualShock 4
по Bluetooth через /dev/hidrawN. Чтение этого отчёта — то самое
действие, которое должно переключить контроллер из короткого
BT-режима (0x01, 10 байт) в полный (0x11, 78 байт, с IMU).

Использование:
    sudo python3 ds4_force_calibration.py /dev/hidraw3
"""
import sys
import fcntl
import array

REPORT_ID = 0x05
SIZE = 41  # DS4_FEATURE_REPORT_CALIBRATION_BT_SIZE

def HIDIOCGFEATURE(size):
    # _IOC(_IOC_READ|_IOC_WRITE, 'H', 0x07, size) для x86/x86_64
    return (3 << 30) | (0x48 << 8) | 0x07 | (size << 16)

def main():
    if len(sys.argv) != 2:
        print("Использование: sudo python3 ds4_force_calibration.py /dev/hidrawN")
        sys.exit(1)

    path = sys.argv[1]
    buf = array.array('B', [0] * SIZE)
    buf[0] = REPORT_ID

    try:
        with open(path, 'rb+', buffering=0) as fd:
            fcntl.ioctl(fd, HIDIOCGFEATURE(SIZE), buf, True)
    except OSError as e:
        print(f"ioctl не прошёл: {e}")
        print("Возможные причины: неверный путь, устройство не отвечает по BT,")
        print("либо контроллер не поддерживает этот feature report.")
        sys.exit(1)

    print("Успех. Полученные данные (hex):")
    print(buf.tobytes().hex())
    print("\nТеперь проверьте заново: sudo hexdump -C", path.replace('hidraw', 'hidraw'))
    print("Первый байт входящих отчётов должен стать 11 вместо 01.")

if __name__ == "__main__":
    main()