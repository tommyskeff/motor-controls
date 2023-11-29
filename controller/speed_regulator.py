from controller.simple_display import SliderWindow
from controller.vesc_controller import MotorVESC
import asyncio
import math

CYCLE_INTERVAL = 0.01
DISABLED_SPEED = 800
MAXIMUM_SPEED = 20000
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
        speed_desired = DISABLED_SPEED + self._potentiometer_reading * (MAXIMUM_SPEED - DISABLED_SPEED)
        speed_desired = speed_desired // zerosPower * zerosPower

        speed_difference = speed_desired - self._current_speed
        if speed_difference > 0:
            speed_difference = min(speed_difference, self._acceleration_limit)
        else:
            speed_difference = max(speed_difference, -self._acceleration_limit)

        return speed_difference


    def _set_motor_speed(self, speed: int) -> None:
        self._current_speed = speed
        self._controller.set_speed(speed)
        self._window.set_text(f"Speed: {speed}")


    def _cycle(self) -> None:
        self._potentiometer_reading = self._window.get_slider_value()
        increment = self._calculate_speed_increment()
        current_speed = self._current_speed + int(increment)
        current_speed = max(min(current_speed, MAXIMUM_SPEED), DISABLED_SPEED)
        self._set_motor_speed(current_speed)
        
