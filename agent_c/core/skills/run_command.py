from typing import Annotated
import subprocess

def run_command(terminal_id: Annotated[str, "Terminal ID"], command: Annotated[str, "Command to execute"]) -> Annotated[str, "Command execution status"]:
    """
    Executes a shell command in a specified terminal and returns the output.

    Parameters:
    terminal_id (str): Identifier for the terminal in which the command should be run.
    command (str): The shell command to execute.

    Returns:
    str: The output from the terminal after running the command.
    """
    try:
        result = subprocess.run(['./run_command', terminal_id, command], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    terminal_id = "79335"  # Example terminal ID
    command = "ls"
    
    output = run_command(terminal_id, command)
    print(output)
