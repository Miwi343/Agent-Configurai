from typing import Annotated
import subprocess

def open_shell(os_type: Annotated[str, "Operating System"]) -> Annotated[str, "Terminal ID"]:
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
        process = subprocess.Popen(['gnome-terminal'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        terminal_id = str(process.pid)
    
    elif os_type == "Windows":  # Windows
        command = 'Start-Process powershell -NoNewWindow -PassThru'
        process = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
        terminal_id = process.stdout.strip()

    else:
        raise ValueError(f"Unsupported operating system: {os_type}")
    
    return terminal_id

if __name__ == "__main__":
    import platform
    os_type = platform.system()
    terminal_id = open_shell(os_type)
    print(f"Opened terminal with ID: {terminal_id}")
