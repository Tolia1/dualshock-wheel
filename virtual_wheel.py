from evdev import UInput, AbsInfo, ecodes


capabilities = {
    ecodes.EV_ABS: {
        ecodes.ABS_X: AbsInfo(
            value=0,
            min=-32768,
            max=32767,
            fuzz=0,
            flat=0,
            resolution=0
        )
    }
}


ui = UInput(
    capabilities,
    name="My Virtual Steering Wheel",
    version=1
)

print("Virtual wheel created.")
print("Device:", ui.device)
print("Press Ctrl+C to exit.")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nClosing virtual wheel.")

ui.close()