from config.settings import EXIT_COMMANDS, TOOL_PARAM_SEPARATOR, EMOJI_TOOL

def print_welcome_message():
    """Prints the welcome message when the chat starts."""
    print("\n\n\n")
    print("💬 Chat started! Type 'exit', 'quit', or 'bye' to end the conversation.\n")

def check_exit_command(user_input: str) -> bool:
    """Checks if the user input is an exit command."""
    return user_input.lower().strip() in EXIT_COMMANDS

def handle_tool_execution(tool_name: str, tool_input: str, available_tools: dict):
    """Handles the execution of a tool and returns the response."""
    print(f"{EMOJI_TOOL}: {tool_name}({tool_input})")

    # Handle tools with multiple parameters
    if tool_name in ["create_file", "update_file"]:
        params = tool_input.split(TOOL_PARAM_SEPARATOR)
        tool_response = available_tools[tool_name](*params)
    else:
        tool_response = available_tools[tool_name](tool_input)

    print(f"{EMOJI_TOOL}: {tool_name}({tool_input}) = {tool_response}")
    return tool_response
