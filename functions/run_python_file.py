import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    work_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(work_dir, file_path))

    if not target_path.startswith(work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python", target_path] + args
        completed_process = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=30, 
            cwd=work_dir
        ) 

        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}") 
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not output:
            return "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return output

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python command on the provided file from the variable 'file_path' using any arguments if provided, constrained within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the input file, to be found within the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the file."
                ),
                description="Optional arguments to pass to the file."
            ),
        },
        required=["file_path"],
    ),
)