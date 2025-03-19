class tool:
    def __init__(self,tool_id,user_id, name:str, description:str,inputs:str,output_type:str,file_path:str,create_time,update_time ):
        self.tool_id = tool_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.inputs = inputs
        self.output_type = output_type
        self.file_path = file_path
        self.update_time = update_time
        self.create_time = create_time