import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        result = f"Result for '{target_dir}' directory:\n"
        if not valid_target_dir:
            result += f'\tError: Cannot list "{directory}" as it is outside the permitted working directory\n'
            return result

        if not os.path.isdir(target_dir):
            result += f'\tError: "{directory}" is not a directory\n'
            return result
    
        print(os.listdir(target_dir))
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)

            result += f" - {item}: file_size={size} bytes, is_dir={is_dir}\n"

        #return f'Success: "{directory}" is within the working directory'
        return result       
    except Exception as e:
        return f'Error: {e}'
