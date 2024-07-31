from typing import Annotated
import platform
import asyncio
import subprocess

async def open_shell(os_type: Annotated[str, "Operating System"]) -> Annotated[str, "Terminal ID"]:
    """
    Opens a new terminal window based on the specified operating system and returns the terminal ID.

    Parameters:
    os_type (str): The operating system type (Darwin, Linux, Windows).

    Returns:
    str: The ID of the opened terminal window.
    """
    terminal_id = ""
    
    if os_type == "Darwin":  # macOS
        command = '''
        tell application "Terminal"
            activate
            do script ""
            set terminal_id to id of front window
        end tell
        '''
        process = subprocess.run(['osascript', '-e', command], capture_output=True, text=True)
        terminal_id = process.stdout.strip()

    elif os_type == "Linux":  # Linux
        process = await asyncio.create_subprocess_exec(
            'gnome-terminal',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        # The terminal ID logic would be different for actual implementation
        # For simplicity, we use the process ID
        terminal_id = str(process.pid)
    
    elif os_type == "Windows":  # Windows
        command = 'New-PSSession -Name mysession'
        process = subprocess.run(['powershell', '-NoExit', '-Command', command], capture_output=True, text=True)
        # Capture the session name or ID if possible
        terminal_id = "mysession"

    else:
        raise ValueError(f"Unsupported operating system: {os_type}")
    
    return terminal_id

if __name__ == "__main__":
    os_type = platform.system()  # Example OS type
    
    async def main():
        terminal_id = await open_shell(os_type)
        print(f"Opened terminal with ID: {terminal_id}")

    asyncio.run(main())
