import os

def run_command(cmd: str):
    """Executes a system command and returns the result."""
    result = os.system(cmd)
    return result

