from typing import Annotated
import platform
import asyncio

async def run_command(command: Annotated[str, "Command to execute"]) -> Annotated[str, "Command execution status"]:
    system = platform.system()

    if system == "Darwin":  # macOS
        applescript_command = f'''
        tell application "Terminal"
            activate
            do script "{command}" in front window
        end tell
        '''
        # Start process to execute the command
        process = await asyncio.create_subprocess_exec(
            'osascript', '-e', applescript_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        # Wait for the process to finish and get the output
        stdout, stderr = await process.communicate()
        return f"Command '{command}' executed. Output: {stdout.decode()}, Error: {stderr.decode()}"

    elif system == "Linux":  # Linux
        bash_command = f'gnome-terminal -- bash -c "{command}; exec bash"'
        process = await asyncio.create_subprocess_exec(
            'bash', '-c', bash_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to finish and get the output
        stdout, stderr = await process.communicate()
        return f"Command '{command}' executed. Output: {stdout.decode()}, Error: {stderr.decode()}"
    
    elif system == "Windows":  # Windows
        powershell_command = f'Enter-PSSession -Name mysession; {command}'
        process = await asyncio.create_subprocess_exec(
            'powershell.exe', '-Command', powershell_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to finish and get the output
        stdout, stderr = await process.communicate()
        return f"Command '{command}' executed. Output: {stdout.decode()}, Error: {stderr.decode()}"
    else:
        raise OSError(f"Unsupported platform: {system}")


if __name__ == "__main__":
    command = "echo Hello World"
    
    async def main():
        status = await run_command(command)
        print(status)

    asyncio.run(main())
