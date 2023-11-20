from serial import SerialException
from speed_regulator import SpeedRegulator
from vesc_controller import MotorVESC, DummyVESC
from simple_display import SliderWindow
import asyncio

PORT = "COM3"
ACC_LIM = 250

async def main():
    motor = MotorVESC(PORT)
    # motor = DummyVESC(PORT)

    #try:
    motor.connect()
    #
    # except SerialException:
    #    print(f"Unable to connect to port {PORT}")
    #    return

    slider = SliderWindow()
    regulator = SpeedRegulator(motor, slider, ACC_LIM)

    asyncio.create_task(regulator.start())
    await asyncio.create_task(slider.run())

    motor.close()


if __name__ == "__main__":
    asyncio.run(main())