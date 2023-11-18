import asyncio
from simple_display import SliderWindow

CYCLE_INTERVAL = 0.01

class MotorController:

    def __init__(self, window: SliderWindow, acceleration_limit: float) -> None:
        self._window = window
        self._running = False
        self._current_speed = 1000
        self._speed_desired = 1000
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
        speed_desired = 1000 + self._potentiometer_reading * (20000 - 1000)
        speed_desired = speed_desired // 100 * 100

        speed_difference = speed_desired - self._current_speed
        increment_speed = speed_difference / 1
        increment_speed = min(increment_speed, self._acceleration_limit)

        return increment_speed

    def _set_motor_speed(self, speed: int) -> None:
        self._current_speed = speed
        self._window.set_text(f"RPM: {speed}")

    def _cycle(self) -> None:
        self._potentiometer_reading = self._window.get_slider_value()
        increment = self._calculate_speed_increment()
        current_speed = self._current_speed + int(increment)
        current_speed = max(min(current_speed, 20000), 1000)
        self._set_motor_speed(current_speed) 
