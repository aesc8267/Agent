import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Union, Optional

data = [[1, 2, 3, 4], [5, 6, 7, 8]]


# def forward(x:Union[list,np.array],height:Union[list,np.array]) -> Any:
#     plt.bar(x,y)
#     plt.xlabel("Index")
#     plt.ylabel("Value")
#     plt.title("Bar Graph")
#     filename='./images/bar_graph.png'
#     plt.savefig(filename)
#     return filename
def forward(
    x: Union[list, np.array],
    height: Union[list, np.array],
    bar_labels: Optional[list]=None,
    bar_colors: Optional[list]=None,
    ylabel: Optional[str]=None,
    title: Optional[str]=None,
    legend: Optional[str]=None,
) -> Any:
    plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
    plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
    fig, ax = plt.subplots()
    ax.bar(x, height, color=bar_colors, label=bar_labels)

    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(title=legend)
    filename = "./images/bar_graph.png"
    plt.savefig(filename)    
    return ax

x = [1, 2, 3, 4]                                                                                                 
height = [2, 3, 4, 5]                                                                                            
bar_labels = ['a', 'b', 'c', 'd']                                                                                
bar_colors = ['red', 'blue', 'green', 'orange']                                                                  
                                                                                                                
ax = forward(x=x, height=height, bar_labels=bar_labels, bar_colors=bar_colors, ylabel='Y values', title='中文', legend='Data')  
ax.plot(x,height)
plt.show()