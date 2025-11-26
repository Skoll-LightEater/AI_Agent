import os
import subprocess
from google.genai import types

#LLM Schema script

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Allows you to run a valid python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to a file, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="List the python files you wish to run"
            ),
        },
    ),
)

#Function

def run_python_file(working_directory, file_path, args=[]):
    full_dir = os.path.abspath(os.path.join(working_directory, file_path))
    work_dir = os.path.abspath(working_directory)
    if not full_dir.startswith(work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_dir):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python", full_dir, *args], capture_output=True, cwd=working_directory, timeout=30, text=True)
        response = ""
        if result.stdout != "":
            response += f"STDOUT: {result.stdout}\n"
        if result.stderr != "":
            response += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            response += f"Process exited with code {result.returncode}"
        if response == "":
            return "No output produced."
        else:
            return response
        return response
    except Exception as e:
        return f"Error: executing Python file: {e}"
