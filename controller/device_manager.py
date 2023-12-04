from controller.exceptions import StartupException

DEVICE_PREFIX = "device="
SLIDER_PREFIX = "slider-device="

class DeviceManager:

    def __init__(self, path: str) -> None:
        self._path = path

    def read_port_from_file(self) -> str:
        try:
            f = open(self._path, "r")
            lines = f.readlines()
            f.close()
        except FileNotFoundError:
            raise StartupException(f"Device file '{self._path}' does not exist in the filesystem")
        
        device = None
        slider = None
        
        for line in lines:
            if line.startswith(DEVICE_PREFIX):
                device = line[len(DEVICE_PREFIX):]
            if line.startswith(SLIDER_PREFIX):
                slider = line[len(SLIDER_PREFIX):]
                
        if (not device) or (not slider):
            raise StartupException(f"Invalid device specified in config '{self._path}'")
        
        return device, slider