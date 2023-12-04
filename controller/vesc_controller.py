from controller.exceptions import StartupException
from serial import Serial, SerialException
import logging
import pyvesc
from pyvesc.VESC.messages import SetRotorPositionMode, SetRPM
import random

BAUD_RATE = 115200
TIMEOUT = 0.05


class MotorVESC:

    def __init__(self, logger: logging.Logger, port: str) -> None:
        self._logger = logger
        self._port = port
        self._set_mode = False
        self._conn = None


    def connect(self) -> None:
        self._logger.info(f"Attempting to connect to {self._port}...")
        try:
            self._conn = Serial(self._port, baudrate=BAUD_RATE, timeout=TIMEOUT)
        except SerialException as e:
            raise StartupException(f"Failed to connect to serial port '{self._port}'")
        

    def close(self) -> None:
        self.set_speed(0)


    def set_speed(self, speed: int) -> None:
        if not self._set_mode:
            self._set_mode = True
            self._send_message(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_ENCODER))

        self._send_message(SetRPM(speed))
        

    def _send_message(self, message) -> None:
        data = pyvesc.encode(message)
        self._conn.write(data)



class DummyVESC(MotorVESC):

    def connect(self) -> None:
        self._logger.info("Dummy connected.")


    def close(self) -> None:
        self.set_speed(0)
        self._logger.info("Dummy closed.")


    def set_speed(self, speed: int) -> None:
        if not self._set_mode:
            self._set_mode = True
            self._logger.info("Dummy initialized motor speed controller.")


        if random.random() > 0.99:
            self._logger.debug(f"Dummy set motor speed {speed}")
        

    def _send_message(self, message) -> None:
        self._logger.debug(f"Sending message {message}")