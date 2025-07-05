import os 
from google.genai import types


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



def get_files_info(working_directory, directory= "." ):
    try:
        full_target_path= os.path.join(working_directory, directory) 
        abs_target_path = os.path.abspath(full_target_path)
        abs_working_dir = os.path.abspath(working_directory)
        if abs_target_path.startswith(abs_working_dir) == False :
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif os.path.isdir(abs_target_path) == False:
            return f'Error: "{directory}" is not a directory'
        target_dir_list=os.listdir(abs_target_path)
        present_files = [] 
        for file in target_dir_list:
                file_path = os.path.join(full_target_path,file)
                file_path =  os.path.abspath(file_path)
                present_files.append(f'- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}') 
        return '\n'.join(present_files)
    except Exception as e:
         return f"Error:{str(e)}"
         


