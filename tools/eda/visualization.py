from typing import Any, Optional, Union
from smolagents.tools import Tool
import matplotlib.pyplot as plt
import numpy as np

class bar(Tool):
    name = "bar"
    description = "Creates a bar graph from the given data.and the final image is saved in the images folder.the filename and the axes of the graph is returned."
    inputs = {
        "x": {"type": "array", "description": "The x values of the bars."},
        "height": {"type": "array", "description": "The height of the bars."},
        "bar_labels": {"type": "array", "description": "The labels of the bars.","nullable":True},
        "bar_colors": {"type": "array", "description": "The colors of the bars.","nullable":True},
        "ylabel": {"type": "string", "description": "The label of the y-axis.","nullable":True},
        "title": {"type": "string", "description": "The title of the graph.","nullable":True},
        "legend": {"type": "string", "description": "The legend of the graph.","nullable":True},
    }
    output_type="any"

    def forward(
        self,
        x: Union[list, np.array],
        height: Union[list, np.array],
        bar_labels: Optional[list]=None,
        bar_colors: Optional[list]=None,
        ylabel: Optional[str]=None,
        title: Optional[str]=None,
        legend: Optional[str]=None,
    ) -> Any:
        fig, ax = plt.subplots()
        ax.bar(x, height, color=bar_colors, label=bar_labels)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(title=legend)
        
        filename = "./images/bar_graph.png"
        plt.savefig(filename)
        return filename,ax

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
        plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
        plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
