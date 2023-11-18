from motor_controls import MotorController
from simple_display import SliderWindow
import asyncio

async def main():
    slider = SliderWindow()
    motor = MotorController(slider, 300)

    motor_task = asyncio.create_task(motor.start())
    slider_task = asyncio.create_task(slider.run())

    await slider_task



if __name__ == "__main__":
    asyncio.run(main())