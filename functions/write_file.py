import os 
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the file location that is asked of you, replace it each time with whatever text user is looking for ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write your file to the location you are pointed at and ",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description = "the content that should be written"
            )
        },
    ),
)


def write_file(working_directory,file_path,content) : 
    try: 
        full_target_path = os.path.join(working_directory,file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path= os.path.abspath(full_target_path) 
        if abs_target_path.startswith(abs_working_dir) == False :
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.exists(full_target_path) == False:
            os.makedirs(os.path.dirname(full_target_path),exist_ok=True)


        with open(full_target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error:{str(e)}"
