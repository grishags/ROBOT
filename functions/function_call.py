from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

from google.genai import types

working_dict = "./calculator"
function_dict = {"write_file": write_file ,
                 "get_file_content" : get_file_content, 
                 "get_files_info":get_files_info,
                 "run_python_file": run_python_file} 


def call_function (function_call_part,verbose = False):
    if verbose: 
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")
    
    arguements = function_call_part.args.copy() 
    arguements["working_directory"] = "./calculator"
    
    
    if function_call_part.name in function_dict: 
        function_result = function_dict[function_call_part.name](**arguements)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )

    else: 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name ,
                    response={"error": f"Unknown function: {function_call_part.name }"},
                )
            ],
        )
            
