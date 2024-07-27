import platform
import subprocess
from typing import Annotated, Dict, Any

def get_macos_version() -> str:
    try:
        result = subprocess.run(['sw_vers', '-productVersion'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown macOS version"

def get_os() -> Annotated[Dict[str, Any], "OS information"]:
    os_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "macos_version": get_macos_version()
    }
    return os_info

if __name__ == "__main__":
    print(get_os())
