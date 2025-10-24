import os

def create_file(filepath: str, content: str = ""):
    """Creates a new file at the specified filepath with given content."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"File '{filepath}' created successfully"
    except Exception as e:
        return f"Error creating file: {str(e)}"

def read_file(filepath: str):
    """Reads and returns the content of a file at the specified filepath."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

def update_file(filepath: str, content: str):
    """Appends content to an existing file at the specified filepath."""
    try:
        with open(filepath, 'a') as f:
            f.write(content)
        return f"File '{filepath}' updated successfully"
    except Exception as e:
        return f"Error updating file: {str(e)}"

def delete_file(filepath: str):
    """Deletes the file at the specified filepath."""
    try:
        os.remove(filepath)
        return f"File '{filepath}' deleted successfully"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

def list_directory(path: str = "."):
    """list all files and directories in the specified path."""
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error Listing directory: {str(e)}"
