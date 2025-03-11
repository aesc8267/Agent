from typing import Any, Optional
from smolagents.tools import Tool


class file_writer(Tool):
    name = "file_writer"
    description = "you can use this tool to write to a simple file"
    inputs = {
        "filename": {"type": "string", "description": "the name of the file"},
        "content": {
            "type": "string",
            "description": "the content to write to the file",
        },
    }

    output_type = "any"

    def forward(self, filename: str, content: str) -> Any:
        with open(filename, "w") as f:
            f.write(content)
        return filename
    def __init__(self,*args,**kwargs):
        self.is_initialized = False