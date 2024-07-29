import subprocess
from typing import Annotated

def capture_output() -> Annotated[str, "Output of the command"]:
    # Execute the command and capture its output
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

    # if empty output, return string "success"
    if not result.stdout:
        return "No terminal output - successfully ran command"

    # Access the output
    return result.stdout

if __name__ == "__main__":
    print(capture_output())