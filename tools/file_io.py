from typing import Any, Optional
from smolagents.tools import Tool
import os
class file_writer(Tool):
    name = "file_writer"
    description = "you can use this tool to write to a simple file"
    inputs = {
        "filename": {"type": "string", "description": "the name of the file"},
        "content": {
            "type": "string",
            "description": "the content to write to the file",
        },
        "mode":{
            "type":"boolean",
            "description":"the mode to write to the file, if true, the file will be appended, if false, the file will be overwritten",
            "nullable":"True",
        }
    }

    output_type = "any"

    def forward(self, filename: str, content: str,mode:bool=False) -> Any:
        # file_dir='./outputs'
        # filename=os.path.join(file_dir,filename)
        if mode==False:
            io_mode="w"
        else:
            io_mode="a"
        with open(filename, io_mode) as f:
            f.write(content)
        return filename
    def __init__(self,*args,**kwargs):
        self.is_initialized = False
class file_reader(Tool):
    name="file_reader"
    description="you can use this tool to read a simple txt file. eg test.txt"
    inputs={
        "filename":{"type":"string","description":"the name of the file.eg /usr/loacl/data/test.txt"},
    }
    output_type="str"
    def forward(self,filename:str)-> str:
        with open(filename,"r") as f:
            content=f.read()
        return content
    def __init__(self,*args,**kwargs):
        self.is_initialized = False