import platform
import asyncio
import subprocess
from typing import Annotated

async def get_terminal_output(command: Annotated[str, "Command to run"]) -> Annotated[str, "Command Output"]:
    """
    Runs a command in the terminal and returns the output.

    Parameters:
    command (str): The command to run.

    Returns:
    str: The output of the command.
    """
    os_type = platform.system()
    outputs = []

    if os_type == "Darwin" or os_type == "Linux":  # macOS and Linux
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            outputs.append(stdout.decode('utf-8')) #type: ignore
        else:
            outputs.append(stderr.decode('utf-8')) #type: ignore

    elif os_type == "Windows":  # Windows
        process = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
        if process.returncode == 0:
            outputs.append(process.stdout) #type: ignore
        else:
            outputs.append(process.stderr) #type: ignore

    else:
        raise ValueError(f"Unsupported operating system: {os_type}")

    return '\n'.join(outputs) #type: ignore

if __name__ == "__main__":
    command = "ls -la"  # Example command
    
    async def main():
        output = await get_terminal_output(command)
        print(f"Command output:\n{output}")

    asyncio.run(main())
