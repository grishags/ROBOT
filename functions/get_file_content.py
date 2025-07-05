import os 
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of a file and returns the contents in a text string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The files to gather content from , relative to the working directory. If not provided do not proceed",
            ),
        
        },
        required = ["file_path"]
    ),
)




def get_file_content(working_directory,file_path):
    try: 
        full_target_path = os.path.join(working_directory,file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path= os.path.abspath(full_target_path) 
        if abs_target_path.startswith(abs_working_dir) == False :
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(abs_target_path) == False:
            return f'Error: File not found or is not a regular file "{file_path}"'
        
        MAX_CHARS = 10000

        with open(full_target_path, "r") as f:
            
            file_content_string,file_content_left= f.read(MAX_CHARS),f.read() 
            if len(file_content_left) > 0 :
                 return file_content_string + f"[...File {file_path} truncated at 10000 characters]"
            else: 
                 return file_content_string
    except Exception as e:
        return f"Error:{str(e)}"
    

