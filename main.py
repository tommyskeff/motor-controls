from serial import SerialException
from speed_regulator import SpeedRegulator
from vesc_controller import MotorVESC, DummyVESC
from simple_display import SliderWindow
import asyncio

ACC_LIM = 250

async def main():
    f = open("device", "r")
    port = f.readline()
    f.close()

    print(f"Connecting to {port}")

    motor = MotorVESC(port)
    # motor = DummyVESC(PORT)

    try:
        motor.connect()
    except SerialException as e:
       print(f"Unable to connect to port {port}")
       print(e)
       return

    slider = SliderWindow()
    regulator = SpeedRegulator(motor, slider, ACC_LIM)

    asyncio.create_task(regulator.start())
    await asyncio.create_task(slider.run())

    motor.close()


if __name__ == "__main__":
    asyncio.run(main())