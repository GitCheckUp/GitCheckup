from io import BytesIO
import base64
import matplotlib.pyplot as plt
from math import ceil

#Change default styling
plt.style.use("ggplot")

#Chance font to Consolas
plt.rcParams['font.sans-serif'] = "Consolas"

#Remove borders.
plt.rcParams["axes.spines.left"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.bottom"] = False

#Remove background
plt.rcParams["savefig.transparent"] = True


def getGraph():
    buffer = BytesIO()
    plt.xticks(rotation=15, ha='right') #Rotate the tags on the x-axis
    plt.tight_layout()  #Solution for the tag cropping.
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_bar_plot(values, labels, title, xlabel = None):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.yticks(range(0, ceil(max(values) + 1), ceil(ceil(max(values) + 1) / 10)))
    plt.title(title)
    if (xlabel):
        plt.xlabel(xlabel)
    graph = getGraph()
    return graph

def get_pie_plot(values, labels, title, xlabel = None):
    values = list(values)
    labels = list(labels)
    for i in range(len(values) -1, -1, -1):
        if (values[i] == 0):
            values.pop(i)
            labels.pop(i)

    plt.switch_backend('AGG')
    plt.figure(figsize = (10, 6))
    plt.pie(values, labels = labels, shadow = True, autopct='%1.0f%%')
    plt.title(title)
    if (xlabel):
        plt.xlabel(xlabel)
    graph = getGraph()
    return graph
