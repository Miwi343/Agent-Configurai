from typing import Annotated
import subprocess
import asyncio
import platform
from .get_terminal_output import get_terminal_output  # Absolute import

async def run_command(terminal_id: Annotated[str, "Terminal ID"], command: Annotated[str, "Command to execute"]) -> Annotated[str, "Command Output"]:
    """
    Executes a shell command in a specified terminal and returns the output.

    Parameters:
    terminal_id (str): Identifier for the terminal in which the command should be run.
    command (str): The shell command to execute.

    Returns:
    str: The output from the terminal after running the command.
    """
    os_type = platform.system()
    try:
        # Run the command in the actual terminal
        if os_type == "Darwin":  # macOS
            run_script = f'''
            tell application "Terminal"
                do script "{command}" in window id {terminal_id}
            end tell
            '''
            subprocess.run(['osascript', '-e', run_script], capture_output=True, text=True)

        elif os_type == "Linux":  # Linux
            subprocess.run(['gnome-terminal', '--', 'bash', '-c', command])

        elif os_type == "Windows":  # Windows
            run_script = f'Start-Process powershell -ArgumentList "{command}" -NoNewWindow -PassThru'
            subprocess.run(['powershell', '-Command', run_script])

        # Custom message for 'cd' command
        if command.startswith("cd "):
            directory = command[3:].strip()
            # Actual terminal will execute the cd command without any output
            output = f"Navigated successfully to {directory}"
        else:
            # Capture the output using get_terminal_output
            output = await get_terminal_output(command)
            
        return output
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    async def main():
        # Open a shell to get the terminal ID
        from agent_c.core.skills.open_shell import open_shell
        os_type = platform.system()
        terminal_id = open_shell(os_type)
        print(f"Opened terminal with ID: {terminal_id}")

        # List of commands to execute
        commands = ["cd ~/Desktop", "ls -la"]  # Example commands

        # Run each command and print the output
        for command in commands:
            output = await run_command(terminal_id, command)
            print("\n")
            print(f"Captured output for '{command}':\n{output}")

    asyncio.run(main())
