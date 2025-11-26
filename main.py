#get key

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#load LLM

from google import genai

client = genai.Client(api_key=api_key)

from google.genai import types

#import sys

import sys
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *


#locate function Schemas

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

#set variables

#system_prompt2 = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#call function to run external functions

def call_function(function_call_part, verbose=False):
    function_dict = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "run_python_file" : run_python_file,
        "write_file" : write_file
    }

    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_call_part.args["working_directory"] = "./calculator"

    if function_call_part.name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    function_result = function_dict[function_call_part.name](**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


#Main

def main():
    print("Hello from ai-agent!")

    if len(sys.argv) < 2:
        sys.exit("Error: No input detected!")

    user_prompt = sys.argv[1]
    timer = 0
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    while timer < 20:
        timer += 1
        loop_count = 0
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )
        )

        verbose = "--verbose" in sys.argv
        temp_list = []
        if response.function_calls == None:
            print(response.text)
        else:
            for function_call_part in response.function_calls:
                new_resp = call_function(function_call_part, verbose)
                if not new_resp.parts[0].function_response.response:
                    raise FatalException("Fatal Error")
                temp_list.append(new_resp.parts[0])
                if verbose:
                    print(f"-> {new_resp.parts[0].function_response.response}")

        for a in response.candidates:
            messages.append(a.content)
        messages.append(types.Content(role="user", parts=temp_list))


        args = []
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                args.append(arg)

        if verbose:
            print(f"User prompt: {user_prompt}\n")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        for a in response.candidates:
            for b in a.content.parts:
                if b.function_call:
                    loop_count += 1
        if loop_count == 0 and response.text:
            print(response.text)
            break



if __name__ == "__main__":
    main()
