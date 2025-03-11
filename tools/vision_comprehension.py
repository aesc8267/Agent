from typing import Any, Optional
from smolagents.tools import Tool
import requests
import os
from openai import OpenAI
class VisionComprehension(Tool):
    name="vision_comprehension"
    description="you can use this tool to understand the image content by your prompt"
    inputs={
        "filename":{"type":"string","description":"the name of the file.eg: 'image.png'"},
        "file_dir":{"type":"string","description":"the dir of the file.eg: '/home/user/images/'"},
        "prompt":{"type":"string","description":"the question you want to ask about the image"}
    }
    output_type="any"
    def forward(self,filename:str,file_dir:str,prompt:str)->any:
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-vl-plus",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            extra_headers={"X-DashScope-OssResourceResolve": "enable"},
            messages=[{"role": "user","content": [
                    {"type": "text","text":prompt},
                    {"type": "image_url",
                    "image_url": {"url": self.getImagurl(filename,file_dir)},}
                    ]}]
            )
        # print(completion.model_dump_json())
        return completion.choices[0].message.content
    def getPolicy(self):
        url="https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model=qwen-vl-plus"
        headers={
            "Content-Type":"application/json",
            "Authorization":"Bearer "+self.api_key
        }
        res=requests.get(url=url,headers=headers)
        res
        res_data=res.json()['data']
        return res_data
    def getImagurl(self,filename,filedir):
        url = self.policy['upload_host']
        key=self.policy['upload_dir']+'/'+filename

        data={
            "policy": self.policy['policy'],
            "signature":self.policy['signature'],
            "OSSAccessKeyId": self.policy['oss_access_key_id'],
            "x-oss-object-acl": self.policy['x_oss_object_acl'],
            "x-oss-forbid-overwrite": self.policy['x_oss_forbid_overwrite'],
            "success_action_status":200,
            "key":key
        }
        files = {
            'file': open(os.path.join(filedir,filename), 'rb')  # 注意：此路径需根据实际情况调整
        }
        response = requests.post(url, data=data, files=files)
        # 关闭文件
        files['file'].close()
        if response.status_code == 200:
            print("文件上传成功")
            imagurl="oss://"+key
            return imagurl
        elif response.status_code == 403:
            self.policy=self.getPolicy()
            return self.getImagurl(filename,filedir)
        elif response.status_code == 409:
            print("文件上传重复，不允许覆盖：")
            print(response.status_code)
            print(response.text)
        else:
            print("文件上传失败，错误信息：")
            print(response.status_code)
            print(response.text)

    def __init__(self,*args,**kwargs):
        self.is_initialized = False
        self.api_key="sk-615616fb539749dda57c80cc0928669d"
        self.policy=self.getPolicy()