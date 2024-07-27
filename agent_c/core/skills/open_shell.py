import subprocess
import platform
import asyncio

async def open_shell() -> str:
    system = platform.system()

    if system == "Darwin":  # macOS
        command = '''
        tell application "Terminal"
            activate
            do script ""
        end tell
        '''
        subprocess.run(['osascript', '-e', command])
    elif system == "Linux":  # Linux
        subprocess.run(['gnome-terminal'])
    elif system == "Windows":  # Windows
        subprocess.run(['powershell', '-NoExit', '-Command', 'New-PSSession -Name mysession'])
    
    return "Terminal session started."

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(open_shell()))
