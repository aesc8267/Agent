from typing import Any, Optional,Union
from smolagents.tools import Tool
import matplotlib.pyplot as plt
import numpy as np
class bar(Tool):
    name = "bar"
    description = "Plots a bar graph of the given data."
    inputs={'x':{'type':'array','description':'the x values of the bar graph'},'y':{'type':'array','description':'the y values of the bar graph'}}
    output_type = "image"
    def forward(self, x:Union[list,np.array],y:Union[list,np.array]) -> Any:
        plt.bar(x,y)
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.title("Bar Graph")
        plt.show()
    def __init__(self, *args, **kwargs):
        self.is_initialized = False