import pyvesc
from pyvesc.VESC.messages import SetRotorPositionMode, GetRotorPosition, SetRPM, GetValues
import serial
import random

BAUD_RATE = 115200
TIMEOUT = 0.05

class MotorVESC:

    def __init__(self, port: str) -> None:
        self._port = port
        self._set_mode = False
        self._conn = None

    def connect(self) -> None:
        self._conn = serial.Serial(self._port, baudrate=BAUD_RATE, timeout=TIMEOUT)
        self._conn.open()

    def close(self) -> None:
        self.set_speed(0)
        self._conn.close()

    def set_speed(self, speed: int) -> None:
        if not self._set_mode:
            self._set_mode = True
            self._send_message(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_ENCODER))

        self._send_message(SetRPM(speed))
        self._send_message(GetValues)
        

    def _send_message(self, message) -> None:
        data = pyvesc.encode(message)
        self._conn.write(data)



class DummyVESC(MotorVESC):
    def connect(self) -> None:
        print("Dummy connected.")

    def close(self) -> None:
        self.set_speed(0)
        print("Dummy closed.")

    def set_speed(self, speed: int) -> None:
        if not self._set_mode:
            self._set_mode = True
            print("Dummy initialized motor speed controller.")


        # if random.random() > 0.995:
        #     print(f"Dummy set motor speed {speed}")
        

    def _send_message(self, message) -> None:
        pass