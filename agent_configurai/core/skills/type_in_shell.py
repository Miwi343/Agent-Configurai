from typing import Annotated, Tuple
import platform
import asyncio

async def type_in_shell(command: Annotated[str, "Command to type and execute"]) -> Annotated[Tuple[str, str], "Command output and error"]:
    system = platform.system()

    if system == "Darwin":  # macOS
        applescript_command = f'''
        tell application "Terminal"
            activate
            do script "{command}" in front window
        end tell
        '''
        process = await asyncio.create_subprocess_exec(
            'osascript', '-e', applescript_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    elif system == "Linux":  # Linux
        bash_command = f'gnome-terminal -- bash -c "{command}; exec bash"'
        process = await asyncio.create_subprocess_exec(
            'bash', '-c', bash_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    elif system == "Windows":  # Windows
        powershell_command = f'Enter-PSSession -Name mysession; {command}'
        process = await asyncio.create_subprocess_exec(
            'powershell.exe', '-Command', powershell_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    else:
        raise OSError(f"Unsupported platform: {system}")

    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

if __name__ == "__main__":
    command = "echo Hello World"
    
    async def main():
        output, error = await type_in_shell(command)
        print(f"Output: {output}")
        print(f"Error: {error}")

    asyncio.run(main())
