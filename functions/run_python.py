import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file is relative to the working directory.",
            ),
        },
        required = ["file_path"]
    ),
)




def run_python_file(working_directory, file_path): 
    try:
        full_target_path= os.path.join(working_directory, file_path) 
        abs_target_path = os.path.abspath(full_target_path)
        abs_working_dir = os.path.abspath(working_directory)
        if abs_target_path.startswith(abs_working_dir) == False :
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif  os.path.exists(full_target_path) == False:
            return f'Error: File "{file_path}" not found.'
        elif file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        
        p1 = subprocess.run(["python3" ,abs_target_path] ,timeout = 30,capture_output = True,cwd = abs_working_dir,    text=True    )
        output = [] 
        if p1.stdout != "":
            output.append(f"STDOUT:{p1.stdout}")
        if p1.stderr != "": 
            output.append(f"STDERR:{p1.stderr}")
        if p1.returncode > 0 : 
            output.append(f"Process exited with code {p1.returncode}")
        if len(output) == 0:
            return "No output produced"
        return '\n'.join(output)

    except Exception as e: 
        return f"Error: executing Python file: {e}"



   