from flask import Flask, Response
import time
from flask_cors import CORS
from smolagents.agents import CodeAgent
# 知识检索 agent
from smolagents import CodeAgent, OpenAIServerModel, tool, HfApiModel, DuckDuckGoSearchTool
from tools.final_answer import FinalAnswerTool
from tools.visit_webpage import VisitWebpageTool
from tools.vision_comprehension import VisionComprehension
from tools.file_io import file_writer

model = OpenAIServerModel(model_id='qwen-max', api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                          api_key="sk-615616fb539749dda57c80cc0928669d")
# model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", provider="together")
agent = CodeAgent(model=model,
                  tools=[DuckDuckGoSearchTool(), file_writer(), VisitWebpageTool()],
                  additional_authorized_imports=['flask', 'os', 'matplotlib', 'pandas', 'numpy', 'seaborn', 'sklearn',
                                                 'torch', 'transformers', 'tensorflow', 'keras', 'cv2', 'PIL',
                                                 'matplotlib.pyplot', 'matplotlib.pyplot as plt', 'pandas as pd',
                                                 'numpy as np', 'seaborn as sns', 'sklearn as sk', 'torch as torch',
                                                 'transformers as transformers', 'tensorflow as tf', 'keras as keras',
                                                 'cv2 as cv2', 'PIL as PIL', 'matplotlib.pyplot as plt',
                                                 'matplotlib.pyplot as plt', 'pandas as pd', 'numpy as np',
                                                 'seaborn as sns', 'sklearn as sk', 'torch as torch',
                                                 'transformers as transformers', 'tensorflow as tf', 'keras as keras',
                                                 'cv2 as cv2', 'PIL as PIL'],
                  name='qwen_agent',
                  description='information extraction agent,can do rag and web search')
app = Flask(__name__)
CORS(app, origins='*')


def generate(task: str):
    chunks = agent.run(task, stream=True, reset=False)
    start = time.time()
    for chunk in chunks:
        yield chunk


@app.route('/events')
def events():
    task = "请从互联网上搜集，和东华大学有关的信息，帮我整理出来"
    return Response(generate(task), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
