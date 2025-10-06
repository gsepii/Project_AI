import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir, file_path))
    
    if not target_file.startswith(working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent_dir = os.path.dirname(target_file)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}" 

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents provided from the 'content' variable to the file provided by file_path, constrained within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the input file, to be found within the working directory."
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="The contents that are to be written to the target file found from the file path."
            )
        },
        required=["file_path"],
    ),
)