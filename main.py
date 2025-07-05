import os 
import sys 
from dotenv import load_dotenv
from google import genai 
from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *
from functions.function_call import *

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan and then resolve the code the users asks you to fix.
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

 
config=types.GenerateContentConfig(
    tools =[available_functions],system_instruction=system_prompt )


max_loop = 20 


def main():
    load_dotenv("gemini_key.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    query = sys.argv[1]
    flag_present = "--verbose" in sys.argv[2:]
    llm_messages = [types.Content(parts=[types.Part(text=query)],role='user')]
    attempts =1
    while max_loop >= attempts:
        attempts += 1 

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=llm_messages,
            config = config 
        )     
 
        function_calls = []
        if response.candidates:
            for i in response.candidates:
                llm_messages.append(i.content)
                for part in i.content.parts:
                     if part.function_call:
                        function_calls.append(part.function_call)
                    
            
    

        functions_flag = len(function_calls) > 0


        if flag_present  :    
            print(response.text)
            print(f"User prompt:{query}")   
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if functions_flag:
            for function_call in function_calls:
                function_call_result = call_function(function_call, verbose=flag_present)
                llm_messages.append(function_call_result)
                if hasattr(function_call_result.parts[0], "function_response"):
                    result = function_call_result.parts[0].function_response.response
                    if flag_present:
                        print(f"-> {result}")

                else:

                    raise RuntimeError("No function response present!")
        
        else:
            if flag_present:
                pass
            else:
                print(response.text)
                return 




if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main()
    else:
        raise Exception("Requires a query at the very least")
        sys.exit(1)
    

