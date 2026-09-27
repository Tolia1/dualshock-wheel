from evdev import InputDevice, ecodes

DEVICE_PATH = '/dev/input/event21'  # при необходимости подставьте актуальный номер

# ABS_X/Y/Z — акселерометр (диапазон ±32768)
# ABS_RX/RY/RZ — гироскоп (диапазон ±2097152)
AXES = {
    ecodes.ABS_X:  'Accel X',
    ecodes.ABS_Y:  'Accel Y',
    ecodes.ABS_Z:  'Accel Z',
    ecodes.ABS_RX: 'Gyro X ',
    ecodes.ABS_RY: 'Gyro Y ',
    ecodes.ABS_RZ: 'Gyro Z ',
}


def main():
    device = InputDevice(DEVICE_PATH)
    print(f"Слушаю: {device.path} ({device.name})")
    print("Ctrl+C для выхода\n")

    values = {code: 0 for code in AXES}

    try:
        for event in device.read_loop():
            if event.type != ecodes.EV_ABS or event.code not in AXES:
                continue

            values[event.code] = event.value

            line = "  ".join(
                f"{name}: {values[code]:>8}" for code, name in AXES.items()
            )
            print(f"\r{line}", end="", flush=True)

    except KeyboardInterrupt:
        print("\n\nОстановлено.")


if __name__ == '__main__':
    main()