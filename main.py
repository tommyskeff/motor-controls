from speed_regulator import SpeedRegulator
from vesc_controller import MotorVESC, DummyVESC
from simple_display import SliderWindow
from device_manager import DeviceManager
from exceptions import StartupException
import asyncio
import logging
import sys
import time

ACC_LIM = 250
LOG_FILE = "latest.log"
MOTOR_MODE = "VESC" # DUMMY or VESC
BASIC_WINDOW = True

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


async def entrypoint():
    debug_log = logging.FileHandler(LOG_FILE)
    console_log = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    debug_log.setFormatter(formatter)
    console_log.setFormatter(formatter)
   
    LOGGER.addHandler(debug_log)
    LOGGER.addHandler(console_log)

    try:
        LOGGER.info("Starting motor control program...")
        await asyncio.sleep(1.5)
        await main()
    except StartupException as e:
        LOGGER.error("Failed to start the motor controller: " + str(e))


async def main():
    device_manager = DeviceManager()
    port = device_manager.read_port_from_file()

    match MOTOR_MODE:
        case "DUMMY":
            motor = DummyVESC(LOGGER, port)
        case "VESC":
            motor = MotorVESC(LOGGER, port)
        case other:
            raise StartupException(f"Invalid motor mode '{MOTOR_MODE}', options are DUMMY and VESC")
        
    motor.connect()

    slider = SliderWindow()
    regulator = SpeedRegulator(motor, slider, ACC_LIM)

    asyncio.create_task(regulator.start())
    await asyncio.create_task(slider.run())

    motor.close()


if __name__ == "__main__":
    try:
        asyncio.run(entrypoint())
    except KeyboardInterrupt:
        LOGGER.info("Shutting down motor control program...")
        time.sleep(1)
