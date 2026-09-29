from evdev import InputDevice, ecodes

DEVICE_PATH = '/dev/input/event21'  # при необходимости подставьте актуальный номер

# ABS_X/Y/Z — акселерометр (диапазон ±32768)
# ABS_RX/RY/RZ — гироскоп (диапазон ±2097152)
AXES = {
    ecodes.ABS_X:  'Accel X',
    ecodes.ABS_RX: 'Gyro X '
}


def main():
    device = InputDevice(DEVICE_PATH)

    for code, name in AXES.items():
        info = device.absinfo(code)
        print(
            f"{name}: "
            f"value={info.value}, "
            f"min={info.min}, "
            f"max={info.max}, "
            f"fuzz={info.fuzz}, "
            f"resolution={info.resolution}"
        )
    
    print(f"Слушаю: {device.path} ({device.name})")
    print("Ctrl+C для выхода\n")

    previous_x = None
    steering_x = 0

    current_x = 0
    current_acs = 0

    try:
        for event in device.read_loop():
            if event.type != ecodes.EV_ABS or event.code not in AXES:
                continue

            if event.code == ecodes.ABS_X:
                current_x = event.value

            elif event.code == ecodes.ABS_RX:
                current_acs = event.value

            # Первое значение используем только для инициализации
            if previous_x is None:
                previous_x = current_x
                continue

            # Абсолютная величина изменения
            delta = abs(current_x - previous_x)

            steering_x += delta * (1 if current_acs >= 0 else -1)

            print(
                f"\rAccel X: {current_x:>8}  "
                f"Gyro X: {current_acs:>8}"
                f"Streering X: {steering_x:>8}",
                end="",
                flush=True
            )

            previous_x = current_x

    except KeyboardInterrupt:
        print("\n\nОстановлено.")


if __name__ == '__main__':
    main()