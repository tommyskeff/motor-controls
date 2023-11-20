import asyncio
import math
from simple_display import SliderWindow
from vesc_controller import MotorVESC

CYCLE_INTERVAL = 0.01
DISABLED_SPEED = 1000
MAXIMUM_SPEED = 10000
VAL_ZEROS = 2

zerosPower = math.pow(10, VAL_ZEROS)

class SpeedRegulator:

    def __init__(self, controller: MotorVESC, window: SliderWindow, acceleration_limit: float) -> None:
        self._controller = controller
        self._window = window
        self._running = False
        self._current_speed = DISABLED_SPEED
        self._speed_desired = DISABLED_SPEED
        self._potentiometer_reading = 0
        self._acceleration_limit = acceleration_limit

    async def start(self) -> None:
        self._running = True
        while self._running:
            self._cycle()
            await asyncio.sleep(CYCLE_INTERVAL)

    def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def _calculate_speed_increment(self):
        speed_desired = 1000 + self._potentiometer_reading * (MAXIMUM_SPEED - DISABLED_SPEED)
        speed_desired = speed_desired // zerosPower * zerosPower

        speed_difference = speed_desired - self._current_speed
        increment_speed = speed_difference / 1
        increment_speed = min(increment_speed, self._acceleration_limit)

        return increment_speed

    def _set_motor_speed(self, speed: int) -> None:
        self._current_speed = speed
        self._controller.set_speed(speed)
        self._window.set_text(f"RPM: {speed}")

    def _cycle(self) -> None:
        self._potentiometer_reading = self._window.get_slider_value()
        increment = self._calculate_speed_increment()
        current_speed = self._current_speed + int(increment)
        current_speed = max(min(current_speed, MAXIMUM_SPEED), DISABLED_SPEED)
        self._set_motor_speed(current_speed) 
