from controller.speed_regulator import SpeedRegulator
from controller.vesc_controller import MotorVESC, DummyVESC
from controller.simple_display import SliderWindow
from controller.device_manager import DeviceManager
from controller.exceptions import StartupException
from controller.picoboard import PicoBoard
import asyncio
import logging
import sys
import os
import time

ACC_LIM = 250
LOG_FOLDER = "logs"
LOG_FILE = "latest.log"
DEVICE_FILE = "config/device.conf"
MOTOR_MODE = "VESC" # DUMMY or VESC or DUMMY_PICO
BASIC_WINDOW = True

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def main():
    console_log = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_log.setFormatter(formatter)
    LOGGER.addHandler(console_log)
    
    try:
        try:
            os.mkdir(LOG_FOLDER)
        except FileExistsError:
            pass
        
        debug_log = logging.FileHandler(LOG_FOLDER + "/" + LOG_FILE)
        debug_log.setFormatter(formatter)
        LOGGER.addHandler(debug_log)
        
        LOGGER.info("Starting motor control program...")
        time.sleep(1.5)
        asyncio.run(main_async())
    except StartupException as e:
        LOGGER.error("Failed to start the motor controller: " + str(e))
    except KeyboardInterrupt:
        LOGGER.info("Shutting down motor control program...")
        time.sleep(1)


async def main_async():
    device_manager = DeviceManager(DEVICE_FILE)
    port, slider_port = device_manager.read_port_from_file()
    slider = SliderWindow()

    tasks = []
    match MOTOR_MODE:
        case "DUMMY":
            motor = DummyVESC(LOGGER, port)
        case "VESC":
            motor = MotorVESC(LOGGER, port)
            pb = PicoBoard(slider_port)
            tasks.append(lambda : run_pico(pb, slider))
        case "DUMMY_PICO":
            motor = DummyVESC(LOGGER, port)
            pb = PicoBoard(slider_port)
            tasks.append(lambda : run_pico(pb, slider))
            
        case other:
            raise StartupException(f"Invalid motor mode '{MOTOR_MODE}', options are DUMMY and VESC")
        
    motor.connect()
    
    regulator = SpeedRegulator(motor, slider, ACC_LIM)
    tasks.append(regulator.start)
    
    for t in tasks:
        asyncio.create_task(t()) 

    await asyncio.create_task(slider.run())
    motor.close()
    
    
async def run_pico(pb: PicoBoard, display: SliderWindow):
    while True:
        try:
            readings = pb.read()
            slider = min(readings["slider"] / 1000, 1)
            display.set_slider_value(slider)
        except Exception as e:
            LOGGER.error("slider error", e)
        
        await asyncio.sleep(0.05)


if __name__ == "__main__":
    main()
        