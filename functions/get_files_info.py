import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    #absolute_path = os.path.abspath(working_directory, directory)
    working_directory_absoulte_path = os.path.abspath(working_directory)

    absolute_path = working_directory_absoulte_path

    # 
    if directory:
        absolute_path = os.path.abspath(os.path.join(working_directory, directory))


    if not absolute_path.startswith(working_directory_absoulte_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    try: 
        files_info = [] # list to append the string outputs
        for filename in os.listdir(absolute_path):
            filepath = os.path.join(absolute_path, filename) # creating an absolute path with all the files in target_dir
            file_size = 0
            is_dir = os.path.isdir(filepath) # check if the filepath is a directory
            file_size = os.path.getsize(filepath) # get filesize of the filepath 
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)