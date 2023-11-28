from exceptions import StartupException

DEVICE_FILE = "device"

class DeviceManager:

    def __init__(self) -> None:
        pass

    def read_port_from_file(self) -> str:
        try:
            f = open(DEVICE_FILE, "r")
            port = f.readline()
            f.close()
        except FileNotFoundError:
            raise StartupException(f"Device file '{DEVICE_FILE}' does not exist in the filesystem")
        
        return port