from speed_regulator import SpeedRegulator
from vesc_controller import MotorVESC, DummyVESC
from simple_display import SliderWindow
from device_manager import DeviceManager
from exceptions import StartupException
import asyncio
import logging

ACC_LIM = 250
LOG_FILE = "latest.log"
LOGGER = logging.getLogger('motor_controller')
MOTOR_MODE = "DUMMY" # DUMMY or VESC


async def entrypoint():
    debug_log = logging.FileHandler(LOG_FILE)
    debug_log.setLevel(logging.DEBUG)
    
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    debug_log.setFormatter(formatter)
    console_log.setFormatter(formatter)
   
    LOGGER.addHandler(debug_log)
    LOGGER.addHandler(console_log)
    

    try:
        await main()
    except StartupException as e:
        LOGGER.error("Failed to start the motor controller: " + str(e))


async def main():
    device_manager = DeviceManager()
    port = device_manager.read_port_from_file()

    match MOTOR_MODE:
        case "DUMMY":
            motor = DummyVESC(port)
        case "VESC":
            motor = MotorVESC(port)
        case other:
            raise StartupException(f"Invalid motor mode '{MOTOR_MODE}', options are DUMMY and VESC")
        
    motor.connect()

    slider = SliderWindow()
    regulator = SpeedRegulator(motor, slider, ACC_LIM)

    asyncio.create_task(regulator.start())
    await asyncio.create_task(slider.run())

    motor.close()


if __name__ == "__main__":
    asyncio.run(entrypoint())
