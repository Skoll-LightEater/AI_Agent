import os
from google.genai import types

#LLM Schema script

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

#Function

def get_files_info(working_directory, directory="."):
    full_dir = os.path.abspath(os.path.join(working_directory, directory))
    work_dir = os.path.abspath(working_directory)
    if not full_dir.startswith(work_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isfile(full_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        stringy = ""
        for item in os.listdir(full_dir):
            stringy += f"- {item}: file_size={os.path.getsize(os.path.join(full_dir, item))}, is_dir={os.path.isdir(os.path.join(full_dir, item))}\n"
        return stringy
    except Exception as e:
        return f"Error: {e}"

