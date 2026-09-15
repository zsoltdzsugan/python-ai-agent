import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file' 

        command = ["python", target_file]

        if not args == None:
            command.extend(args)

        process_result = subprocess.run(command,capture_output=True, cwd=working_directory, text=True, timeout=30)

        output = ''
        if process_result.returncode != 0:
            output += f'Process exited with code {process_result.returncode}'

        if not process_result.stdout and not process_result.stderr:
            output += f'No output produced'

        if process_result.stdout:
            output += f'STDOUT: {process_result.stdout}'

        if process_result.stderr:
            output += f'STDERR: {process_result.stderr}'

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
