import os
from google.genai import types

#LLM Schema script

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Allows you to create or overwrite a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to a file, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content you want to save to the file"
            ),
        },
    ),
)

#Function

def write_file(working_directory, file_path, content):
    full_dir = os.path.abspath(os.path.join(working_directory, file_path))
    work_dir = os.path.abspath(working_directory)
    if not full_dir.startswith(work_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        new_dir, new_file = os.path.split(full_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        with open(full_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
