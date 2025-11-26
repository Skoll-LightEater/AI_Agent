import os

from google.genai import types

#LLM Schema script

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the content if the file is a valid .txt document, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to a file, relative to the working directory"
            ),
        },
    ),
)

#Function

def get_file_content(working_directory, file_path):
    full_dir = os.path.abspath(os.path.join(working_directory, file_path))
    work_dir = os.path.abspath(working_directory)
    if not full_dir.startswith(work_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        max_characters = 10000
        with open(full_dir, "r") as f:
            content = f.read(max_characters)
            if len(content) == max_characters:
                content += f' [...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f"Error: {e}"
