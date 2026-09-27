from evdev import InputDevice

device = InputDevice('/dev/input/event21')

for event in device.read_loop():
    print(event)