from typing import Annotated
import subprocess
import asyncio
import platform
import os

async def run_command(terminal_id: Annotated[str, "Terminal ID"], command: Annotated[str, "Command to execute"]) -> Annotated[str, "Command Output"]:
    """
    Executes a shell command in a specified terminal and returns the output.

    Parameters:
    terminal_id (str): Identifier for the terminal in which the command should be run.
    command (str): The shell command to execute.

    Returns:
    str: The output from the terminal after running the command.
    """
    try:
        # Construct the absolute path to the bash script
        script_path = os.path.join(os.path.dirname(__file__), 'run_command.sh')
        
        # Run the bash script with the terminal_id and command as arguments
        result = subprocess.run([script_path, terminal_id, command], capture_output=True, text=True)
        output = result.stdout.strip()

        return output
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    async def main():
        # Open a shell to get the terminal ID
        from open_shell import open_shell
        os_type = platform.system()
        terminal_id =  open_shell(os_type)
        print(f"Opened terminal with ID: {terminal_id}")

        # List of commands to execute
        commands = ["ls", "cd ~/Desktop", "ls -la", "cd Projects/", "ls", "cd Miwi/"]  # Example commands

        # Run each command and print the output
        for command in commands:
            output = await run_command(terminal_id, command)
            print("\n")
            print(f"Captured output for '{command}':\n{output}")

    asyncio.run(main())
