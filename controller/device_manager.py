from controller.exceptions import StartupException

CONF_PREFIX = "device="

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
        for line in lines:
            if line.startswith(CONF_PREFIX):
                device = line[len(CONF_PREFIX):]
                
        if not device:
            raise StartupException(f"Invalid device specified in config '{self._path}'")
        
        return device